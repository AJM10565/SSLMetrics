FROM python:3.7-alpine
RUN mkdir /metrics -p
COPY code/ /app
WORKDIR /app
ENTRYPOINT ["python", "./SSLMetrics.py"]
