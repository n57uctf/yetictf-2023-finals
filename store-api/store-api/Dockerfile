FROM python:3.9

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src
RUN pip3 install -r requirements.txt
COPY . /src

ENTRYPOINT ["python3", "setup.py"]


