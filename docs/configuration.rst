Configuration
=============

.. highlight:: yaml
.. py:currentmodule:: asphalt.kafka

Configuring a Kafka producer
----------------------------

Here's a minimal configuration for starting a Kafka producer::

    components:
      kafka_producer:

This uses ``localhost:9092`` as the bootstrap server, and adds an
:class:`~aiokafka.AIOKafkaProducer` resource with the name ``default``.

Here's a somewhat more elaborate example::

    components:
      kafka_producer:
        resource_name: myproducer
        options:
          bootstrap_servers:
            - localhost:9092
            - kafka:9092

This uses the two servers as bootstrap servers, and adds the producer resource with the
name ``myproducer`` instead of ``default``.

You can pass through any keyword arguments to :class:`~aiokafka.AIOKafkaProducer` using
the ``options`` parameter.

Configuring a Kafka consumer
----------------------------

Here's a minimal configuration for starting a Kafka consumer::

    components:
      kafka_consumer:

This uses ``localhost:9092`` as the bootstrap server, and adds an
:class:`~aiokafka.AIOKafkaConsumer` resource with the name ``default``. This consumer
will not have any initial topic subscriptions.

Here's a somewhat more elaborate example::

    components:
      kafka_consumer:
        resource_name: myconsumer
        topics:
          - mycompany.foo.bar
          - another.topic
        options:
          bootstrap_servers:
            - localhost:9092
            - kafka:9092

This uses the two servers as bootstrap servers, and adds the consumer resource with the
name ``myconsumer`` instead of ``default``. It will also subscribe to the topics
``mycompany.foo.bar`` and ``another.topic`` at start.

You can pass through any keyword arguments to :class:`~aiokafka.AIOKafkaConsumer` using
the ``options`` parameter.

Configuring a Kafka admin client
--------------------------------

Here's a minimal configuration for starting a Kafka admin client::

    components:
      kafka_admin:

This uses ``localhost:9092`` as the bootstrap server, and adds an
AIOKafkaAdminClient_ resource with the name ``default``.

Here's a somewhat more elaborate example::

    components:
      kafka_admin:
        resource_name: myadmin
        options:
          bootstrap_servers:
            - localhost:9092
            - kafka:9092

This uses the two servers as bootstrap servers, and adds the admin client resource with
the name ``myadmin`` instead of ``default``.

You can pass through any keyword arguments to AIOKafkaAdminClient_ using the
``options`` parameter.

.. warning:: The aiokafka admin client API is currently experimental, and subject to
    changes even between patch releases.

.. _AIOKafkaAdminClient: https://github.com/aio-libs/aiokafka/blob/master/aiokafka/\
    admin/client.py

Using external SSL context resources
------------------------------------

If you wish the share an :class:`~ssl.SSLContext` resource from elsewhere in your
application, you can specify the resource name as the ``ssl_context`` parameter::

    components:
      kafka_producer:
        ssl_context: default

This will cause the component to wait until an :class:`~ssl.SSLContext` resource with
the name ``default`` is available, and then pass it to the producer's constructor.

.. note:: If ``ssl_context`` is also passed in ``options``, that value will be
    overwritten.

Reusing Kafka resources from elsewhere in the application
---------------------------------------------------------

It's possible to configure each Kafka component to forego the setup of its particular
resource, and instead use an existing resource. This may make sense in at least two
different scenarios:

#. You are running a test suite, and want to set up session-wide or module-wide Kafka
   resources in order to cut down the run time of the suite
#. You have multiple Kafka components on more than one level in the component hierarchy,
   and would like to share them for the purposes of efficiency, or any another reason.

To do this, simply pass either a resource name, or the corresponding object in the
``existing_resource`` parameter::

    components:
      kafka_consumer:
        existing_resource: default
