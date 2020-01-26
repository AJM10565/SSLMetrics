FROM python:3

RUN mkdir -p /app

COPY Commits.py /app
COPY config.py /app
COPY Lines_Of_Code_And_Num_Of_Chars.py /app
COPY Master.py /app
COPY Number_Of_Issues.py /app
COPY Pull_Requests.py /app
COPY simple_cli.py /app

WORKDIR /app

RUN pip install numpy
RUN pip install pandas
RUN pip install requests

ENTRYPOINT python simple_cli.py $REPO