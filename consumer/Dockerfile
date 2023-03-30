FROM python:3.11

WORKDIR /home/
ADD consumer/requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD consumer consumer/
ADD utils utils/
RUN chmod +x consumer/start.sh

EXPOSE 8000/tcp