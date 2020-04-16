FROM python:3.7
RUN mkdir -p /metrics
COPY Code/ /app
WORKDIR /app
ENTRYPOINT ["python", "./SSLMetrics.py"]
