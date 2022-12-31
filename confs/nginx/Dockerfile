FROM nginx:1.19.0-alpine

COPY booking.conf /etc/nginx/conf.d/

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /project
WORKDIR /project