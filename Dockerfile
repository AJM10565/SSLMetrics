FROM python:3

ADD Commits.py /
ADD config.py /
ADD Lines_Of_Code_And_Num_Of_Chars.py /
ADD Master.py /
ADD Number_Of_Issues.py /
ADD Pull_Requests.py /
ADD simple_cli.py /

RUN pip install numpy
RUN pip install pandas
RUN pip install requests

ENTRYPOINT python simple_cli.py $REPO