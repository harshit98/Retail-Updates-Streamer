from datastore.main import ElasticsearchRequestHandler

es = ElasticsearchRequestHandler()

# get single document
product_id = 200
print(f"product having id {product_id} :: {es.get(product_id)}")

# get multiple documents having stock greater than 0
query = {"query": {"bool": {"must": {"range": {"product.stock": {"gt": 0}}}}}}
print(f"products having stock > 0 :: {es.search(query)}")

# update price of product with id = 200
resp = es.get(product_id)
results = resp.get('hits').get('hits')
product = results.get('_source').get('product')

print(f"product price before update {product['price']}")
product['price'] = 8.5
print(f"product price after update {product['price']}")

update = es.update(product, product_id)
if update:
    print(f"product updated successfully")
else:
    print(f"product update failed")
