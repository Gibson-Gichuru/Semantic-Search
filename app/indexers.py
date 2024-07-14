from redis.commands.search.field import (
    TextField,
    TagField,
    NumericField,
    VectorField
)

PRODUCT_REVIEW_SCHEMA = (
    TextField("$.Summary", no_stem=True, as_name="Summary"),
    NumericField("$.Score", as_name="Score"),
    TextField("$.Text", no_stem=True, as_name="Text"),
    TagField("$.profilename", as_name="profilename"),
    TagField("$.productid", as_name="productid"),
    VectorField(
        "$.text_embeddings",
        "FLAT",
        {
            "TYPE":"FLOAT32",
            "DIM":1536,
            "DISTANCE_METRIC":"COSINE",
        },
        as_name="vector"
    )
)


PRODUCT_SCHEMA = (
    TagField("$.productid", as_name="productid"),
    TagField("$.name", as_name="name"),
    TextField("$.description", no_stem=True, as_name="description"),
    TagField("$.category", as_name="category"),
    NumericField("$.price", as_name="price"),
    VectorField(
        "$.description_embeddings",
        "FLAT",
        {
            "TYPE":"FLOAT32",
            "DIM":1536,
            "DISTANCE_METRIC":"COSINE",
        },
        as_name="vector"
    )
)