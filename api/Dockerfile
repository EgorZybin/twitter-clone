FROM python:3.11

RUN apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /api

COPY . .

RUN pip install --no-cache-dir -r api/requirements.txt

CMD ["uvicorn", "api.routes:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
