from app import create_app
import os
import csv
import random
from app.schema import Customer, KeyNamingScheme, Product, EmbeddingModels
from config import base_dir


app = create_app(os.environ.get('ENV') or "default")


def setup_ids(pipeline, key, row_index):

    with open(os.path.join(base_dir, "data/Reviews.csv")) as file:

        reader = csv.reader(file)

        counter = 0

        for row in reader:

            # skip header
            if counter == 0:
                counter += 1
                continue

            pipeline.sadd(key, row[row_index])

    pipeline.execute()


def load_user_data(faker_obj, pipeline):

    gender_choices = ("M", "F")

    available_user_ids = app.redis_client.scard("user:allowed:ids")

    if available_user_ids == 0:
        setup_ids(pipeline, "user:allowed:ids", 2)

    available_user_ids = app.redis_client.scard("user:allowed:ids")
    # creating fake customers

    while available_user_ids > 0:

        user_id = app.redis_client.spop("user:allowed:ids")

        user = Customer(
            **faker_obj.simple_profile(sex=random.choice(gender_choices)),
            userid=user_id,
        )

        pipeline.hset(KeyNamingScheme.USER_KEY.value+user_id, mapping=user.__dict__)

        available_user_ids = app.redis_client.scard("user:allowed:ids")

        print(f"loading user: {user.name} to pipeline")


def load_product_data(faker_obj, pipeline):

    available_product_ids = app.redis_client.scard("product:allowed:ids")

    if available_product_ids == 0:

        setup_ids(pipeline, "product:allowed:ids", 1)

    available_product_ids = app.redis_client.scard("product:allowed:ids")


    while available_product_ids > 0:

        product_id = app.redis_client.spop("product:allowed:ids")

        description = faker_obj.paragraph()

        description_embeddings = app.open_ai_client.embeddings.create(
            input=description,
            model=EmbeddingModels.MODEL_3_SMALL.value
        ).data[0].embedding

        product = Product(
            productid=product_id,
            name=faker_obj.word(),
            description=description,
            category=faker_obj.word(),
            price=faker_obj.pydecimal(left_digits=3, right_digits=2, positive=True),
            description_embeddings=description_embeddings
        )

        pipeline.json().set(
            KeyNamingScheme.PRODUCT_KEY.value+product_id,
            "$",
            product.__dict__
        )

        available_product_ids = app.redis_client.scard("product:allowed:ids")

        print(f"Loading product: {product.name} to pipeline")
    

def __update_review_embeddings(review, open_ai_client):

    embedding = open_ai_client.embeddings.create(
        input=review.Text,
        model=EmbeddingModels.MODEL_3_SMALL.value
    ).data[0].embedding

    review.text_embeddings = embedding
    return review


def load_product_reviews(pipeline):

    from config import environment

    list(map(
        lambda item : pipeline.json().set(
            KeyNamingScheme.PRODUCT_REVIEW.value+item.Id,
            "$",
           __update_review_embeddings(item, app.open_ai_client).__dict__
        ),
        environment[app.config["ENV"]].load_data('reviews.csv')
    ))


@app.cli.command()
def load_dev_data():

    assert app.config['ENV'] == "development", "load_data is only for development environment"

    from faker import Faker

    pipeline = app.redis_client.pipeline()

    faker_obj = Faker()

    load_user_data(faker_obj, pipeline)

    load_product_data(faker_obj, pipeline)

    load_product_reviews(pipeline)

    pipeline.execute()


@app.cli.command()
def register_indexers():


    from app.indexers import PRODUCT_REVIEW_SCHEMA, PRODUCT_SCHEMA

    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.exceptions import ResponseError

    
    # Registering Product review index

    try:
        product_index_defination =IndexDefinition(
            prefix=[KeyNamingScheme.PRODUCT_REVIEW.value], 
            index_type=IndexType.JSON
        )

        app.redis_client.ft(KeyNamingScheme.PRODUCT_REVIEW_INDEXER.value).create_index(
            fields=PRODUCT_REVIEW_SCHEMA,
            definition=product_index_defination
        )

        print("Product Review Indexer created")

    except ResponseError as e:

        print(f"Product Review {e}")


    # Registering Product index

    try:

        product_indexer_defination = IndexDefinition(
            prefix=[KeyNamingScheme.PRODUCT_KEY.value],
            index_type=IndexType.JSON
        )

        app.redis_client.ft(
            KeyNamingScheme.PRODUCT_INDEXER.value
        ).create_index(
            fields=PRODUCT_SCHEMA,
            definition=product_indexer_defination
        )

        print("Product Indexer created")

    except ResponseError as e:

        print(f"Product {e}")