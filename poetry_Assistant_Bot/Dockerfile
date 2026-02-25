# Базовий образ контейнерва
FROM python:3.13.6-slim

# Встановимо робочу директорію всередині контейнера
WORKDIR /app

# Встановлюємо  poetry всередині контейнера
RUN pip install poetry

# Копіюємо файли конфігурації і встановлюємо залежності poetry  
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main
# Копіюємо інші файли в робочу директорію контейнера
COPY . .

# Запуск застосунка всередині контейнера
CMD ["python", "main.py"]