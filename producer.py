import os

import pika
import requests
import datetime
import time
import json

time.sleep(20)

credentials = pika.PlainCredentials('user', os.getenv('PIKA_PASSWORD'))
params = pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# channel.queue_declare(queue='crypto_prices', durable=True)

exchange_name = 'crypto_events'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

try:
    while True:
        try:
            req = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        except Exception as ee:
            print(f'Exception in get: {ee}')
            time.sleep(60)
            continue
        if req.status_code == 200:
            cur_time = datetime.datetime.now().isoformat()
            data = req.json()
            payload = {'price': data['bitcoin']['usd'], 'timestamp': cur_time}
            msg = json.dumps(payload)
            channel.basic_publish(exchange=exchange_name,
                                  routing_key='', body=msg, properties=pika.BasicProperties(delivery_mode=2))
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
