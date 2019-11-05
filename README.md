# PSE - Picture Search Engine
Le Picture Search Engine est un méta-moteur de recherche d'image de qualité, open source.

# Objectif
L'objectif de ce projet est d'illustrer la mise en oeuvre de plusieurs technologies reconnues
 comme références dans leur domaine pour la réalisation d'une architecture sécurisée de type micro-services. 
 
 Ainsi on combine plusieurs technologies de pointes :
Pour le backend :
- le langage python, dont le nombre de bibliothéque garantit de pouvoir s'attaquer 
à tout type de domaine d'activité avec une prédisposition pour la data et l'intelligence artificiel
- le framework Flask d'architectures micro-services, dotés de nombreux 
plugin et apportant tout les avantages de ce type d'architecture
- l'usage d'une base de données open-source et NoSQL : MongoDB, calibré pour le big data,
- la containerisation via Docker garantissant la scalabilité de l'ensemble 
- l'utilisation d'une librairie de génération automatique de documentation pour l'API
- la sécurisation et le suivi (et l'éventuelle facturation) de l'usage de l'API via la gestion de token d'accès
- sécurisation du serveur via l'usage d'un certificat gratuit Let's Encrypt

Dans un second article, nous développerons le front-end:
- sous format d'une Progressive Web App multi-devices (vs un développement pour chaque plateforme),
- en typescript sur la dernière version du framework Angular,
- hébergé gratuitement grâce aux github page.

# Démonstration
Pour l'instant une interface minimal est accessible directement à l'adresse : https://pse.f80.fr
La documentation de l'API auto-générée par l'extension 
RestPlus est disponible sur : https://server.f80.fr:5800 



# Configuration du serveur
On décrit ici la configuration d'un serveur Linux. 

Toute l'installation va se faire en mode root ce qui n'est pas conseillé en environnement de production.
Ainsi le répertoire /root va héberger :
- un sous répertoire "data" destiné à stocker la base MondoDB
- un sous répertoire "certs" va recevoir une copie des certificats pour la connexion SSL

# Sécurisation du serveur
Notamment pour des raisons de référencement, l'usage de l'https est de plus en plus courrant. 
Cela implique que les api utilisées par les front-end sécurisés doivent également être sécurisé.
Dans cet exemple on va utilise des certificats Let's Encrypt.

Vous devez paramétrer le DNS de votre domaine pour le faire pointer vers
votre serveur. La procédure dépend de votre fournisseur de nom de domaine. 

Puis, sur le serveur qui hébergera l'api, on récupère "certbot" qui automatise la procédure
d'installation des certificats.

`apt-get -t jessie-backports install certbot`

puis on lance la fabrication des certificats :

`certbot certonly --standalone -d sub.domaine.com` 
en remplacant sub.domain.com par votre domaine. Si tout se passe bien, vous récupèrez
plusieurs fichiers dans le répertoire /etc/letsencrypt/live/<sub.domain.com>
Pour établir une connexion sécurisée avec Flask on utilise deux de ces fichiers :
"fullchain.pem" et "privkey.pem". 

Copiés dans le repertoire /root/certs ils seront accessible à notre serveur Flask :
`mkdir /root/certs && cp /etc/letsencrypt/live/sub.domain.com/* /root/certs`


# La base de données
## MongoDB
La base de données est utilsée comme cache pour stocker les réponses aux requêtes. 
On aurait pu utiliser des techniques plus légère ou des bases de données plus simple
que MongoDB mais l'objectif est d'illustrer l'usage d'une base moderne
 - opérationnelle pour le big data,
 - compatible avec l'<a href="https://www.datacamp.com/courses/introduction-to-using-mongodb-for-data-science-with-python">analyse de données</a>,
 - hautement scalable.

## Installation
Pour ne pas compliquer le processus d'installation, on choisie d'utiliser MongoDB
via son image "docker" : https://hub.docker.com/_/mongo

Si l'on part d'un serveur vierge, il faut commencer par installer Docker.
On trouve beaucoup de tutoriel suivant le système d'exploitation. Pour linux la commande suivante 
fonctionne sans intervention le plus souvent :

`curl -sSL get.docker.com | sh && systemctl start docker && systemctl enable docker`

Docker étant maintenant disponible l'installation de la base est particulierement simple :

`docker run --restart=always -v /root/mongodata:/data/db -d -p 27017-27019:27017-27019 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin_password mongo`

## Remarques
On aurait pû utiliser
- un autre port que le port standard : 27017 
- un autre couple (user / mot de passe) que (admin / admin_password)
- il est possible de se connecter via Mongo Compass pour visionner le contenu de la base

# Installation du serveur
Il est temps d'installer l'API. Là aussi, l'usage de Docker simplifie le déploiement à l'extrème. 
Ainsi, l'installation de notre serveur flask se fait par la commande :

`docker pull f80hub/picturesearchenginex86:latest && docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchenginex86 -d f80hub/picturesearchenginex86:latest localhost admin admin_password 5600 ssl`

grâce à cette commande on a :
- télécharger l'image picturesearchenginex86 fabriqué préalablement par la commande :
`docker build -t f80hub/picturesearchenginex86 . & docker push f80hub/picturesearchenginex86:latest`

- programmer le rédémarrage automatique de l'API lorsque le serveur redémarre,
- ouvert l'accès aux certificats pour permettre a Flask de sécuriser les transactions
- ouvert le port 5600 pour la communication a notre API
- enfin en terminant par "ssl" on configure l'API en mode sécurisé
(il est possible de lancer l'api en mode non sécurisé en enlenvant le paramèttre ssl. Dans ce cas, 
l'étape de fabrication des certificats n'est pas nécéssaire et l'api peut être jointe directement via
l'adresse IP du serveur) 

# Fichier de configuration
Dans une optique d'industrialisation, les paramètres du serveur sont regroupés 
dans une fichier YAML. <br>
Même si ce format est moin courant que json, on gagne en lisibilité
mais surtout YAML supporte les commentaires. 


# Fonctionnement de l'API
L'API est avant tout un prétexte pour illustrer l'architecture, pour autant elle pourrait servir de 
point de départ à un moteur de recherche d'images comme alternative à un google image.
Elle recoit en paramètre un mot clé et interroge deux plateformes de référencement de photo : PixaBay
et Unsplash. Les résultats sont concaténés et renvoyer au front-end sous forme d'une suite d'URL.

Préalablement, le Front-End envoie un user et un mot de passe et recoit en échange un token temporaire.
Cette mécanique est mise en oeuvre, sur le serveur, par la librarie Flask-JWT selon le principe 
des JSON Web Token (https://fr.wikipedia.org/wiki/JSON_Web_Token).

Dans l'exemple aucune interface d'enregistrement des développeurs n'est proposées. Pour aurtant 



# Remarque divers
Le code est abondamment documenté. Via RestPlus on génére
automatiquement une documentation pour notre API


# Front-end de tests
Pour tester notre API, nous avons développé une page HTML contenant un code minimal javascript
pour 
- demander un token d'utilisation de l'API
- utiliser le token obtenue pour interroger l'API
- afficher le résultat

Dans un prochain article, nous remplacerons ce fichier par une web application développée sur Angular 


# Références
De nombreux articles traitent des différentes briques 
impliquées dans le Picture Search Engine:
- La documentation de l'extension Flask-JWT : https://pythonhosted.org/Flask-JWT/
- La documentation de l'extension Flask-restplus : https://flask-restplus.readthedocs.io/en/stable/
- L'installation de MongoDB : https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/
 
