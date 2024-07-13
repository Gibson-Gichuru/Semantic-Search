from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class KeyNamingScheme(Enum):

    USER_KEY = "user:{}"
    PRODUCT_KEY = "product:{}"
    PRODUCT_REVIEW = "product:review:{}"


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

