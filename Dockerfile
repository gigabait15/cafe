FROM python:3.10-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файла с зависимостями
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов проекта в контейнер
COPY . .

# Открытие порта для приложения
EXPOSE 8000

# Запуск приложения с указанием хоста
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
