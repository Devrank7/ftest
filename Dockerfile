# Базовый образ с Python
FROM python:3.12-slim

# Установим рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Укажем команду для запуска бота
CMD ["python", "main.py"]