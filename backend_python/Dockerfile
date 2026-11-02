# NEBians backend (Django + DRF, ASGI via daphne). Build from this directory:
#   docker build -t nebians-backend .
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential pkg-config default-libmysqlclient-dev libjpeg-dev zlib1g-dev ffmpeg curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN SECRET_KEY=build-only ADMIN_API_SALT=build-only CONSICA_BRIDGE_KEY=build-only DEBUG=True \
    python manage.py collectstatic --noinput >/dev/null 2>&1 || true

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/api/content/manifest/ || exit 1

# Apply migrations on boot, then serve.
CMD ["sh", "-c", "python manage.py migrate --noinput && daphne -b 0.0.0.0 -p 8000 nebians.asgi:application"]
