from starlette.config import Config

config = Config('.env')

PROJECT_NAME: str = config("RETAIL_APP", default='retail-kafka-producer')

KAFKA_INSTANCE: str = config("KAFKA_INSTANCE", default='localhost:9092')
