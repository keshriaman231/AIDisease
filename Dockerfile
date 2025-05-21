# Dockerfile
FROM python:3.11

WORKDIR /app
COPY backend/ .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PORT=5000
EXPOSE 5000

CMD ["python", "app.py"]
