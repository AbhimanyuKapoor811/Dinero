FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/app.py

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/app.py"]
