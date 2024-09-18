import pika
import json

def publish_order_request(customer_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange for orders
    channel.exchange_declare(exchange='order_exchange', exchange_type='topic')

    # Prepare the message with the customer ID
    message = {
        'customer_id': customer_id
    }

    # Publish the message to RabbitMQ
    channel.basic_publish(
        exchange='order_exchange',
        routing_key='customer.order.request',
        body=json.dumps(message)
    )

    print(f"Published order request for customer {customer_id}")
    connection.close()
