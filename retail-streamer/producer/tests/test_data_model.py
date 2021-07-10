import pytest

from producer.app.core.models.models import ProducerResponseModel
from producer.app.core.models.models import ProducerMessageModel

from pydantic import ValidationError


def test_producer_message():
    message = ProducerMessageModel(name='message_1')

    assert all([msg in message.dict()]
               for msg in ['name', 'message_id', 'timestamp'])

    assert isinstance(message.timestamp, str)
