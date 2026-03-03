import streamlit as st
import pandas as pd
import time
import altair as alt
from main import get_db_connection


st.set_page_config(page_title="Crypt", layout="wide")
st.title("🏭 Мониторинг биткоина")


def load_data():
    conn = get_db_connection()
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
    conn.close()
    return data


placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = load_data()
            last_price = data.iloc[0]['price']
            st.metric(label="Bitcoin Price (USD)", value=f"${last_price}")

            base = alt.Chart(data).encode(
                x=alt.X('created_at', title='Время'),
                y=alt.Y('price', title='Цена (USD)', scale=alt.Scale(zero=False, padding=1))
            )

            sma = alt.Chart(data).encode(
                x=alt.X('created_at', title='Время'),
                y=alt.Y('sma_10', title='Цена (USD)', scale=alt.Scale(zero=False, padding=1))
            )

            line = base.mark_line()
            line_sma = sma.mark_line(strokeDash=[5, 5], color='red', strokeWidth=0.5)

            points = base.mark_circle(size=500, opacity=0).encode(
                tooltip=['created_at', 'price']
            )

            final_chart = (line + points + line_sma).interactive()

            st.altair_chart(final_chart, use_container_width=True)

            st.dataframe(data.head(5))

        except Exception as e:
            st.error(e)
    time.sleep(60)
