# Базовый образ с Python
FROM python:3.12-slim

# Установим рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Копируем весь проект в контейнер
COPY . .
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8000 background:app & python main.py"]
