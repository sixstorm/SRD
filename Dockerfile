FROM nginx:alpine

WORKDIR /bin/SRD

RUN mkdir /bin/SRD/settings
VOLUME /bin/SRD/settings

RUN mkdir /bin/SRD/temp
RUN mkdir /bin/SRD/templates

RUN apk add --no-cache tzdata
ENV TZ=America/Chicago

RUN apk update
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools praw wget jinja2

COPY ./Scrape.py /bin/SRD
COPY ./style.css /bin/SRD
COPY ./templates/all.html /bin/SRD/templates/all.html
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./scripts/run.sh /bin/SRD/scripts/run.sh

COPY ./scripts/startup.sh /docker-entrypoint.d
RUN chmod a+x /docker-entrypoint.d/startup.sh
COPY ./scripts/run.sh /etc/periodic/hourly/runSRD
RUN ["chmod","-R","a+wx","/etc/periodic/hourly"]
# COPY ./scripts/run.sh /etc/periodic/1min/runSRD
# RUN ["chmod","-R","a+wx","/etc/periodic/1min"]
# RUN echo "* * * * * run-parts /etc/periodic/1min" >> /etc/crontabs/root

EXPOSE 80