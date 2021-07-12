import asyncio
from datetime import datetime
import json

from elasticsearch import AsyncElasticsearch

from aiokafka import AIOKafkaConsumer
from elasticsearch.exceptions import TransportError

from app.core.config import KAFKA_INSTANCE
from app.core.config import PROJECT_NAME

from app.core.models.model import ConsumerResponse
from fastapi import FastAPI

from loguru import logger

app = FastAPI(title=PROJECT_NAME)

loop = asyncio.get_event_loop()

es = AsyncElasticsearch(hosts=['http://127.0.0.1:9200'])


def kafka_json_deserializer(serialized):
    return json.loads(serialized)


@app.get("/consumer/{topicname}")
async def kafka_consume(topicname: str):
    """
    Produce a message into <topicname>
    This will produce a message into a Apache Kafka topic.
    """
    consumer = AIOKafkaConsumer(topicname,
                                loop=loop,
                                client_id=PROJECT_NAME,
                                bootstrap_servers=KAFKA_INSTANCE,
                                enable_auto_commit=True,
                                value_deserializer=kafka_json_deserializer)

    await consumer.start()
    logger.debug('starting consumer task')

    retrieved_requests = []
    try:
        result = await consumer.getmany(timeout_ms=20000)
        logger.info(f"Got {len(result)} messages in {topicname}.")

        for _, messages in result.items():
            if messages:
                for message in messages:
                    retrieved_requests.append({"value": message.value})

        for request in retrieved_requests:
            value = request.get('value')
            product_id = value.get('product_id')
            price = value.get('price')
            stock = value.get('stock')

            logger.info("data before sending to elasticsearch for update")
            try:
                data = await es.get(index='retail-catalogue', id=product_id)
                logger.info("data: ", data['_source'])
            except TransportError as e:
                raise e

            logger.info("after update, new data in elasticsearch")
            data['_source']['product']['id'] = product_id
            data['_source']['product']['price'] = price
            data['_source']['product']['stock'] = stock

            product_name = data['_source']['product']['name']
            product_id = data['_source']['product']['id']

            update_data = data['_source']
            data_for_update = {'doc': {"product": update_data['product']}}

            logger.info("data going for update in elasticsearch")
            try:
                await es.update(index='retail-catalogue',
                                body=data_for_update,
                                id=product_id)

                response = ConsumerResponse(topic=topicname,
                                            timestamp=str(datetime.now()),
                                            product_name=product_name,
                                            product_id=product_id,
                                            success=True)

                logger.info(response)
            except TransportError as e:
                raise e

            return response

    except Exception as e:
        logger.error(
            f"Error when trying to consume request on topic {topicname}: {str(e)}"
        )
    finally:
        await consumer.stop()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
