# Picture Seach Engine
Moteur de recherche d'images

# Objectif
L'objectif de cet article est d'illustrer l'usage des dernières technologies pour la réalisation d'une architecture typique client-serveur de type micro-services, sécurisée. Ainsi elle utilise 
les technologies les plus en pointes actuellement :
- fonctionnement en mode client serveur reposant sur des API reste
- usage d'une base de données NoSQL : MongoDB
- serveur scalable via les techniques de containerisation de Docker
- serveur développé dans l'un des languages qui monte, python
- utilisation d'une librairie de génération automatique de documentation pour l'API
- sécurisation de l'API via génération de token
- sécurisation du serveur via l'usage d'un certificat Let's Encrypt

Le front-end est 
- développé en typescript sur le framework Angular
- hébergé gratuitement grâce aux github page

# Démonstration
Le front-end est accessible directement à l'adresse : https://pse.f80.fr
La documentation de l'API générée par l'extension RestPlus se trouve ici : 


# Le code
Le code est abondamment commenté. 


# Sécurisation du serveur
Dans cet exemple on va utilise des certificats Let's Encrypt.

tout d'abord vous devez paramétrer le DNS de votre domaine pour le faire pointer vers
votre serveur. La procédure dépend de votre fournisseur de nom de domaine. Par exemple, chez
1 and 1 elle est expliquée ici. 
Puis, sur le serveur, on récupère certbot qui automatise la procédure
d'installation des certificats.

`apt-get -t jessie-backports install certbot`

l'installation des certificats s'obtient ainsi :

`certbot certonly --standalone -d sub.domaine.com` 
en remplacant sub.domain.com par votre domaine

pour établir une connexion sécurisée Flask utilise deux fichiers :
fullchain.pem et privkey.pem produit par certbot. On les places
dans le repertoire /root/certs qui est visible depuis l'image docker
du serveur par la commande 

`mkdir /root/certs && cp /etc/letsencrypt/live/sub.domain.com/* /root/certs`


# Installation de docker
Dans le projet on utilise un serveur Linux 
pour héberger nos images Docker, et l'on se place dans une configuration root
(ce qui n'est clairement pas conseillé en environnement de production)

L'installation de docker dépend de l'OS mais dans beaucoup de cas, 
il suffit d'exécuter :

`sudo curl -sSL get.docker.com | sh && systemctl enable docker && systemctl start docker`


# La base de données
La base de données est utilsée comme cache pour stocker les réponses aux requêtes. 
On aurait pu utiliser des techniques plus légère ou des bases de données plus simple
que MongoDB mais l'objectif est d'illustrer l'usage d'une base moderne
 - opérationnelle pour le big data,
 - compatible avec l'<a href="https://www.datacamp.com/courses/introduction-to-using-mongodb-for-data-science-with-python">analyse de données</a>,
 - hautement scalable.

Via docker, on peut avoir une installation de la base particulierement simple à mettre en
oeuvre :

`docker run --restart=always -v /root/mongodata:/data/db -d -p 27017:27017 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin_password mongo`

On aurait pû utiliser
- un autre port que le port standard : 27017 
- un autre couple (user / mot de passe) que (admin / admin_password)

# Installation du serveur


# Références
De nombreux articles traitent des différentes briques 
impliquées dans le Picture Search Engine:
- La documentation de l'extension Flask-JWT : https://pythonhosted.org/Flask-JWT/
- La documentation de l'extension Flask-restplus : https://flask-restplus.readthedocs.io/en/stable/
- L'installation de MongoDB : https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/
 
