import uuid

from datetime import datetime

from pydantic import BaseModel
from pydantic import validator


class ProducerMessageModel(BaseModel):
    name: str
    message_id: str = ""
    timestamp: str = ""

    @validator("message_id", pre=True, always=True)
    def set_message_id(values):
        if "name" in values:
            return f"{values['name']}_{uuid.uuid4()}"
        else:
            raise ValueError("'name' field is not present in values")

    @validator("timestamp", pre=True, always=True)
    def set_timestamp():
        return str(datetime.utcnow())


class ProducerResponseModel(BaseModel):
    name: str
    message_id: str
    topic: str
    timestamp: str = ""
    status: int
    message: str

    @validator("timestamp", pre=True, always=True)
    def set_timestamp():
        return str(datetime.utcnow())
