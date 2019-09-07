FROM ubuntu:latest
MAINTAINER alisson.copyleft@gmail.com

RUN apt clean && apt update 
RUN apt install libmysqlclient-dev python3 python3-pip -y
COPY src /opt/
RUN python3 -m pip install /opt/requirements.txt

EXPOSE 5000

CMD ["python3","/opt/app.py"]