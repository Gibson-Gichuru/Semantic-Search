from redis.commands.search.query import Query
from flask import current_app
from app.schema import EmbeddingModels, ProductQuery, ProductReviewQuery
import numpy as np

class QueryFactory:

    def __init__(self):

        pass

    @staticmethod
    def get_embeddings_blob(query:str):

        embeddings = current_app.open_ai_client.embeddings.create(
            input=query,
            model=EmbeddingModels.MODEL_3_SMALL.value
        ).data[0].embedding

        return np.array(embeddings, dtype=np.float32).tobytes()
    


class ProductQueryBulder(QueryFactory):

    
    @staticmethod
    def build(query:ProductQuery) -> Query:

        filter_ = ""

        query_ = query.__dict__

        if query_.get("name"):

            filter_ = filter_.join(f"@name:{query_['name']}")

        if query_.get("category"):

            filter_ = filter_.join(f" @category:{query_['category']}")

        if filter_ == "":

            filter_ = "*"

        
        return Query(
            f"({filter_})=> [KNN $items @vector $vector_blob as vector_score]"
        ).sort_by("vector_score").dialect(2)



class ProductReviewQueryBulder(QueryFactory):

    @staticmethod
    def build(query:ProductReviewQuery):

        query = Query(
            '(*)=> [KNN $items @vector $vector_blob as vector_score]'
        ).sort_by("vector_score").return_fields(
            "vector_score",
            "productid",
            "Summary",
            "Score",
            "Text"
        ).dialect(2)

        return query