import os

import pika
import requests
import datetime
import psycopg2
import time
import json

time.sleep(20)

credentials = pika.PlainCredentials('user', os.getenv('PIKA_PASSWORD'))
params = pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='crypto_prices', durable=True)

try:
    while True:
        req = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        if req.status_code == 200:
            cur_time = datetime.datetime.now().isoformat()
            data = req.json()
            payload = {'price': data['bitcoin']['usd'], 'timestamp': cur_time}
            msg = json.dumps(payload)
            channel.basic_publish(exchange='', routing_key='crypto_prices', body=msg, properties=pika.BasicProperties(delivery_mode=2))
            print('Sent to RabbitMQ!')
        else:
            print('Status code:', req.status_code)
        time.sleep(60)
except KeyboardInterrupt:
    print('Interrupted from keyboard')
except Exception as e:
    print(f'Exception: {e}')
finally:
    if connection.is_open and not connection.is_closed:
        connection.close()
        print('Connection closed')