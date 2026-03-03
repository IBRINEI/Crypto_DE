import streamlit as st
import pandas as pd
import time
import altair as alt
import requests


st.set_page_config(page_title="Crypt", layout="wide")
st.title("🏭 Мониторинг биткоина")


def fetch_data_from_api():
    url = "http://api:8000/api/v1/prices/all"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['message'], columns=['created_at', 'price', 'sma_10'])
        if not df.empty and 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
        return df
    except Exception as e:
        st.error(f'Error in fetch_data_from_api, {e}')
        return pd.DataFrame()


placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            data = fetch_data_from_api()
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
            print(e)
            st.error(e)
    time.sleep(60)
