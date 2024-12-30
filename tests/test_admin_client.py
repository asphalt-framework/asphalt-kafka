from __future__ import annotations

import ssl

import pytest
from aiokafka.admin import AIOKafkaAdminClient
from asphalt.core import Context, add_resource, get_resource_nowait, start_component

from asphalt.kafka import KafkaAdminComponent

pytestmark = pytest.mark.anyio


async def test_default_settings() -> None:
    component = KafkaAdminComponent()
    async with Context():
        await component.start()
        get_resource_nowait(AIOKafkaAdminClient)


@pytest.mark.parametrize(
    "lookup", [pytest.param(False, id="direct"), pytest.param(True, id="lookup")]
)
async def test_existing_resource(lookup: bool) -> None:
    client = AIOKafkaAdminClient()
    async with Context():
        if lookup:
            add_resource(client)

        await start_component(
            KafkaAdminComponent,
            {
                "existing_resource": "default" if lookup else client,
                "resource_name": "alt",
            },
        )
        assert get_resource_nowait(AIOKafkaAdminClient, "alt") is client


async def test_existing_resource_conflict() -> None:
    consumer = AIOKafkaAdminClient()
    component = KafkaAdminComponent(existing_resource="default")
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
            KafkaAdminComponent,
            {"ssl_context": "default" if lookup else ssl_context},
        )
        client = get_resource_nowait(AIOKafkaAdminClient)
        assert client._client._ssl_context is ssl_context
