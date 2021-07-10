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
                'name': {
                    'index': 'analyzed',
                    'type': 'string'
                },
                'category': {
                    'index': 'analyzed',
                    'type': 'string'
                },
                'id': {
                    'index': 'not_analyzed',
                    'type': 'integer'
                },
                'price': {
                    'index': 'not_analyzed',
                    'type': 'float'
                },
                'stock': {
                    'index': 'not_analyzed',
                    'type': 'integer'
                }
            },
            'update_ts': {
                'index': 'not_analyzed',
                'type': 'date',
                'format': 'epoch_second'
            }
        }
    }
}
