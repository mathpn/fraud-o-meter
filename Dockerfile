FROM python:3.11

WORKDIR /home/
ADD requirements.txt requirements.txt
ADD start.sh start.sh
RUN chmod +x start.sh
RUN pip install -r requirements.txt

COPY app/ app/

EXPOSE 8000/tcp