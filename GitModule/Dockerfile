FROM python:3.7
RUN mkdir -p /metrics
WORKDIR /bin
COPY Code/ /app
WORKDIR /app
RUN git checkout https://github.com/AlDanial/cloc
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./SSLMetrics.py"]
