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

# Configuration du serveur
Dans le projet on utilise un serveur Linux pour héberger nos images Docker, et l'on se place dans une configuration root
(ce qui n'est clairement pas conseillé en environnement de production)

L'installation de docker dépend de l'OS mais dans beaucoup de cas, il suffit d'exécuter :
<pre>
sudo curl -sSL get.docker.com | sh
</pre>


# La base de données
La base de données est utilsée comme cache pour stocker les réponses aux requêtes. 
On aurait pu utiliser des techniques plus légère ou des bases de données plus simple
que MongoDB mais l'objectif était également de mettre en oeuvre une base NoSQL de plus
en plus utilisé dans les projets d'envergure.

Via docker, on peut avoir une installation de la base particulierement simple à mettre en
oeuvre :
<pre>
docker run --restart=always -v /root/mongodata:/data/db -d -p 27017:27017 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin_password mongo
</pre>
On aurait pû utiliser
- un autre port que le port standard : 27017 
- un autre user / mot de passe que admin / admin_password

# Références
De nombreux articles traitent des différentes briques 
impliquées dans le Picture Search Engine:
- La documentation de l'extension Flask-JWT : https://pythonhosted.org/Flask-JWT/
- La documentation de l'extension Flask-restplus : https://flask-restplus.readthedocs.io/en/stable/
 
