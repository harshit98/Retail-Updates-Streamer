import asyncio
import typing
import logging
import time

from elasticsearch import AsyncElasticsearch

from datastore.config import ELASTICSEARCH_HOST, ELASTICSEARCH_INSTANCE, ELASTICSEARCH_INDEX

logger = logging.getLogger()

loop = asyncio.get_event_loop()


class ElasticsearchRequestHandler:
    def __init__(self):
        self.es_client = AsyncElasticsearch(hosts=[ELASTICSEARCH_INSTANCE],
                                            loop=loop)

    async def get(self, product_id) -> typing.Any:
        logger.info(f"searching in ES for product with id {product_id}")

        return await self.es_client.get(id=product_id,
                                        index=ELASTICSEARCH_INDEX)

    async def search(self, es_query) -> typing.Any:
        logger.info(f"searching in ES for product with query {es_query}")

        return await self.es_client.search(body=es_query,
                                           index=ELASTICSEARCH_INDEX)

    async def update(self, data, product_id) -> bool:
        logger.info(f"update for product id {product_id} with data {data}")

        data_to_update = {"doc": {"product": data}}
        resp = await self.es_client.update(id=product_id,
                                           body=data_to_update,
                                           index=ELASTICSEARCH_INDEX)

        return True if resp else False

    async def setup(self) -> None:
        logger.info(f"creating index with mappings")
        await self.es_client.indices.create(index=ELASTICSEARCH_HOST)

        logger.info(f"waiting for cluster green health")

        time.sleep(2)
        logger.info(f"index created successfully")

    async def bulk_indexing(self, data_for_es) -> None:
        bulk_data = []

        for _, row in data_for_es.iterrows():
            doc = {
                "index": {
                    "_index": ELASTICSEARCH_INDEX,
                    "_type": '_doc',
                    "_id": row['product']['id']
                }
            }
            bulk_data.append(doc)

        logger.info(f"performing bulk indexing of data")
        await self.es_client.bulk(index=ELASTICSEARCH_INDEX, body=bulk_data)
        time.sleep(2)
        logger.info(f"bulk indexing successful")
