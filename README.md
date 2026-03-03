\# Crypto DE



Event-driven microservices pipeline for tracking cryptocurrency prices and generating alerts. Built to practice decoupled architecture, message brokers, caching, and CI/CD.



\## Tech Stack

\* \*\*Backend:\*\* Python 3.9, FastAPI

\* \*\*Data Layer:\*\* PostgreSQL (Persistence), Redis (Caching)

\* \*\*Message Broker:\*\* RabbitMQ (Fanout exchanges)

\* \*\*Frontend:\*\* Streamlit

\* \*\*DevOps:\*\* Docker Compose, GitHub Actions, Pytest, Flake8



\## Architecture





\* \*\*Miner (Producer):\*\* Fetches BTC price, publishes to RabbitMQ exchange (`crypto\_events`).

\* \*\*Worker (Consumer):\*\* Handles DB bootstrapping, reads from queue, persists records to PostgreSQL.

\* \*\*Alerter (Consumer):\*\* Evaluates stream in real-time. Triggers Telegram alerts on threshold breach.

\* \*\*API Gateway:\*\* Serves historical data. Calculates SMA-10 via SQL window functions. Caches responses in Redis (60s TTL) to minimize DB read operations.

\* \*\*Dashboard:\*\* Decoupled frontend visualizing data fetched exclusively via REST API.



\## Quickstart



1\. \*\*Clone and configure:\*\*

&nbsp;  ```bash

&nbsp;  git clone \[https://github.com/YOUR\_USERNAME/crypto\_factory.git](https://github.com/YOUR\_USERNAME/crypto\_factory.git)

&nbsp;  cd crypto\_factory

&nbsp;  ```

2\. \*\*Create `.env`:\*\*

```TOML

DB\_PASSWORD=your\_password

PIKA\_PASSWORD=your\_password

TG\_TOKEN=your\_telegram\_token # Optional

TG\_CHAT\_ID=your\_chat\_id      # Optional

```

3\. \*\*Run:\*\*

```bash

docker compose up -d --build

```



\## Services



\- \*\*Dashboard:\*\* http://localhost:8501

\- \*\*API Docs (Swagger):\*\* http://localhost:8080/docs

\- \*\*RabbitMQ UI:\*\* http://localhost:15672



\## CI / Testing



GitHub Actions pipeline runs on every `push`. It provisions an ephemeral Docker environment, executes integration tests (`pytest`), and checks syntax (`flake8`).



Run tests locally:

```bash

docker compose exec api pytest

```



