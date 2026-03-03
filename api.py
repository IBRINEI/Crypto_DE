from fastapi import FastAPI
import pandas as pd

from main import get_db_connection


app = FastAPI(
    title="🏭 Crypto Factory API",
    description="Публичный API для получения данных о цене Биткоина"
)

print('API Started!')


@app.get("/api/v1/prices/latest")
def get_latest_prices():
    """
    Возвращает последние 10 записей курса биткоина.
    """
    conn = get_db_connection()
    if not conn:
        return {"error": "No connection to DB"}
    query = '''
    SELECT created_at, price
    FROM bitcoin_rates
    ORDER BY created_at DESC
    LIMIT 10'''
    data = pd.read_sql_query(query, conn)
    conn.close()
    # dict_data = list(data.to_dict().values())
    dict_data = dict(zip(data['created_at'], data['price']))
    print('API returns: ', dict_data)
    return {"message": dict_data}


@app.get("/api/v1/prices/all")
def get_price_history():
    """
    Возвращает всю историю записей курса биткоина + SMA.
    """
    conn = get_db_connection()
    if not conn:
        return {"error": "No connection to DB"}
    try:
        query = '''SELECT 
        created_at,
        price,
        AVG(price) OVER (
            ORDER BY created_at 
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ) as sma_10
        FROM bitcoin_rates
        ORDER BY created_at DESC'''
        data = pd.read_sql_query(query, conn)
        msg = data.to_dict('records')
        print('API returns history!')
        return {'message': msg}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
