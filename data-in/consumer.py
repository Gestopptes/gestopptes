import pika, json
from typing import List
from pika.channel import Channel
from pika import BasicProperties
from pika.spec import Basic
import config

class Item(object):

    def __init__(self, description: str, price: float, quantity: float):
        self.description = description
        self.price = price
        self.quantity = quantity

ListItem = List[Item]

class Order(object):

    def __init__(self, total : float, items: ListItem):
        self.total = total
        self.items = items

def consumer(ch: Channel, method: Basic.Deliver, properties: BasicProperties, body):
    print("Consumer")
    print(f'body={body}')
    print(f'method={method}')
    print(f'properties={properties}')
    try:
        dados = json.loads(body)
        order = Order(total=dados["total"], items=[Item(description=i["description"], price=i["price"], quantity=i["quantity"]) for i in dados["items"]])
        print(f"{order}")
        print(f" [x] Message successfully received!")
    except Exception as ex:
        props = pika.BasicProperties(
            delivery_mode = 2,
            headers={"exception": f"{ex}"}
        )
        ch.basic_publish(config.dlq_name, config.dlq_name, body=body, properties=props)
    finally:
        ch.basic_ack(delivery_tag = method.delivery_tag)


connection = None
try:
    channel, connection = config.get_channel()
    ret = channel.basic_consume(queue=config.queue_name, auto_ack=False, on_message_callback=consumer)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except Exception as ex:
    print(f" [x] Excepton: {type(ex)}:{ex}")
finally:
    connection.close()