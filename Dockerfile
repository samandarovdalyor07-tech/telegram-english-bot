# English Learning Bot — Docker image
FROM python:3.12-slim

WORKDIR /app

# Bog'liqliklarni o'rnatamiz (avval requirements — kesh uchun)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha kodini ko'chiramiz
COPY . .

# Botni ishga tushiramiz (polling)
CMD ["python", "bot.py"]
