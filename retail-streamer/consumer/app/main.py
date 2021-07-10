import asyncio
import json
import typing

from aiokafka import AIOKafkaConsumer

from consumer.app.core.config import KAFKA_INSTANCE, PROJECT_NAME

from consumer.app.core.models.models import ConsumerResponseModel

from fastapi import FastAPI, WebSocket

from consumer.app.core.logging import Logger

from starlette.endpoints import WebSocketEndpoint
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title=PROJECT_NAME)

app.add_middleware(CORSMiddleware, allow_origins=['*'])

logger = Logger()


async def consume_message(consumer, topic_name):
    async for msg in consumer:
        return msg.value.decode()


@app.websocket_route('/consumer/{topic_name}')
class WebSocketConsumer(WebSocketEndpoint):
    """
    This class will start consuming messages from kafka topic.
    """
    async def on_connect(self, websocket: WebSocket) -> None:
        topic_name = websocket['path'].split('/')[2]

        await websocket.accept()
        await websocket.send_json({'message': 'connected'})

        loop = asyncio.get_event_loop()

        self.consumer = AIOKafkaConsumer(topic_name,
                                         loop=loop,
                                         client_id=PROJECT_NAME,
                                         bootstrap_servers=KAFKA_INSTANCE,
                                         enable_auto_commit=True)

        await self.consumer.start()

        self.consumer_task = asyncio.create_task(
            self.send_consumer_message(websocket=websocket,
                                       topic_name=topic_name))

        logger.info('connected')

    async def on_disconnect(self, websocket: WebSocket) -> None:
        self.consumer_task.cancel()
        await self.consumer.stop()

        logger.info(f"counter: {self.counter}")
        logger.info("disconnected")
        logger.info("consumer stopped")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({'message': data})

    async def send_consumer_message(self, websocket: WebSocket,
                                    topic_name: str) -> None:
        self.counter = 0

        while True:
            data = await consume_message(self.consumer, topic_name)
            response = ConsumerResponseModel(topic=topic_name,
                                             **json.loads(data))
            logger.info(response)

            await websocket.send_text(f"{response.json()}")
            self.counter += 1


def health():
    return {'message': 'consumer part up and running'}
