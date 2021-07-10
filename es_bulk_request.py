import asyncio
import time
from datastore.main import ElasticsearchRequestHandler

es = ElasticsearchRequestHandler()

data_for_es = [{
    "product": {
        "id": 10,
        "name": "Funny Farm House Ketchup",
        "category": "Dips and Ketchups",
        "price": 100,
        "stock": 5,
    },
    "update_ts": 1625931472
}, {
    "product": {
        "id": 11,
        "name": "Salsa Dip",
        "category": "Dips and Ketchups",
        "price": 20,
        "stock": 100
    },
    "update_ts": 1625931472
}, {
    "product": {
        "id": 12,
        "name": "Cheese Nachos",
        "category": "Snacks",
        "price": 13.75,
        "stock": 1
    },
    "update_ts": 1625931472
}]


async def main():
    s = time.perf_counter()
    await es.bulk_indexing(data_for_es=data_for_es)

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

    await es.close_connection()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
