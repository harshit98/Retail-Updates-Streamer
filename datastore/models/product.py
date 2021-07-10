from pydantic import BaseModel


class ProductInfoModel(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int


class ProductModel(BaseModel):
    product: ProductInfoModel
    update_ts: int
