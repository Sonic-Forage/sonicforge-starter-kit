FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8788
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8788/api/launch-status', timeout=5).read()"
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8788"]
