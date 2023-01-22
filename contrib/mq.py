from aio_pika import connect
from settings import rabbitmq
from aio_pika.patterns import RPC


async def sendMessageMQ(queue, message):
    try:
        connection = await connect(
            "amqp://{}:{}@{}/".format(rabbitmq.get('user'), rabbitmq.get('pass'), rabbitmq.get('host')), client_properties={"connection_name": "caller"}, )
        async with connection:
            channel = await connection.channel()
            rpc = await RPC.create(channel)
            result = await rpc.call(method_name=queue, kwargs=message, expiration=15)
            return result
    except Exception as e:
        raise str(e)
