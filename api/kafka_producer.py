import json
from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from core.env import KAFKA_BROKER, LEAD_TOPIC
from core.logger import get_logger

logger = get_logger("imob_api")

conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(conf)

def init_topic():
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
    lead_topic = NewTopic(LEAD_TOPIC, num_partitions=1, replication_factor=1)
    futures = admin_client.create_topics([lead_topic])

    for topic, future in futures.items():
        try:
            future.result()
            logger.info("Topic successfully created.", extra={"topic": topic})
            
        except KafkaException as e:
            error_kafka = e.args[0]

            if error_kafka.code() == KafkaError.TOPIC_ALREADY_EXISTS:
                logger.info("Topic already exists.", extra={"topic": topic, "action": "skip"})
            else:
                logger.warning("Error on Kafka while trying to create topic", extra={
                    "topic": topic, 
                    "error": str(error_kafka)
                })
                
        except Exception as e:
            logger.error("Fatal error while trying to create topic", extra={
                "topic": topic, 
                "error": str(e)
            })

def send_lead_event(lead_data: dict):
    def delivery_report(err, msg):
        if err is not None:
            logger.error("Error while trying to deliver Kafka message", extra={"error": str(err)})
        else:
            logger.info("Message successfully delivered", extra={
                "topic": msg.topic(),
                "partition": msg.partition()
            })

    payload = json.dumps(lead_data).encode('utf-8')

    producer.produce(
        topic=LEAD_TOPIC,
        value=payload,
        callback=delivery_report
    )
    
    producer.poll(0)
