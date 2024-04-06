from typing import Any

from ._admin import KafkaAdminComponent as KafkaAdminComponent
from ._consumer import KafkaConsumerComponent as KafkaConsumerComponent
from ._producer import KafkaProducerComponent as KafkaProducerComponent

# Re-export imports so they look like they live directly in this package
key: str
value: Any
for key, value in list(locals().items()):
    if getattr(value, "__module__", "").startswith(f"{__name__}."):
        value.__module__ = __name__
