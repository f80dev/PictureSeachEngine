# PSE - Picture Search Engine
Le Picture Search Engine est un méta-moteur, open source, de recherche de photos de qualitées.

# Objectif du projet
L'objectif de ce projet est de combiner plusieurs technologies éprouvées et reconnues pour 
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
- sous format Progressive Web App via Angular 8,
- en typescript,
- hébergé gratuitement sur les "github page".

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
donc commencer par l'installer ce gestionnaire de containers.

On trouve beaucoup de tutoriel suivant le système d'exploitation. 
Pour linux, après s'être connecté en mode root, la commande suivante 
fonctionne sans intervention le plus souvent :
`curl -sSL get.docker.com | sh`
 
puis on démarre le démon et on l'installe pour un démarage automatique 
`systemctl start docker && systemctl enable docker`

Normalement docker est maintenant installé. On peut le vérifier par la commande
`docker ps`  

# Sécurisation
L'étape suivante consiste à sécuriser le serveur pour permettre un appel de notre API via "https"
et l'API par l'usage d'un token d'authentification.

## sécurisation du serveur
L'usage de l'https pour héberger les sites est de plus en plus courant. 
Cela implique que les api utilisées par les front-end sécurisés doivent 
également utilisé le protocol 'https'. 
Pour autant on peut faire fonctionner l'API PSE sur un serveur non sécurisé. 
Dans ce cas, vous pouvez directement passez au chapitre suivant. 

l'usage https nécessite 
 - la mise en place de certificats SSL,
 - l'interoggation du serveur via un nom de domaine. 
  
 Dans cet exemple on va utiliser des certificats "Let's Encrypt".

Vous devez paramétrer le DNS de votre domaine pour le faire pointer vers l'adresse IP de
votre serveur. Le principe consiste 
à ajouter un "enregistrement A" au DNS du nom de domain.
La procédure pas à pas dépend de votre fournisseur de nom de domaine et est souvent détaillée dans les FAQ.
On peut également consulter :  
- https://blog.youdot.io/fr/4-types-enregistrements-dns-a-connaitre/
- https://docs.icodia.com/general/zones-dns

Il faut maintenant fabriquer les certificats.
Sur le serveur qui hébergera l'api, on installe "certbot" en suivant les instructions du site: 
https://certbot.eff.org/instructions

Cet outil automatise la procédure d'installation des certificats via la commande :
`certbot certonly --standalone -d sub.domaine.com` 
en remplacant sub.domain.com par votre domaine. 

Si tout se passe bien, vous récupèrez
plusieurs fichiers dans le répertoire /etc/letsencrypt/live/<sub.domain.com>

Pour établir une connexion sécurisée avec Flask on utilise deux fichiers 
produit par certbot : "fullchain.pem" et "privkey.pem". 

Ils faut les rendre visible à l'image docker de notre serveur
d'api. On va donc les copier dans le repertoire /root/certs:

`mkdir /root/certs && cp /etc/letsencrypt/live/sub.domain.com/* /root/certs`

Théoriquement, cette manipulation doit être réalisé chaque fois que l'on met
à jour les certificats.
on peut aussi choisir de faire point l'image docker directement sur le répertoire hébergent
les certificats et mettre en place un renouvellement automatique (voir https://certbot.eff.org/docs/using.html?highlight=renew#renewing-certificates)


## de l'api
Flask permet l'ajout d'une couche de sécurité directement au niveau
de l'API via l'usage de token pour identifier les utilisateurs (développeurs).

Pour aller plus loin, en particulier si l'on souhaite commercialiser l'api, il est souhaitable
d'installer une solution de gestion d'API (API management). On trouve plusieurs produits pour faire cela
Certains propriétaires d'autres Open source comme le détaille cet article : 
<a href="https://techbeacon.com/app-dev-testing/you-need-api-management-help-11-open-source-tools-consider">11 open-source tools to consider</a>
Dans notre cas, on va rester sur une gestion du token intégrer au serveur.

La procédure d'obtention du token est réduite à sa plus simple expression, puisqu'il suffit
d'appeler l'API "/auth" qui se charge d'enregistrer un username / password dans la base de données et de retourner 
le token d'authentification. 

# La base de données
L'objectif de l'article est également de montrer un exemple d'implémentation d'une 
base de données puissante dans l'univers Python. Pour cette raison on installe MongoDB.

## Installation
Pour ne pas compliquer le processus d'installation, on choisie d'utiliser MongoDB
via son image "docker" : https://hub.docker.com/_/mongo

Rien de plus simple :
`docker run --restart=always -v /root/mongodata:/data/db -d -p 27017-27019:27017-27019 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin_password mongo`

## Remarques
Il faut retenir que 
- l'écriture dans la base depuis l'API se fera avec le user/mot de passe : admin/admin_password
- la base n'est pas nécéssairement installé sur le même serveur que l'API
- la base est disponible sur le port 27017
- il est possible de se connecter via Mongo Compass pour visionner le contenu notre base depuis n'importe quel
poste dès lors qu'on utilise bien les paraméètres de connexion ci-dessus

## Usage
La librairie Python utilisé pour interragir avec MongoDB et PyMongo. MongoDB est une base orientée document.
Les enregistrements sont donc des dictionnaires python. On utilise 2 types d'objets.
Les utilisateurs des API ont la structure suivante :


# Logique de fonctionnement de l'API
## Principe
L'API est avant tout un prétexte pour illustrer l'architecture, pour autant elle pourrait servir de 
point de départ à un moteur de recherche d'images comme alternative à un google image.
Elle recoit en paramètre un mot clé et interroge deux plateformes de référencement de photo : PixaBay
et Unsplash. 
Les résultats sont concaténés et renvoyés au front-end sous forme d'une suite d'URL.

## Fichier de configuration
Dans une optique d'industrialisation, les paramètres du serveur sont regroupés 
dans une fichier YAML. <br>
Même si ce format est moin courant que json, on gagne en lisibilité 
et surtout on profite ainsi de la possibilité d'ajouter des commentaires.

Il contient les paramètres nécéssaires au fonctionnement du serveur, en particulier :
- le point de terminaison (endpoint) de notre API
- les paramètres d'accès aux plateformes de photos.

Ce fichier doit resté confidentiel.
On aurait pû y ajouter les paramètres d'accès à la base mais ces paramètres sont passés
dans la commande docker d'installation du serveur (voir rubrique sur l'installation)

