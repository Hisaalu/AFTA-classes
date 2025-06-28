<<<<<<< HEAD
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./main.py /code/


CMD ["fastapi", "run", "main.py", "--port", "80"]
=======
FROM python:3.11-slim

WORKDIR /code

COPY . .

RUN mkdir -p /code/shared_data

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 9dd52a35cadcf3f1bada7cbc85e3999839bf290b
