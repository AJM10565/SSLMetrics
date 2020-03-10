FROM python:3.7-alpine
RUN mkdir -p /metrics
COPY Code/ /app
WORKDIR /app
ENTRYPOINT ["python", "./SSLMetrics.py"]
