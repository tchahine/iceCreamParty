# iceCreamParty

Nalo lance le 1er glacier automate au monde !!

## Le projet
Il y a 5 parfums de crème glacée disponibles :
- Chocolat Orange
- Sirop d'érable Noix
- Menthe Chocolat
- Vanille Fraise Chocolat
- Chocolat blanc Framboise

Un pot de glace contient 40 boules.

Chaque boule coûte 2 euros.

Un utilisateur a le choix du nombre de boule et des parfums.


## Specifications
1. Une page doit permettre la saisie de la commande gérée en API, le prix sera retournée
ainsi qu'un code aléatoire unique. Il faut gérer les problèmes de stocks !
2. Une page doit permettre de récupérer la commande en entrant le numéro de
commande, une représentation graphique de la glace (boule(s)) sera affiché à l'écran
3. Une page administrateur permet de voir les recettes, le taux de remplissage des pots de
glace
4. Un bouton permet de remplir un pot vide, si un pot est vide un email est envoyé à
l’adresse de l’administrateur (un print suffit pour ce test)
5. Bien sur le code est testé :)
6. Le projet doit être facilement déployés et des instructions pour le déploiement doivent
être fournies


## Requirements
pip install django

pip install pytest-django


## Dev deployment
python manage.py migrate

python manage.py createsuperuser

pytest

python manage.py runserver
