#install docker
#sudo curl -sSL get.docker.com | sh

#x86
#docker build -t f80hub/picturesearchengine . & docker push f80hub/picturesearchengine:latest
#docker rm -f picturesearchengine && docker pull f80hub/picturesearchengine:latest && docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchengine -d f80hub/picturesearchengine:latest ssl
#Après renouvellement les certificats doivent être copié dans le répertoire /root/certs
#cp /etc/letsencrypt/live/server.f80.fr/* /root/certs

FROM jfloff/alpine-python

#Installation

RUN apk update
RUN apk --update add python

RUN pip3 install --upgrade pip

RUN pip3 -v install Flask
RUN pip3 -v install flask-restplus
RUN pip3 -v install Flask-JWT
RUN pip3 -v install Flask-Cors
RUN pip3 -v install requests
RUN apk add py3-openssl

RUN apk --no-cache --update-cache add python3-dev

RUN mkdir /app
RUN mkdir /app/static

WORKDIR /app

VOLUME /certs

COPY . /app

ENTRYPOINT ["python", "app.py"]
