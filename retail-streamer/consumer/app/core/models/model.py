from pydantic import BaseModel


class ConsumerResponse(BaseModel):
    topic: str
    timestamp: str
    product_name: str
    product_id: int
    success: bool
