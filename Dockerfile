# Используем базовый образ Python (как основу для чертежа)
FROM python:3.9-slim

# Копируем наш файл внутрь контейнера
COPY main.py /app/main.py

# Указываем рабочую папку
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Команда, которая запустится при старте контейнера
CMD ["python", "main.py"]