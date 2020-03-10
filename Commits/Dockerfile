FROM python:3.7
RUN mkdir -p /metrics_commits
COPY Code/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./SSLMetrics.py"]
