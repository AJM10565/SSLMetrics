FROM python:3.7-alpine
COPY code/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./app.py"]