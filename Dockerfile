FROM python:3.9-slim

EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "run.sh"]