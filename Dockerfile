FROM python:3.9-alpine

RUN mkdir /project
WORKDIR /project

COPY requirements.txt /project

RUN pip install --no-cache-dir -r requirements.txt

COPY . /project

RUN mkdir -p /var/log/gunicore

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

#sudo docker run --name booking --env-file .env booking
#sudo docker run --name reddis -p 6380:6379 redis
#sudo docker inspect redis -> IP 172.17.0.3