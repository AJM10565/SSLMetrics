FROM python:3.7
RUN mkdir -p /metrics_issues
COPY Code/ /app
WORKDIR /app
ENTRYPOINT ["python", "./SSLMetrics.py"]
