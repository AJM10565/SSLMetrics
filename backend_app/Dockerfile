FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install flask
RUN pip install flask-cors
EXPOSE 5000
CMD python ./app.py