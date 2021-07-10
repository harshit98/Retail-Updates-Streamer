import asyncio
import time
from datastore.main import ElasticsearchRequestHandler

es = ElasticsearchRequestHandler()


async def main():
    # get single document
    product_id = 10
    print(f"product having id {product_id}: {await es.get(product_id)}")

    # get multiple documents having stock greater than 0
    query = {
        "query": {
            "bool": {
                "must": {
                    "range": {
                        "product.stock": {
                            "gt": 6
                        }
                    }
                }
            }
        }
    }
    print(f"products having stock > 6 :: {await es.search(query)}")

    # update price of product with id = 200
    resp = await es.get(product_id)
    product = resp.get('_source').get('product')

    print(f"product price before update {product['price']}")
    product['price'] = 8.5
    print(f"product price after update {product['price']}")

    update = await es.update(product, product_id)
    if update:
        print(f"product updated successfully")
    else:
        print(f"product update failed")

    # close ES connection
    await es.close_connection()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
