import os

import requests
import datetime
import psycopg2
import time

DB_CONFIG = {
    'host': 'db',
    'database': 'crypto_db',
    'user': 'admin',
    'password': os.getenv('DB_PASSWORD'),
}

def get_db_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print('Error while connecting to PostgreSQL', e)
        return None
    return connection

def create_table(connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS bitcoin_rates (id SERIAL PRIMARY KEY, price NUMERIC, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
            print('Table is ready!')
        except psycopg2.Error as e:
            print('Error while creating table', e)
    connection.commit()

def insert_data_to_table(connection, data: dict):
    with connection.cursor() as cursor:
        print(f"Bitcoin is {data['bitcoin']['usd']}$ at {datetime.datetime.now():%Y-%m-%d %H:%M:%S} UTC+0 time")

        cursor.execute('INSERT INTO bitcoin_rates (price) VALUES (%s)', (data['bitcoin']['usd'], ))
    connection.commit()


def main():
    print('Requests ver: ' + requests.__version__)
    print('It is running, waiting 10 seconds!')
    time.sleep(10)
    print('Time is up!')
    connection = get_db_connection()
    if connection is None:
        print('Connection failed')
        return
    create_table(connection)

    while True:
        req = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        if connection is None:
            connection = get_db_connection()
            if connection is None:
                print('Connection failed, retrying in 60 seconds...')
                time.sleep(60)
                continue
            else:
                print('Connection reestablished!')
        if req.status_code == 200:
            insert_data_to_table(connection, req.json())
        else:
            print(f'API request failed. Status code: {req.status_code}')
        time.sleep(60)

if __name__ == '__main__':
    main()
