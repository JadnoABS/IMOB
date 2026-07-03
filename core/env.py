import os
import sys

def get_env_var(key: str) -> str:
    try:
        return os.environ[key]
    except KeyError:
        print(f"ERRO CRÍTICO: Variável de ambiente '{key}' não encontrada!")
        print("A aplicação não pode iniciar sem esta configuração.")
        sys.exit(1)

MONGO_URL = get_env_var("MONGO_URL")
KAFKA_BROKER = get_env_var("KAFKA_BROKER")
LEAD_TOPIC = get_env_var("LEAD_TOPIC")
REDIS_HOST = get_env_var("REDIS_HOST")
REDIS_PORT = get_env_var("REDIS_PORT")
JWT_SECRET= get_env_var("JWT_SECRET")
DEFAULT_PASSWORD = get_env_var("DEFAULT_PASSWORD")
SERVER_URL= get_env_var("SERVER_URL")
