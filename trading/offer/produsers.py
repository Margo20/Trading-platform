import time

from kafka import KafkaProducer
def send_to_kafka():

    producer = KafkaProducer(bootstrap_servers='10.1.0.111:9092')
    for _ in range(100):
        # producer.send('topic-email',  b'some_message_bytes')
        # producer.send('topic-email', key=b'foo', value=b'bar')
        producer.send('topic-email', b'05.01.2022 hello')
        producer.flush()
        # producer.send('geostream', b'05.01.2022 hello')
        print('i send a message')
        time.sleep(5)


if __name__=="__main__":
    send_to_kafka()


# from pykafka import KafkaClient
# import time
#
# client = KafkaClient("127.0.0.1:9092")
# geostream = client.topics["geostream"]
#
# with geostream.get_sync_producer() as producer:
#     i = 0
#     for _ in range(10):
#         producer.produce(b"Kafka is not just an author " + str(i).encode("ascii"))
#         i += 1
#         time.sleep(1)

# def send_to_kafka(email):
#     # producer.send('topic-email', key=str(uuid4()), value=email)
#     # producer.send('topic-email', 'email')
#     pass
#
# def send_to_kafka(email):
#     pass


#
# from pykafka import KafkaClient
# import time
#
# client = KafkaClient("127.0.0.1:9092")
# topic_email = client.topics["topic-email"]
#
# with topic_email.get_sync_producer() as producer:
#     i = 0
#     for _ in range(10):
#         producer.produce(b"Kafka is not just an author " + str(i).encode("ascii"))
#         i += 1
#         time.sleep(1)



# from aiokafka import AIOKafkaProducer
# import asyncio
#
# async def send_one():
#     producer = AIOKafkaProducer(
#         bootstrap_servers='localhost:9092')
#
#     # Get cluster layout and initial topic/partition leadership information
#     await producer.start()
#     print('start_hello')
#     try:
#         # Produce message
#         for _ in range(3):
#
#           await producer.send_and_wait("topic-email", b"Super message Happy New Year!!!")
#
#           print('i send a message')
#     finally:
#         # Wait for all pending messages to be delivered or expire.
#         await producer.stop()
#
# if __name__=="__main__":
#     asyncio.run(send_one())
