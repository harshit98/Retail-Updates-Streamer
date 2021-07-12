import uuid

from datetime import datetime

from pydantic import BaseModel
from pydantic import validator

from loguru import logger


class ProducerMessage(BaseModel):
    timestamp: str = ""
    name: str
    category: str
    price: float
    stock: int
    product_id: int

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())


class ProducerResponse(BaseModel):
    name: str
    message_id: str
    topic: str
    timestamp: str
