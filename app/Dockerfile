FROM python:3.11

WORKDIR /home/
ADD app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD app app/
ADD utils utils/
RUN chmod +x app/start.sh

EXPOSE 8000/tcp