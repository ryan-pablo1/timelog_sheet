FROM ubuntu

# author
MAINTAINER ryanpablo1

# extra metadata
LABEL version="1.0"
LABEL description="time sheet log docker container"


# update sources list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev

ADD . /time_sheet_log
RUN pip3 install -r /time_sheet_log/requirements.txt

ENV PYTHONIOENCODING UTF-8
ENV PYTHONPATH /time_sheet_log:$PATH

CMD ["/bin/bash","-c","sleep 30s && python3 ./time_sheet_log/app.py"]
