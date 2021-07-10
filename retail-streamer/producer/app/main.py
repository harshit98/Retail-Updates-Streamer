import asyncio
import json

from aiokafka import AIOKafkaProducer

from producer.app.core.config import KAFKA_INSTANCE
from producer.app.core.config import PROJECT_NAME

from producer.app.core.models.models import ProducerMessageModel
from producer.app.core.models.models import ProducerResponseModel

from producer.app.core.logging import Logger

from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title=PROJECT_NAME)

loop = asyncio.get_event_loop()

aioproducer = AIOKafkaProducer(loop=loop,
                               client_id=PROJECT_NAME,
                               bootstrap_servers=KAFKA_INSTANCE)

logger = Logger()


@app.on_event('startup')
async def startup_event():
    await aioproducer.start()


@app.on_event('shutdown')
async def shutdown_event():
    await aioproducer.stop()


@app.post('/producer/{topic_name}')
async def produce_message(message: ProducerMessageModel, topic_name: str):
    """
    This method will produce a message into Kafka topic.
    """
    await aioproducer.send(topic_name,
                           json.dumps(message.dict()).encode('ascii'))

    response = ProducerResponseModel(
        name=message.name,
        message_id=message.message_id,
        topic=topic_name,
        message='message pushed to kafka successfully',
        status=1)

    logger.info(response)
    return response


@app.get('/health')
def health():
    return {'status': 'producer part up and running'}
