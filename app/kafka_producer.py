import json
from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def send_lead_event(lead_data: dict):
    def delivery_report(err, msg):
        if err is not None:
            print(f"Erro ao entregar mensagem: {err}")
        else:
            print(f"Mensagem entregue no tópico {msg.topic()} [Partição: {msg.partition()}]")

    payload = json.dumps(lead_data).encode('utf-8')

    producer.produce(
        topic='lead',
        value=payload,
        callback=delivery_report
    )
    
    producer.poll(0)
