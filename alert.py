import pika
import json
import time
import os
import requests


def callback(ch, method, properties, body):
    price = json.loads(body)['price']
    if price < 60000:
        print('[x] Trying to send alert...')
        alarm_msg = f'ALARM test! BTC is {price}$'
        requests.get(
            f"https://api.telegram.org/bot{os.getenv('TG_TOKEN')}"
            f"/sendMessage?chat_id={os.getenv('TG_CHAT_ID')}&text={alarm_msg}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


time.sleep(60)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                               port=5672,
                                                               credentials=pika.PlainCredentials(
                                                                   'user', os.getenv('PIKA_PASSWORD')
                                                               )))
channel = connection.channel()

exchange_name = 'crypto_events'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

channel.queue_declare(queue='crypto_alert', exclusive=True)

channel.queue_bind(exchange=exchange_name, queue='crypto_alert')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='crypto_alert', on_message_callback=callback)

print(' [*] Waiting for messages to alert. To exit press Ctrl+C')
channel.start_consuming()
