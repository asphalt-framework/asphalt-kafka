from aiokafka import AIOKafkaConsumer

from asphalt.core import get_resource


async def handler() -> None:
    consumer = await get_resource(AIOKafkaConsumer)

    # Receive messages from all the subscribed topics
    async for msg in consumer:
        ...  # do something with the message
