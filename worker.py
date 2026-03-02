import pika
import time
import json
import psycopg2

from main import get_db_connection

def insert_data_to_table(connection, data: dict):
    with connection.cursor() as cursor:
        price = data['price']
        timestamp = data['timestamp']
        print(f"Bitcoin is {price}$ at {timestamp} UTC+0 time")

        cursor.execute('INSERT INTO bitcoin_rates (price, created_at) VALUES (%s, %s)', (price, timestamp))
    connection.commit()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    data = json.loads(body)

    conn = get_db_connection()
    if conn:
        insert_data_to_table(conn, data)
        conn.close()

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

time.sleep(30)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=pika.PlainCredentials('user', 'password')))
channel = connection.channel()

channel.queue_declare(queue='crypto_prices', durable=True)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='crypto_prices', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press Ctrl+C')
channel.start_consuming()