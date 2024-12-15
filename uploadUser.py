import random
import hashlib
from pymongo import MongoClient
import string

MONGO_URI = "** ICI VOTRE URI :) **"  # Veuillez remplacer cette chaîne par votre URI de connexion MongoDB
DB_NAME = "mongoDBProject"
COLLECTION_NAME = "users"
PRODUCTS_COLLECTION_NAME = "products"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]
products_collection = db[PRODUCTS_COLLECTION_NAME]

noms = ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Simon", "Laurent", "Lefevre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier", "Morel"]
prenoms = ["Jean", "Marie", "Claude", "Luc", "Sophie", "Paul", "Laura", "Pierre", "Nathalie", "Julien", "Elise", "Antoine", "Camille", "Louis", "Isabelle", "Alexandre", "Margaux", "Hugo", "Emma", "Léa"]
domaines = ["gmail.com", "yahoo.com", "protonmail.com", "hotmail.com", "yandex.ru"]

def generer_password():
    """Génère un mot de passe hashé aléatoire."""
    mot_de_passe = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    hashed = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    return hashed

def generer_email(nom, prenom):
    """Génère un email en combinant nom et prénom."""
    domaine = random.choice(domaines)
    return f"{prenom.lower()}.{nom.lower()}@{domaine}"

def get_all_product_ids():
    """Récupère tous les IDs de produits existants depuis la base de données."""
    products = products_collection.find({}, {"_id": 1})
    return [product["_id"] for product in products]

def generer_users(nb_users=20, product_ids=None):
    """Génère une liste d'utilisateurs avec des données aléatoires."""
    if not product_ids:
        print("Aucun produit trouvé dans la base de données.")
        return []

    print("Génération des données...")
    users = []
    for _ in range(nb_users):
        nom = random.choice(noms)
        prenom = random.choice(prenoms)
        email = generer_email(nom, prenom)
        password = generer_password()
        assigned_product_ids = random.sample(product_ids, random.randint(1, 5))

        user = {
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "password": password,
            "product_ids": assigned_product_ids
        }
        users.append(user)
    return users

def upload_users():
    """Upload les utilisateurs dans la base MongoDB."""
    product_ids = get_all_product_ids()
    if not product_ids:
        print("Erreur : La collection des produits est vide.")
        return

    users = generer_users(product_ids=product_ids)
    print("Upload des données...")
    result = users_collection.insert_many(users)
    print(f"{len(result.inserted_ids)} utilisateurs ont été ajoutés.")

if __name__ == "__main__":
    upload_users()