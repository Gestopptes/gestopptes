import pika
from pika.exchange_type import ExchangeType

queue_name = 'queue_estoque_novo_pedido'
dlq_name = 'dlq_estoque_novo_pedido'

username = 'user'
password = 'password'
host = '100.66.129.30'
port = 5672

def get_channel():
    auth = pika.PlainCredentials(username=username, password=password)
    params = pika.ConnectionParameters(host, port, '/', auth)
    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.exchange_declare(exchange=dlq_name, exchange_type=ExchangeType.topic)
    channel.queue_declare(queue=queue_name, durable=True, arguments={
        "x-dead-letter-exchange": dlq_name,
        "x-dead-letter-routing-key": dlq_name
    })
    channel.queue_declare(queue=dlq_name, durable=True)
    channel.queue_bind(dlq_name, dlq_name, dlq_name)
    return (channel, connection)