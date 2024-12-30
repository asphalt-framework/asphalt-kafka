from __future__ import annotations

import ssl

import pytest
from aiokafka import AIOKafkaProducer
from asphalt.core import Context, add_resource, get_resource_nowait, start_component

from asphalt.kafka import KafkaProducerComponent

pytestmark = pytest.mark.anyio


async def test_default_settings() -> None:
    component = KafkaProducerComponent()
    async with Context():
        await component.start()
        get_resource_nowait(AIOKafkaProducer)


@pytest.mark.parametrize(
    "lookup", [pytest.param(False, id="direct"), pytest.param(True, id="lookup")]
)
async def test_existing_resource(lookup: bool) -> None:
    producer = AIOKafkaProducer()
    async with Context():
        if lookup:
            add_resource(producer)

        await start_component(
            KafkaProducerComponent,
            {
                "existing_resource": "default" if lookup else producer,
                "resource_name": "alt",
            },
        )
        assert get_resource_nowait(AIOKafkaProducer, "alt") is producer


async def test_existing_resource_conflict() -> None:
    producer = AIOKafkaProducer()
    component = KafkaProducerComponent(existing_resource="default")
    async with Context():
        add_resource(producer)
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
            KafkaProducerComponent,
            {"ssl_context": "default" if lookup else ssl_context},
        )
        producer = get_resource_nowait(AIOKafkaProducer)
        assert producer.client._ssl_context is ssl_context
