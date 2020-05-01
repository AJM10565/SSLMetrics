FROM python:3.7
RUN mkdir -p /metrics
COPY Code/ /app
WORKDIR /app
RUN sudo apk add cloc
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./SSLMetrics.py"]
