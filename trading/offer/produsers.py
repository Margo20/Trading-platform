import time
from kafka import KafkaProducer


def send_to_kafka():

    producer = KafkaProducer(bootstrap_servers='10.1.0.111:9092')
    for _ in range(1):
        producer.send('topic-email', b'rita.aniskovets@gmail.com')
        producer.flush()
        print('i send a message')
        time.sleep(5)


if __name__=="__main__":
    send_to_kafka()
