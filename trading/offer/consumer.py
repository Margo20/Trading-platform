# import asyncio
# from aiokafka import AIOKafkaConsumer
#
# from trading.celery import app
#
#
# async def consumer():
#     consumer = AIOKafkaConsumer(
#         'topic-email',
#         bootstrap_servers='10.1.0.111:9092')
#     topics = ['topic-email', 'topic1', 'topic2', 'topic3']
#     consumer.subscribe(topics)
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             print("consumed: ", msg.topic, msg.partition, msg.offset,
#                   msg.key, msg.value, msg.timestamp)
#     finally:
#         await consumer.stop()
#
# # @app.on_event('startup')
# # async def startup():
# #     asyncio.create_task(consumer())
#
# if __name__=="__main__":
#     asyncio.run(consumer())

from pykafka import KafkaClient

client = KafkaClient(hosts="10.1.0.111:9092")
# client = KafkaClient(hosts="localhost:9092")
# client = KafkaClient(hosts="kafka:9092")


def get_messages(topicname):
    def events():
        for message in client.topics[topicname].get_simple_consumer():
            yield message.value.decode()

    return events()

v=0
for x in get_messages("topic-email"):
    print(x,v)
    v+=1
