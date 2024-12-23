from aiokafka import AIOKafkaProducer

from asphalt.core import get_resource


async def handler() -> None:
    producer = await get_resource(AIOKafkaProducer)

    # Send "data" to the topic "some.topic"
    await producer.send("some.topic", b"data")
