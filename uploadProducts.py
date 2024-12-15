import random
from pymongo import MongoClient

# Configuration de la connexion MongoDB Atlas (à remplir avec vos informations)
MONGO_URI = "** ICI VOTRE URI :) **"  # Veuillez remplacer cette chaîne par votre URI de connexion MongoDB
DB_NAME = "mongoDBProject"
COLLECTION_NAME = "products"

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
products_collection = db[COLLECTION_NAME]

# Listes de noms, descriptions et marques de produits
noms_produits = ["Ordinateur", "Téléphone", "Casque", "Clavier", "Souris", "Écran", "Imprimante", "Tablette", "Chargeur", "Disque Dur"]
descriptions = [
    "Produit de haute qualité",
    "Version améliorée avec de nouvelles fonctionnalités",
    "Design moderne et élégant",
    "Durable et fiable",
    "Parfait pour un usage quotidien"
]
brands = ["Samsung", "Apple", "Sony", "Dell", "Logitech", "HP", "Asus", "Acer", "Lenovo", "Microsoft"]

def generer_produits(nb_produits=200):
    """Génère une liste de produits avec des données aléatoires."""
    produits = []
    print("Génération des données...")
    for i in range(1, nb_produits + 1):
        product = {
            "_id": i,
            "nom": random.choice(noms_produits),
            "description": random.choice(descriptions),
            "brand": random.choice(brands),
            "prix": round(random.uniform(10.0, 500.0), 2)
        }
        produits.append(product)
    return produits

def upload_products():
    """Upload les produits dans la base MongoDB."""
    produits = generer_produits()
    print("Upload des données...")
    result = products_collection.insert_many(produits)
    print(f"{len(result.inserted_ids)} produits ont été ajoutés.")

if __name__ == "__main__":
    upload_products()
