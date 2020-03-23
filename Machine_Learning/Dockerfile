FROM python:3.7
COPY code/ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./multiclass.py"]