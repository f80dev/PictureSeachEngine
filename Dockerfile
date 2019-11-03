#installation et démarrage de docker
#sudo curl -sSL get.docker.com | sh && systemctl start docker

#x86
#docker build -t f80hub/picturesearchenginex86 . & docker push f80hub/picturesearchenginex86:latest
#docker rm -f picturesearchenginex86 && docker pull f80hub/picturesearchenginex86:latest && docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchenginex86 -d f80hub/picturesearchenginex86:latest server.f80.fr 5600 ssl

#Après renouvellement les certificats doivent être copié dans le répertoire /root/certs
#cp /etc/letsencrypt/live/server.f80.fr/* /root/certs

FROM jfloff/alpine-python

#Installation

RUN apk update
RUN apk --update add python

RUN pip3 install --upgrade pip

#Installation des librairies complémentaires
RUN pip3 -v install pymongo
RUN pip3 -v install Flask
RUN pip3 -v install flask-restplus
RUN pip3 -v install Flask-JWT
RUN pip3 -v install Flask-Cors
RUN pip3 -v install requests
RUN apk add py3-openssl

#RUN apk --no-cache --update-cache add python3-dev

RUN mkdir /app
#RUN mkdir /app/static


#Ouverture du volumes contenants les certificats
VOLUME /certs

#Installation de l'application dans l'image Docker
WORKDIR /app
COPY . /app

ENTRYPOINT ["python", "app.py"]
