from __future__ import annotations

from collections.abc import MutableMapping
from dataclasses import dataclass, field
from ssl import SSLContext
from typing import Any

from aiokafka import AIOKafkaProducer
from asphalt.core import Component, add_resource, get_resource


@dataclass
class KafkaProducerComponent(Component):
    """
    Publishes a Kafka producer as a resource.

    :param resource_name: name of the producer resource to publish
    :param ssl_context: SSL context to use (can be the name of an
        :class:`~ssl.SSLContext` resource)
    :param options: keyword arguments to pass to :class:`~aiokafka.AIOKafkaProducer`
    """

    resource_name: str = "default"
    ssl_context: str | SSLContext | None = None
    options: MutableMapping[str, Any] = field(default_factory=dict)
    existing_resource: AIOKafkaProducer | str | None = None

    async def start(self) -> None:
        if self.existing_resource is not None:
            if isinstance(self.existing_resource, str):
                producer = await get_resource(
                    AIOKafkaProducer, self.existing_resource, wait=True
                )
            else:
                producer = self.existing_resource

            if self.existing_resource != self.resource_name:
                add_resource(producer, self.resource_name)

            return

        if isinstance(self.ssl_context, str):
            self.options["ssl_context"] = await get_resource(SSLContext, wait=True)
        elif self.ssl_context is not None:
            self.options["ssl_context"] = self.ssl_context

        producer = AIOKafkaProducer(**self.options)
        await producer.start()
        add_resource(producer, self.resource_name, teardown_callback=producer.stop)
