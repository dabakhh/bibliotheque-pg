# database.py
# Ce fichier a une seule responsabilité : ouvrir la connexion à MySQL

import mysql.connector
# On importe le connecteur qu'on a installé avec pip

def get_connection():
    """
    Cette fonction ouvre et retourne une connexion à la base de données.
    On l'appelle à chaque fois qu'on a besoin de parler à MySQL.
    """
    connexion = mysql.connector.connect(
        host     = "localhost",     # "localhost" = MySQL tourne sur TON ordinateur
                                    # Si MySQL est sur un autre serveur tu mets son adresse IP
        user     = "root",          # ton nom d'utilisateur MySQL
                                    # sur WAMP/XAMPP c'est souvent "root" par défaut
        password = "learnQuranfrom0",              # ton mot de passe MySQL
                                    # sur WAMP c'est souvent vide par défaut
        database = "bibliotheque",  # le nom de la base qu'on a créée à l'étape 1
                                    
        use_pure = True             # évite le bug du connecteur C-extension
    )
    return connexion
    # On retourne la connexion pour pouvoir l'utiliser depuis app.py
