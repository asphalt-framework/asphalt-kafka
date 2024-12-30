from __future__ import annotations

from collections.abc import MutableMapping
from dataclasses import dataclass, field
from ssl import SSLContext
from typing import Any

from aiokafka.admin import AIOKafkaAdminClient

from asphalt.core import Component, add_resource, get_resource


@dataclass
class KafkaAdminComponent(Component):
    """
    Publishes a Kafka admin client as a resource.

    :param resource_name: name of the producer resource to publish
    :param ssl_context: SSL context to use (can be the name of an
        :class:`~ssl.SSLContext` resource)
    :param options: keyword arguments to pass to AIOKafkaAdminClient_

    .. _AIOKafkaAdminClient: https://github.com/aio-libs/aiokafka/blob/master/aiokafka/\
        admin/client.py
    """

    resource_name: str = "default"
    ssl_context: str | SSLContext | None = None
    options: MutableMapping[str, Any] = field(default_factory=dict)
    existing_resource: AIOKafkaAdminClient | str | None = None

    async def start(self) -> None:
        if self.existing_resource is not None:
            if isinstance(self.existing_resource, str):
                client = await get_resource(AIOKafkaAdminClient, self.existing_resource)
            else:
                client = self.existing_resource

            if self.existing_resource != self.resource_name:
                add_resource(client, self.resource_name)

            return

        if isinstance(self.ssl_context, str):
            self.options["ssl_context"] = await get_resource(SSLContext)
        elif self.ssl_context is not None:
            self.options["ssl_context"] = self.ssl_context

        client = AIOKafkaAdminClient(**self.options)
        await client.start()
        add_resource(client, self.resource_name, teardown_callback=client.close)
