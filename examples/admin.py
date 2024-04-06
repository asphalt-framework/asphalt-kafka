from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from asphalt.core import get_resource


async def handler() -> None:
    client = await get_resource(AIOKafkaAdminClient)

    # Create a new topic (new.topic) with 5 partitions and a replication factor of 3
    await client.create_topics([NewTopic("new.topic", 5, 3)])
