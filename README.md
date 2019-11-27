# PSE - Picture Search Engine
Le Picture Search Engine est un méta-moteur, 
open source, de recherche de photos de qualitées.

# Objectif du projet
L'objectif de cet article est de combiner plusieurs technologies éprouvées et reconnues pour 
illustrer la mise en oeuvre d'une architecture client/serveur de type micro-services.

La solution, peut se décompose en 2 briques : 
 
## Le backend
- est développé en python. Un langage moderne dont le nombre de bibliothéque garantit 
de pouvoir s'attaquer à tout type de domaine d'activité 
avec une prédisposition pour la data et l'intelligence artificiel,
- l'API repose sur le framework d'architectures micro-services Flask. Il est dotés de nombreux 
plugin pour faciliter la réalisation d'APIs performantes et sécurisées 
- l'usage d'une base de données open-source et NoSQL : MongoDB, calibrée pour le big data avec une garantie
de performence et de scalabilité.
- la containerisation via Docker simplifiant le déploiement tout en permettant la scalabilité de l'ensemble 
via des outils comme kubernetes,
- l'utilisation du plugin Flask-Restplus permet de générer automatiquement une documentation de l'API 
et un outil de test performant et simple,
- la sécurisation, le suivi et l'éventuelle facturation de l'usage de l'API 
via la gestion de token d'accès,
- la sécurisation du serveur via l'usage d'un certificat SSL Let's Encrypt

## Le front-end 

pour l'instant, sous forme d'une page HTML minimale pour utiliser l'API et 
d'une interface d'interrogation via Swagger UI, 
il doit être porté dans un second temps vers un front-end multi-device 
- sous format Progressive Web App sur Angular 8 / Angular Material,
- en typescript,
- hébergé gratuitement sur les "github page".

L'ensemble est très certainement optimisable, mais l'idée est de proposer une architecture 
de base pour simplifier sa reprise et adapatation à d'autres problématiques.

# Configuration du serveur de l'API
A priori l'api peut être installée sur n'importe quel type d'OS supportant Python. 
Dans cet exemple, on utilise une distribution Linux : Fedora (v29)

Pour faire simple, toute l'installation va se faire en mode root 
ce qui n'est pas conseillé en environnement de production.
Ainsi le répertoire /root va héberger :
- un sous-répertoire "/mongodata" destiné à stocker la base MongoDB,
- un sous-répertoire "/certs" recevant une copie des certificats pour la connexion SSL,

Nous allons principalement utilisé des images sous Docker 
pour installer les différentes composantes du serveur. il faut 
donc commencer par installer le fameux gestionnaire de containers.

On trouve beaucoup de tutoriel sur l'installation de Docker suivant le système d'exploitation. 
Pour linux, après s'être connecté en mode root, la commande suivante 
fonctionne le plus souvent sans intervention :

`curl -sSL get.docker.com | sh`
 
puis on démarre le démon et on l'installe pour un démarage automatique :

`systemctl start docker && systemctl enable docker`

Normalement docker est maintenant installé. 
On peut le vérifier par la commande `docker ps` qui affiche les images docker présentent.

# Sécurisation
L'étape suivante consiste à 
- sécuriser le serveur pour permettre un appel de notre API via "https"
- authentifier les utilisateurs de l'API par l'usage d'un token.

## sécurisation du serveur : mise en place des certificats SSL
L'usage de l'https pour héberger les sites est de plus en plus courant. 
Cela implique que les api utilisées par les front-end sécurisés doivent 
également utiliser le protocol 'https'. 
Pour autant, on peut faire fonctionner notre API sur un serveur non sécurisé. 
Dans ce cas, vous pouvez directement passez au chapitre suivant. 

l'usage 'https' nécessite 
 - la mise en place de certificats SSL,
 - l'interrogation du serveur via un nom de domaine. 
  
Dans cet exemple on utilise des certificats "Let's Encrypt".

Vous devez paramétrer le DNS de votre domaine 
pour le faire pointer vers l'adresse IP de
votre serveur. Le principe consiste 
à ajouter un "enregistrement A" au DNS du nom de domain.

La procédure pas à pas dépend de votre fournisseur 
de nom de domaine et est souvent détaillée dans les FAQ.
On peut également consulter les sites suivants :  
- https://blog.youdot.io/fr/4-types-enregistrements-dns-a-connaitre/
- https://docs.icodia.com/general/zones-dns

Il faut, maintenant, fabriquer les certificats.
Sur le serveur qui hébergera l'api, 
on installe "certbot" en suivant les instructions du site: 
https://certbot.eff.org/instructions

Cet outil automatise la procédure d'installation des certificats 
via la commande :
`certbot certonly --standalone -d sub.domaine.com` 
en remplacant sub.domain.com par votre domaine. 

