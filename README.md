# PSE - Picture Search Engine
Le Picture Search Engine est un méta-moteur de recherche d'image de qualité, open source.
L'objectif du projet est d'illustrer une architecture client/serveur reposant sur un framework
de type micro-services securisés.

# Objectif
Ce projet est met en oeuvre plusieurs technologies reconnues
 comme références dans leur domaine pour la réalisation d'une architecture sécurisée de type micro-services. 
 
 On décompose la solution en 2 briques : le front-end et le back-end
 
Pour le backend :
- le langage python, dont le nombre de bibliothéque garantit de pouvoir s'attaquer 
à tout type de domaine d'activité avec une prédisposition pour la data et l'intelligence artificiel, est utilisé pour coder
notre API
- le framework d'architectures micro-services Flask, dotés de nombreux plugin pour faciliter la réalisation d'API performantes
et sécurisées 
- l'usage d'une base de données open-source et NoSQL : MongoDB, calibrée pour le big data,
- la containerisation via Docker simplifiant le déploiement et garantissant la scalabilité de l'ensemble 
- l'utilisation du plugin Flask-Restplus pour génération automatique de la documentation de l'API et d'un outil de test
- la sécurisation et le suivi (et l'éventuelle facturation) de l'usage de l'API via la gestion de token d'accès
- la sécurisation du serveur via l'usage d'un certificat gratuit Let's Encrypt

Le front-end est, pour l'instant, sous forme 
- d'une page HTML minimale pour interroger
- d'une interface d'interrogation de l'API via Swagger UI 

Dans un second article, nous développerons le front-end:
- sous format d'une Progressive Web App multi-devices (vs un développement pour chaque plateforme),
- en typescript sur la dernière version du framework Angular,
- hébergé gratuitement grâce aux github page.

# Démonstration
L'interface minimal est accessible directement à l'adresse : https://pse.f80.fr
La documentation auto-générée par l'extension 
RestPlus est disponible sur : https://server.f80.fr:5800 


# Configuration du serveur
A priori l'api peut être installé sur n'importe quel type d'OS supportant Python. Dans cet exemple, on se repose sur Linux 

Pour faire simple, toute l'installation va se faire en mode root ce qui n'est pas conseillé en environnement de production.
Ainsi le répertoire /root va héberger :
- un sous-répertoire "data" destiné à stocker la base MongoDB,
- un sous-répertoire "certs" va recevoir une copie des certificats pour la connexion SSL,

Le démonstrateur repose sur un serveur Linux sous Fédora 29.
Nous allons principalement utilisé des images sous Docker pour installer les différentes composantes de l'API. il faut 
donc commencer par l'installer.

On trouve beaucoup de tutoriel suivant le système d'exploitation. Pour linux la commande suivante 
fonctionne sans intervention le plus souvent :

`curl -sSL get.docker.com | sh`
 
 puis on démarre le démon et on l'installe pour un démarage automatique 
 
 `systemctl start docker && systemctl enable docker`

Normalement docker est installé.  

# Sécurisation
L'api peut fonctionner sur un serveur non sécurisé. Dans ce cas, le chapitre qui suit
est optionnel.
## ... du serveur
L'usage de l'https pour héberger les sites est de plus en plus courant. 
Cela implique que les api utilisées par les front-end sécurisés doivent également utilisé le protocol 'https'
On doit donc mettre en place des certificats SSL et interogger le serveur 
via son nom de domaine. Dans cet exemple on va utilise des certificats "Let's Encrypt".

Vous devez paramétrer le DNS de votre domaine pour le faire pointer vers l'adresse IP de
votre serveur. Le principe consiste 
à ajouter un "enregistrement A" au DNS du nom de domain.
La procédure pas à pas dépend de votre fournisseur de nom de domaine et est souvent détaillée dans les FAQ.
On peut également consulter :  
- https://blog.youdot.io/fr/4-types-enregistrements-dns-a-connaitre/
- https://docs.icodia.com/general/zones-dns

Il faut maintenant fabriquer les certificats.
Sur le serveur qui hébergera l'api, on récupère "certbot" qui automatise la procédure
d'installation des certificats via la commande :

`apt-get -t jessie-backports install certbot`

puis on lance la fabrication des certificats :

`certbot certonly --standalone -d sub.domaine.com` 
en remplacant sub.domain.com par votre domaine. Si tout se passe bien, vous récupèrez
plusieurs fichiers dans le répertoire /etc/letsencrypt/live/<sub.domain.com>

Pour établir une connexion sécurisée avec Flask on utilise deux de ces fichiers :
"fullchain.pem" et "privkey.pem". 

Ils sont copiés dans le repertoire /root/certs pour être accessible à notre serveur Flask :

`mkdir /root/certs && cp /etc/letsencrypt/live/sub.domain.com/* /root/certs`


## de l'api
Flask permet l'ajout d'une couche de sécurité via l'usage de token pour identifier 
les utilisateurs.

Pour aller plus loin, en particulier si l'on souhaite commercialisé l'api, il est souhaitable
d'installer une solution de gestion d'API (API management). On trouve plusieurs produits pour faire cela
Certains propriétaires d'autre Open source comme le montre cet article : 
<a href="https://techbeacon.com/app-dev-testing/you-need-api-management-help-11-open-source-tools-consider">11 open-source tools to consider</a>


# La base de données
L'objectif de l'article est également de montrer un exemple d'implémentation d'une base de données puissante dans une 
API Python. Pour cette raison on installe MongoDB.

On aurait pu utiliser des techniques plus légères ou des bases de données plus simple
que MongoDB mais l'objectif est d'illustrer l'usage d'une base moderne
 - opérationnelle pour le big data,
 - compatible avec l'<a href="https://www.datacamp.com/courses/introduction-to-using-mongodb-for-data-science-with-python">analyse de données</a>,
 - hautement scalable.


## Installation
Pour ne pas compliquer le processus d'installation, on choisie d'utiliser MongoDB
via son image "docker" : https://hub.docker.com/_/mongo

Rien de plus simple :

`docker run --restart=always -v /root/mongodata:/data/db -d -p 27017-27019:27017-27019 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin_password mongo`

## Remarques
Il faut retenir que 
- l'écriture dans la base depuis l'API se fera avec le user/mot de passe : admin/admin_password
- la base est disponible sur le port 27017
- il est possible de se connecter via Mongo Compass pour visionner le contenu notre base depuis n'importe quel
poste dès lors qu'on utilise bien les paraméètres de connexion ci-dessus

# L'api
## Principe
L'API est avant tout un prétexte pour illustrer l'architecture, pour autant elle pourrait servir de 
point de départ à un moteur de recherche d'images comme alternative à un google image.
Elle recoit en paramètre un mot clé et interroge deux plateformes de référencement de photo : PixaBay
et Unsplash. Les résultats sont concaténés et renvoyer au front-end sous forme d'une suite d'URL.

## Fichier de configuration
Dans une optique d'industrialisation, les paramètres du serveur sont regroupés 
dans une fichier YAML. <br>
Même si ce format est moin courant que json, on gagne en lisibilité et surtout YAML supporte les commentaires. 

##Principale fonction mise en oeuvre
Le code est abondamment commenté, donc facilement adaptable.

On peut le décomposer en plusieurs blocs :
###Le fonctionnement des API
- les fonctions queryUnsplash et queryPixabay ("tools.py") se chargent 
de l'interrogation des plateformes de photos.
- La ressource Image dont l'API "get" se charge de la consolidation 
des résultats des deux fonctions précédentes

### La gestion des API
Les fonctions du module "tools.py" s'occupe 
- de la gestion des token (encodage et décodage)

### La base de donénes
La base de données est prise en charge par la classe DAO ("dao.py") qui fait 
l'interface avec la base de données, pour 
- gérer les utilisateurs des api, (inscription et récupération des droits)
- tracer l'ensemble des transactions (écriture en base du token et de la date) donnant ainsi la possibilité
de gestion de quotas et d'une eventuelle facturation 


# Déploiement
Il est temps d'installer l'API. Là aussi, l'usage de Docker simplifie le déploiement. 
une fois le code finaliser, le fichier "Dockerfile" permet la construction d'une image
déployable du serveur d'API.

La commande pour construire l'image et la rendre disponible sur le hub docker est simple :
`docker build -t <votre_hub>/picturesearchenginex86 . & docker push <votre_hub>/picturesearchenginex86:latest`
ou <votre_hub> est remplacé par votre compte sur le portail.

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

Préalablement, le Front-End envoie un user et un mot de passe et recoit en échange un token temporaire.
Cette mécanique est mise en oeuvre, sur le serveur, par la librarie Flask-JWT selon le principe 
des JSON Web Token (https://fr.wikipedia.org/wiki/JSON_Web_Token).

Dans l'exemple aucune interface d'enregistrement des développeurs n'est proposées. Pour aurtant 


# Remarque divers
Le code est abondamment documenté. 
Via RestPlus on génére automatiquement une documentation pour notre API



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
 
