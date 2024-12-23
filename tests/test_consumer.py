from __future__ import annotations

import ssl

import pytest
from aiokafka import AIOKafkaConsumer

from asphalt.core import Context, add_resource, get_resource_nowait, start_component
from asphalt.kafka import KafkaConsumerComponent

pytestmark = pytest.mark.anyio


async def test_default_settings() -> None:
    component = KafkaConsumerComponent()
    async with Context():
        await component.start()
        get_resource_nowait(AIOKafkaConsumer)


@pytest.mark.parametrize(
    "lookup", [pytest.param(False, id="direct"), pytest.param(True, id="lookup")]
)
async def test_existing_resource(lookup: bool) -> None:
    consumer = AIOKafkaConsumer()
    async with Context():
        if lookup:
            add_resource(consumer)

        await start_component(
            KafkaConsumerComponent,
            {
                "existing_resource": "default" if lookup else consumer,
                "resource_name": "alt",
            },
        )
        assert get_resource_nowait(AIOKafkaConsumer, "alt") is consumer


async def test_existing_resource_conflict() -> None:
    consumer = AIOKafkaConsumer()
    component = KafkaConsumerComponent(existing_resource="default")
    async with Context():
        add_resource(consumer)
        await component.start()


@pytest.mark.parametrize(
    "lookup", [pytest.param(False, id="direct"), pytest.param(True, id="lookup")]
)
async def test_ssl_context(lookup: bool) -> None:
    ssl_context = ssl.create_default_context()
    async with Context():
        if lookup:
            add_resource(ssl_context)

        await start_component(
            KafkaConsumerComponent,
            {"ssl_context": "default" if lookup else ssl_context},
        )
        consumer = get_resource_nowait(AIOKafkaConsumer)
        assert consumer._client._ssl_context is ssl_context