##Principale fonction mise en oeuvre
Le code est abondamment commenté, donc facilement adaptable / "forkable".

On peut le décomposer en plusieurs blocs :
### Le fonctionnement des API
- les fonctions queryUnsplash et queryPixabay ("tools.py") se chargent 
de l'interrogation des plateformes de photos. Elles nécessitent un enregistrement préalable sur leur portail
développeurs afin d'y récupérer des clés d'usage. Voir https://pixabay.com/api/docs/ et 
https://unsplash.com/developers. Ces clés doivent être inscrites dans le fichier settings.yaml du projet

- La ressource "Image" dont l'API "get" se charge de la consolidation 
des résultats des deux fonctions précédentes

### La gestion des API : app.py
La configuration des API, route et parsing des paramètres en particulier, est assuré par RestPlus via
- la classe Image qui par, l'héritage de la classe ressource, fonctionne suivant les préceptes REST.
- les décorateurs app.route, indiquant les routes pour l'appel des apis.
- le parser, se charge de décomposer les paramètres et contribue à produire la documentation pour swagger

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
L'idéal est de commencer par s'inscrire sur le <a href='https://hub.docker.com/'>hub docker</a> 
afin de disposer d'un espace susceptible de recevoir
l'image Docker de l'API. 

une fois le code finaliser, le fichier "Dockerfile" permet la construction d'une image
déployable du serveur d'API.

La commande pour construire l'image est simple.

`docker build -t <votre_hub>/picturesearchenginex86 .`  

Elle doit être exécutée depuis le répertoire contenant le fichier "Dockerfile".
puis on se connecte :

`docker login`

pour enfin, la mettre en ligne sur le hub docker 

`docker push <votre_hub>/picturesearchenginex86:latest`

ou <votre_hub> est à remplacer par votre compte.


## Installation de l'image
Maintenant que notre image est disponible, on peut la récupérer et l'installer sur le serveur
Ainsi, l'installation de l'API se fera par la commande :

`docker pull <votre hub>/picturesearchenginex86:latest` 

pour récupérer l'image puis

`docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchenginex86 -d <votre hub>/picturesearchenginex86:latest localhost admin admin_password 5600 ssl` 

grâce à cette commande on a :
- téléchargé l'image picturesearchenginex86 fabriquée préalablement,
- programmé le rédémarrage automatique de l'API lorsque le serveur redémarre (restart),
- ouvert l'accès aux certificats pour permettre à Flask de sécuriser les transactions (-v)
- ouvert le port 5600 pour la communication a notre API (-p)

Les derniers termes de la commande sont directement "passés" comme paramètres a l'API (récupérer par sys.args en python):
- Ainsi, les paramètres de connexion à la base de données sont transmit à l'installation de l'image dans la commande docker. Ici
on a passé "localhost" en considérant que l'API et la base sont sur le même serveur et "admin"/"admin_password" comme
utilisateur / password pour se connecter à la base
- enfin en terminant par "ssl" on configure l'API en mode sécurisé
(il est possible de lancer l'api en mode non sécurisé en enlenvant le paramèttre ssl. Dans ce cas, 
l'étape de fabrication des certificats n'est pas nécéssaire et l'api peut être jointe directement via
l'adresse IP du serveur) 


# Remarque divers

- Il est possible de récupérer l'image utilisée par le démonstrateur en exécutant, sur le serveur :

`docker pull f80hub/picturesearchenginex86:latest && docker run --restart=always -v /root/certs:/app/certs -p 5600:5600 --name picturesearchenginex86 -d f80hub/picturesearchenginex86:latest localhost admin admin_password 5600 ssl`
 
- Via RestPlus on génére automatiquement une documentation Swagger et 
une interface d'utilisation pour notre API 


# Démonstrateur
Un démonstrateur est disponible en ligne via une interface minimal, 
accessible directement à l'adresse : https://pse.f80.fr

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
Grâce à RestPlus on dispose également d'une interface d'interrogation de l'API 
sur : https://server.f80.fr:5800
Pour l'utiliser il faut 
- obtenir un token,
- l'inscrire dans la section authentification,
- puis appeler l'API en passant les paramètres souhaités.  

 
# Références
De nombreux articles traitent des différentes briques 
impliquées dans le Picture Search Engine:
- L'installation de docker : https://docs.docker.com/get-started/
- La documentation de l'extension Flask-restplus : https://flask-restplus.readthedocs.io/en/stable/
- L'installation de MongoDB : https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/
