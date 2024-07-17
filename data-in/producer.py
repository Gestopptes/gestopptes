import pika
import config

dados = """{
    "total": 462,
    "items":[
        {"description":"Pelo", "price":0.50, "quantity":60},
        {"description":"Chumbinho", "price":4.80, "quantity":90}
    ]
}"""

channel, connection = config.get_channel()
channel.basic_publish(exchange='', routing_key=config.queue_name, body=dados)
print(f" [x] Sent {dados}")
connection.close()