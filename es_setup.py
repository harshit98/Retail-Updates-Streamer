import asyncio
import aiohttp
import time

from datastore.main import ElasticsearchRequestHandler

es = ElasticsearchRequestHandler()

request_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    'mappings': {
        'properties': {
            'product': {
                'type': 'object',
                'properties': {
                    'name': {
                        'index': True,
                        'type': 'text'
                    },
                    'category': {
                        'index': True,
                        'type': 'text'
                    },
                    'id': {
                        'index': True,
                        'type': 'integer'
                    },
                    'price': {
                        'index': True,
                        'type': 'float'
                    },
                    'stock': {
                        'index': True,
                        'type': 'integer'
                    }
                }
            },
            'update_ts': {
                'index': True,
                'type': 'date',
                'format': 'epoch_second'
            }
        }
    }
}


async def main():
    s = time.perf_counter()
    await es.setup(mappings_and_settings=request_body)

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
    await es.close_connection()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
