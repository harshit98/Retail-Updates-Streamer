from pydantic import BaseModel


class ConsumerResponseModel(BaseModel):
    product: str
    price: float
    stock: int
    status: int
    message: str
