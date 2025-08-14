FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create non-root user
RUN useradd -m appuser
USER appuser

COPY . /app

# Expose port
EXPOSE 8000

# Start with gunicorn+uvicorn workers for prod hardening
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
