from __future__ import annotations

from asyncio import CancelledError
from collections.abc import AsyncGenerator, MutableMapping, Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from ssl import SSLContext
from typing import Any

from aiokafka import AIOKafkaConsumer

from asphalt.core import Component, add_resource, context_teardown, get_resource


@dataclass
class KafkaConsumerComponent(Component):
    """
    Publishes a Kafka consumer as a resource.

    :param resource_name: name of the consumer resource to publish
    :param ssl_context: SSL context to use (can be the name of an
        :class:`~ssl.SSLContext` resource)
    :param options: keyword arguments to pass to :class:`~aiokafka.AIOKafkaConsumer`
    :param topics: topics to subscribe to
    :param existing_resource: an existing :class:`~aiokafka.AIOKafkaConsumer` object, or
        the resource name of one, that should be used instead of creating a new one
    """

    resource_name: str = "default"
    ssl_context: str | SSLContext | None = None
    options: MutableMapping[str, Any] = field(default_factory=dict)
    topics: Sequence[str] = field(default_factory=list)
    existing_resource: AIOKafkaConsumer | str | None = None

    @context_teardown
    async def start(self) -> AsyncGenerator[None, Any]:
        if self.existing_resource is not None:
            if isinstance(self.existing_resource, str):
                consumer = await get_resource(
                    AIOKafkaConsumer, self.existing_resource, wait=True
                )
            else:
                consumer = self.existing_resource

            if self.existing_resource != self.resource_name:
                add_resource(consumer, self.resource_name)

            yield
            return

        if isinstance(self.ssl_context, str):
            self.options["ssl_context"] = await get_resource(SSLContext, wait=True)
        elif self.ssl_context is not None:
            self.options["ssl_context"] = self.ssl_context

        consumer = AIOKafkaConsumer(*self.topics, **self.options)
        await consumer.start()
        add_resource(consumer, self.resource_name)

        yield

        # Workaround for https://github.com/aio-libs/aiokafka/issues/647
        with suppress(CancelledError):
            await consumer.stop()
