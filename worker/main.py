import json
import time
import sys
import redis
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient

from core.env import KAFKA_BROKER, LEAD_TOPIC, REDIS_HOST, REDIS_PORT
from core.logger import get_logger

logger = get_logger("imob_worker")

def wait_for_topic(broker_url: str, topic: str, max_retries: int = 15):
    admin = AdminClient({'bootstrap.servers': broker_url})
    
    logger.info("Starting Kafka readiness check...", extra={"topic": topic})

    for retry in range(1, max_retries + 1):
        try:
            metadata = admin.list_topics(topic, timeout=3.0)
            
            if topic in metadata.topics:
                logger.info("Topic found! Worker ready to consume.", extra={"topic": topic})
                return True
                
            logger.warning("Topic does not exist yet. Waiting for API to create...", extra={
                "attempt": f"{retry}/{max_retries}",
                "topic": topic
            })
            time.sleep(2)
            
        except Exception as e:
            logger.error("Failed to communicate with Kafka during check.", extra={"error": str(e)})
            time.sleep(2)

    logger.critical("Timeout exceeded. Topic was not created. Shutting down Worker.")
    sys.exit(1)

def init_worker():
    wait_for_topic(KAFKA_BROKER, LEAD_TOPIC)

    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'realtor_notification_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([LEAD_TOPIC])

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

    logger.info("Processing Worker started. Waiting for new leads...")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error("Kafka error occurred", extra={"error": str(msg.error())})
                    break
            
            lead_data = json.loads(msg.value().decode('utf-8'))
            lead_id = lead_data.get('_id')
            client_name = lead_data.get('nome')
            
            logger.info("Processing received lead", extra={"lead_id": lead_id, "client_name": client_name})
            
            redis_key = f"processed_lead:{lead_id}"
            if redis_client.exists(redis_key):
                logger.info("Lead already processed. Skipping duplicate.", extra={
                    "lead_id": lead_id, 
                    "action": "skip"
                })
                continue
            
            logger.info("Preparing notification for realtor about client...", extra={
                "lead_id": lead_id,
                "client_name": client_name
            })
            
            time.sleep(2) # Simulação de I/O (ex: envio de email)
            
            # 86400 segundos = 24 horas 
            redis_client.set(redis_key, "1", ex=86400)
            
            logger.info("Notification sent successfully! Lead completed.", extra={"lead_id": lead_id})
            
    except KeyboardInterrupt:
        logger.info("Shutting down worker gracefully...")
    finally:
        consumer.close()

if __name__ == "__main__":
    init_worker()

