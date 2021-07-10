import typing
import logging
import time

from elasticsearch import AsyncElasticsearch

from pydantic import ValidationError

from datastore.config import ELASTICSEARCH_INSTANCE, ELASTICSEARCH_INDEX
from datastore.models.product import ProductInfoModel

logger = logging.getLogger()


class ElasticsearchRequestHandler:
    def __init__(self):
        self.es_client = AsyncElasticsearch(hosts=[ELASTICSEARCH_INSTANCE])

    async def get(self, product_id) -> typing.Any:
        """
        Retrieve document by id.
        """
        logger.info(f"searching in ES for product with id {product_id}")

        return await self.es_client.get(id=product_id,
                                        index=ELASTICSEARCH_INDEX)

    async def search(self, es_query) -> typing.Any:
        """
        Search for document by using query filters.
        """
        logger.info(f"searching in ES for product with query {es_query}")

        return await self.es_client.search(body=es_query,
                                           index=ELASTICSEARCH_INDEX)

    async def update(self, data, product_id) -> bool:
        """
        Update information in a document.
        """
        logger.info(f"update for product id {product_id} with data {data}")

        data_to_update = {"doc": {"product": data}}
        # validate data before update
        try:
            ProductInfoModel(id=product_id,
                             name=data['name'],
                             category=data['category'],
                             price=data['price'],
                             stock=data['stock'])
        except ValidationError as e:
            logger.error(
                f"an exception occurred during data update to ES: {e}")

        logger.info("data validation successful, sending update to ES")
        resp = await self.es_client.update(id=product_id,
                                           body=data_to_update,
                                           index=ELASTICSEARCH_INDEX)

        return True if resp else False

    async def setup(self, mappings_and_settings) -> None:
        """
        Setup index settings and mappings.
        """
        logger.info(f"creating index with mappings")
        await self.es_client.indices.create(index=ELASTICSEARCH_INDEX,
                                            body=mappings_and_settings)

        logger.info(f"waiting for cluster green health")

        time.sleep(2)
        logger.info(f"index created successfully")

    async def bulk_indexing(self, data_for_es) -> None:
        """
        Prepare data by bulk indexing in ES.
        """
        bulk_data = []

        for product_data in data_for_es:
            metadata = {
                "index": {
                    "_index": ELASTICSEARCH_INDEX,
                    "_id": product_data['product']['id']
                }
            }
            # first append metadata
            bulk_data.append(metadata)
            # then append actual data
            bulk_data.append(product_data)

        logger.info(f"performing bulk indexing of data")
        await self.es_client.bulk(index=ELASTICSEARCH_INDEX, body=bulk_data)

        time.sleep(2)
        logger.info(f"bulk indexing successful")

    async def close_connection(self):
        """
        Close ES connection after processing everything.
        """
        await self.es_client.close()
