# Базовый образ с Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY app.py .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт (Shiny слушает на 8000 по умолчанию)
EXPOSE 8000

# Команда для запуска приложения
CMD ["shiny", "run", "--host", "0.0.0.0", "--port", "8000", "app.py"]