Lors de son exécution, Let's Encrypt va chercher à joindre votre serveur
via le port 80. Il faut donc s'assurer que l'accès est possible depuis l'extérieur (en particulier
en regardant du côté des firewall et/ou des redirection de ports)

Si tout se passe bien, vous récupèrez
plusieurs fichiers dans le répertoire /etc/letsencrypt/live/<sub.domain.com>

Pour établir une connexion sécurisée, Flask utilise deux fichiers 
produit par certbot : 
- "fullchain.pem" : contenant l'ensemble des certificats
- "privkey.pem" :  La clé privée de votre certificat. A garder confidentielle en toutes circonstances 
                   et à ne communiquer à personne quel que soit le prétexte.

Ils faut rendre ces fichiers visibles à l'image docker de notre serveur
On va donc les copier dans le repertoire /root/certs 
que l'on ouvrira à l'image via la commande "VOLUME"

`mkdir /root/certs && cp /etc/letsencrypt/live/sub.domain.com/* /root/certs`

Théoriquement, cette manipulation doit être réalisé chaque fois que l'on met
à jour les certificats. Let's encrypt impose le renouvellement des certificats tous les 3 mois.
La procédure est automatisable via (voir https://certbot.eff.org/docs/using.html?highlight=renew#renewing-certificates)
met il faut également automatiser la copie. 
Vous pouvez également utiliser un certificat, 
souvent fourni gratuitement par le fournisseur
du nom de domaine.


## Sécurisation de l'api par gestion de token
Flask permet l'ajout d'une couche de sécurité directement au niveau
de l'API via l'usage de token pour identifier les utilisateurs (développeurs).

Pour aller plus loin, en particulier si l'on souhaite commercialiser l'api, 
il faudrat envisager l'installation de solution de gestion d'API (API management). On trouve plusieurs produits pour faire cela
Certaines sont propriétaires, d'autres Open source 
comme le détaille cet article : 
<a href="https://techbeacon.com/app-dev-testing/you-need-api-management-help-11-open-source-tools-consider">11 open-source tools to consider</a>

Dans notre cas, nous allons rester sur une gestion du token intégrer au serveur.

La procédure d'obtention du token est réduite à sa plus simple expression, puisqu'il suffit
d'appeler l'API "/auth" qui se charge d'enregistrer un username / password 
dans la base de données et de retourner 
le token d'authentification. 

Dans une version plus industrialisée, on pourrait par exemple exiger un email comme
nom d'utilisateur. A chaque appel, l'api se connectera à la base pour retrouver
le compte via le token. Ainsi il est possible de vérifier que le développeur à
les droits pour utiliser notre API.

Une autre option pour, non mise en oeuvre ici, consiste à n'authoriser les appels
à l'API que depuis une adresse spécifique.

# La base de données
L'objectif de l'article est également de montrer un exemple d'implémentation d'une 
base de données moderne et courrante dans l'univers Python. Pour cette raison on installe MongoDB
via la librairie "pymongo" (https://api.mongodb.com/python/current/)

## Installation
On doit commencer par installer un instance de MongoDB sur le serveur.
Pour ne pas compliquer le processus d'installation, on choisie d'utiliser
l'image "docker" : https://hub.docker.com/_/mongo

Rien de plus simple, puisqu'une seule commande suffit :
`docker run --restart=always -v /root/mongodata:/data/db -d -p 27017-27019:27017-27019 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin_password mongo`

## Remarques
Il faut retenir que 
- l'écriture dans la base depuis l'API se fera avec le user/mot de passe : admin/admin_password. 
Ce couple sera utilisé dans l'API pour se connecter à la base
- la base n'est pas nécéssairement installée sur le même serveur que l'API
- le port de connexion à la base de donnée est celui par défaut, le 27017. Dans une optique industrielle, il peut être souhaitable
de le modifier 
- il est possible de se connecter via l'outil Mongo Compass (https://www.mongodb.com/products/compass) 
pour visionner le contenu notre base depuis n'importe quel
poste dès lors qu'on utilise bien les paramètres de connexion ci-dessus

## Usage
La librairie Python utilisée pour interragir avec MongoDB doit être installée. 
MongoDB est une base orientée document.

Chaque enregistrement est donc un dictionnaire python (type dict). Dans notre API, on utilise 2 types d'objets:
- l'objet user est un simple dictionnaire (user,mot de passe)
- un objet log_entrie contient chaque appel aux API : le token, la date de l'appel et les paramètres


# Logique de fonctionnement de l'API
## Principe
L'API est avant tout un prétexte pour illustrer l'architecture, pour autant elle pourrait servir de 
point de départ à un moteur de recherche d'images comme alternative à un google image.
Elle recoit en paramètre un mot clé et interroge deux plateformes de référencement de photos : PixaBay
et Unsplash. Ces deux plateformes exposent des API via leur portail développeurs.

Les résultats sont concaténés et renvoyés au front-end sous forme d'une suite d'URL.

REST repose sur 4 actions possibles sur les ressources manipulés. GET pour les récupérer, POST pour les ajouter,
PUT pour mettre a jour une ressource existente, enfin DELETE pour supprimer une ressource.
Plus d'info sur REST se trouve ici : https://blog.nicolashachet.com/niveaux/confirme/larchitecture-rest-expliquee-en-5-regles/
La librairie RestPlus, implémente l'architecture REST sur flask. 
Elle consiste à représenter les ressources (au sens REST) par des classes Python. les verbes, en particulier GET, celui qu'on
va utiliser, est implémenté par une méthode du même nom de la classe représentant la ressource.


## Fichier de configuration
Dans une optique d'industrialisation, les paramètres du serveur sont regroupés 
dans une fichier YAML. <br>
Même si ce format est moins courant que json, on gagne en lisibilité 
notamment via la possibilité d'ajouter des commentaires.

Il contient les paramètres nécéssaires au fonctionnement du serveur, en particulier :
- le point de terminaison (endpoint) de notre API
- les paramètres d'accès aux plateformes de photos.

Ce fichier doit resté confidentiel.
On aurait pû y ajouter les paramètres d'accès à la base mais ces paramètres sont passés
dans la commande docker d'installation du serveur (voir rubrique sur l'installation)

##Principale fonction mise en oeuvre
Le code est assez court et abondamment commenté, donc facilement adaptable / "forkable".
Dans la suite on le décrit dans les grandes lignes.

### Le fonctionnement des API : retourner des photos
- les fonctions queryUnsplash et queryPixabay ("tools.py") se chargent 
de l'interrogation des plateformes de photos. Elles nécessitent un enregistrement préalable sur leur portail
développeurs afin d'y récupérer des clés d'usage. Voir https://pixabay.com/api/docs/ et 
https://unsplash.com/developers. Ces clés doivent être inscrites dans le fichier "settings.yaml" du projet.

- La ressource "Image" dont l'API "get" se charge de la consolidation 
des résultats des deux fonctions précédentes

### La gestion des API : app.py
La configuration des API, route et parsing des paramètres en particulier, est assuré par RestPlus via
- la classe Image qui par, l'héritage de la classe ressource, fonctionne suivant les préceptes REST.
- les décorateurs app.route, indiquant les routes pour l'appel des apis.
- le parser, se charge de décomposer les paramètres et contribue à produire la documentation pour swagger

Dans notre serveur on n'a finalemenet besoin que d'une seule api (plus celle pour l'authentification). 
On pourrait en ajouter d'autres, mais celles ci seraient construites sur à peu prèt le même model 
imposé par Flask-plus : une classe représente la ressource adressées et les méthode GET, POST de cette classe 
implémentent la logique REST.

### Authentification des appels à l'API : tools.py 
La gestion des tokens d'authentification, en particulier encodage et décodage, 
est assuré par les fonctions createToken et decodeToken
Le décorateur token_required vérifie la présence du token dans les API. Il reçoit l'instance de 
la base de données comme paramètre et peut ainsi récupérer le compte développeur et par exemple,
vérifier les quotas et / ou les droits avant d'autoriser l'exécution.

### La base de données : dao.py
La base de données est prise en charge par la classe DAO qui fait 
l'interface entre MongoDB et l'API, pour 
- ouvrir la connexion avec la base MongoDB via son constructeur,
- gérer les utilisateurs des api, (inscription et lecture dans la base pour confirmer la possibilité d'utiliser l'API)
- tracer l'ensemble des transactions (écritures à chaque appel, du token et de la date) ouvrant ainsi la possibilité
d'une gestion de quotas et d'une éventuelle facturation 


# Déploiement de l'API
Là aussi, l'usage de Docker simplifie le déploiement de notre API.

## Fabrication de l'image docker
Avant de fabriquer l'image, il est préférable de s'inscrire 
sur le <a href='https://hub.docker.com/'>hub docker</a> 
Après cette inscription vous disposez d'un espace pour stocker les images Docker
que vous allez construire. 

Une fois le code finaliser, stocker dans le fichier "App.py", 
le fichier Docker ("Dockerfile") permet la construction d'une image
déployable du serveur d'API. Elle repose sur une distribution Linux relativement
légère et disposant d'une image Python préinstallée.

Dans le répertoire GitHub, on propose deux fichiers Dockerfile. L'un permet de construire
une image docker installable sur un serveur de type x86. L'autre va permettre de déployer *
l'API sur un serveur ARM, Raspberry PI par exemple. Les deux images repose sur la distribution
Alpine compatible x86 et ARM.

Le fichier Dockerfile se charge d'installer sur l'image les libraries nécéssaires à
l'exécution de l'API et d'installer les fichiers python nécéssaire dans le répertoire /app 
de l'images.

La commande pour construire l'image est simple :

`docker build -t <votre_hub>/picturesearchenginex86 .`  

Elle doit être exécutée depuis le répertoire contenant le fichier "Dockerfile".

Une fois construite on se connecte a son compte docker pour pouvoir l'uploader.

`docker login`

après connexion, on execute la ligne suivante pour mettre en ligne notre image :

`docker push <votre_hub>/picturesearchenginex86:latest`

ou <votre_hub> est à remplacer par votre compte, évidemment.


## Installation de l'image
Maintenant que notre image est disponible, on peut la récupérer et l'installer sur le serveur
Ainsi, l'installation de l'API se fera via la commande "pull".

`docker pull <votre hub>/picturesearchenginex86:latest` 

pour lancer le serveur, il suffit d'utiliser la commande "run" de docker

`docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchenginex86 -d <votre hub>/picturesearchenginex86:latest localhost admin admin_password 5600 ssl` 

grâce à cette commande on a :
- téléchargé l'image picturesearchenginex86 fabriquée préalablement,
- programmé le rédémarrage automatique de l'API lorsque le serveur redémarre (--restart),
- ouvert l'accès aux certificats pour permettre à Flask de sécuriser les transactions (-v)
- ouvert le port 5600 pour la communication a notre API (-p)

Les derniers termes de la commande sont directement "passés" 
comme paramètres a l'API (récupérer par sys.args en python):
- Ainsi, les paramètres de connexion à la base de données sont transmis 
à l'installation de l'image dans la commande docker. Ici
on a passé "localhost" en considérant que l'API et la base sont sur 
le même serveur et "admin"/"admin_password" comme
utilisateur / password pour se connecter à la base
- enfin en terminant par "ssl" on configure l'API en mode sécurisé
(il est possible de lancer l'api en mode non sécurisé en enlenvant le paramèttre ssl. Dans ce cas, 
l'étape de fabrication des certificats n'est pas nécéssaire et l'api peut être jointe directement via
l'adresse IP du serveur) 


# Démonstrateur de l'API
Un démonstrateur, disponible en ligne via une interface minimal, est
accessible directement à l'adresse : https://pse.f80.fr

Il est possible de récupérer l'image utilisée par le démonstrateur en exécutant, sur le serveur :

`docker pull f80hub/picturesearchenginex86:latest && docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchenginex86 -d f80hub/picturesearchenginex86:latest localhost admin admin_password 5600 ssl`


## le mini front-end
L'interface se charge de :
- demander un token d'utilisation de l'API,
- demander le mot clé de la recherche,
- appeler l'API avec le mot clé et le token,
- afficher le résultat.

Au lancement on peut lui passer 3 paramètres pour lui indiquer ou se trouve le serveur 
et le port ouvert pour l'API :
`http://pse.f80.fr?server=<addresse_du_server>&port=<port_de_api>&endpoint=<endpoint>`

Dans un prochain article, nous remplacerons ce fichier par une web application développée sur Angular.

## L'interface swagger
Grâce à RestPlus on dispose automatiquement d'une interface d'interrogation de l'API 
accessible via https://server.f80.fr:5800

Pour l'utiliser il faut 
- obtenir un token par appel de la méthode "auth",
- l'inscrire dans la section "authentification" de Swagger UI,
- puis appeler l'API en passant les paramètres souhaités.  

Cette documentation repose sur l'usage de décorateurs au sein de notre code Python :
- @api.doc va être utilisé pour documenter le besoin d'une clé d'acces aux APIs
- @api.expect génére automatiquement une documentation des paramètres reposant sur un parser,
- @api.param en charge de la documentation des paramètres utilisés par les API (n'utilisant pas un parser)
- @api.response en charge de la documentation des réponses retournées par l'API

 
# Références
En plus des différents liens déjà cités, 
De nombreux articles disponibles sur le web, traitent des différentes briques 
impliquées dans l'API:
- L'installation de docker : https://docs.docker.com/get-started/
- La documentation de l'extension Flask-restplus : https://flask-restplus.readthedocs.io/en/stable/
- L'installation de MongoDB : https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/
- Comprendre les décorateurs sous python : http://sametmax.com/comprendre-les-decorateurs-python-pas-a-pas-partie-1/
- Un article assez proche sur la mise en place d'une API via RestPlus : https://blog.invivoo.com/designer-des-apis-rest-avec-flask-restplus/


Article rédigé par Herve HOAREAU
Société F80, Développement Full-Stack, tranformation digitale et analyse de données
herve.hoareau@f80.fr
