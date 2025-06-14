FROM python:3.11-slim

WORKDIR /code

COPY . .

RUN mkdir -p /code/shared_data

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
