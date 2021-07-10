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

es.bulk_indexing(data_for_es=data_for_es)
