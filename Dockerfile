FROM nginx:alpine

WORKDIR /bin/SRD

RUN mkdir /bin/SRD/settings
VOLUME /bin/SRD/settings

RUN mkdir /bin/SRD/temp
RUN mkdir /bin/SRD/templates

RUN apk update
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install --no-cache praw wget jinja2

COPY ./Cleanup.py /bin/SRD
COPY ./Scrape.py /bin/SRD
COPY ./style.css /bin/SRD
COPY ./templates/all.html /bin/SRD/templates/all.html
COPY ./nginx.conf /etc/nginx/nginx.conf

RUN ln -sf /bin/SRD/Scrape.py /etc/periodic/daily/Scrape.py

EXPOSE 80
