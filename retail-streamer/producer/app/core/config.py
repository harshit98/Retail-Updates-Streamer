from starlette.config import Config

config = Config('.env')

PROJECT_NAME: str = config("RETAIL_APP", default='retail-kafka-producer')

KAFKA_HOST: str = config("KAFKA_HOST")
KAFKA_PORT: str = config("KAFKA_PORT")

KAFKA_INSTANCE = KAFKA_HOST + ":" + KAFKA_HOST
