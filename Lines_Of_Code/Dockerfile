FROM python:3.7
RUN mkdir -p /metrics
COPY Code/ /app
RUN pip install requests
WORKDIR /app
ENTRYPOINT ["python", "./SSLMetrics.py"]
