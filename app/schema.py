from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class KeyNamingScheme(Enum):

    USER_KEY = "user:"
    PRODUCT_KEY = "product:"
    PRODUCT_REVIEW = "product:review:"
    PRODUCT_REVIEW_INDEXER = "idx:product:review"
    PRODUCT_INDEXER = "idx:product"


class EmbeddingModels(Enum):

    MODEL_3_SMALL = "text-embedding-3-small"

class Customer(BaseModel):
    username: str
    userid: str
    name: str
    sex: str
    address: str
    mail: str

class Product(BaseModel):
    productid: str
    name: str
    description: str
    category: str
    price: float
    description_embeddings: Optional[List[float]] = []


class BaseQuery(BaseModel):
    query: str
    items: int

class ProductQuery(BaseQuery):

    name: Optional[str] = None
    category: Optional[str] = None

class ProductReviewQuery(BaseQuery):

    pass

class ProductReview(BaseModel):
    Id: str
    profilename: str
    productid: str
    userid: str
    HelpfulnessNumerator: int
    HelpfulnessDenominator: int
    Score: int
    Time: int
    Summary: str
    Text: str
    text_embeddings: Optional[List[float]] = []

class ProductReviewOut(BaseModel):
    vector_score: float
    productid: str
    Summary: str
    Score: int
    Text: str