from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

MONGO_URI = "** ICI VOTRE URI :) **"  # Veuillez remplacer cette chaîne par votre URI de connexion MongoDB
DB_NAME = "mongoDBProject"

# Initialiser Flask et MongoDB
app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
products_collection = db["products"]


@app.route("/")
def accueil():
	"""
	Route d'accueil de l'API.
	Retourne un message de bienvenue.
	"""
	return jsonify({"message": "Bienvenue sur l'API de gestion des utilisateurs et produits."})


# ----------- Routes Utilisateurs -----------

@app.route("/utilisateurs", methods=["GET"])
def get_utilisateurs():
	"""
	Récupère tous les utilisateurs.
	"""
	utilisateurs = users_collection.find()
	return dumps(utilisateurs), 200


@app.route("/utilisateur/<string:id>", methods=["GET"])
def get_utilisateur(id):
	"""
	Récupère un utilisateur par son ID.
	"""
	utilisateur = users_collection.find_one({"_id": ObjectId(id)})
	if utilisateur:
		return dumps(utilisateur), 200
	return jsonify({"erreur": "Utilisateur non trouvé."}), 404


@app.route("/utilisateur", methods=["POST"])
def create_utilisateur():
	"""
	Crée un nouvel utilisateur avec les données fournies.
	"""
	data = request.json
	nouveau_user = {
		"nom": data["nom"],
		"prenom": data["prenom"],
		"email": data["email"],
		"password": data["password"],
		"product_ids": data.get("product_ids", [])
	}
	result = users_collection.insert_one(nouveau_user)
	return jsonify({"message": "Utilisateur créé avec succès", "id": str(result.inserted_id)}), 201


@app.route("/utilisateur/<string:id>", methods=["DELETE"])
def delete_utilisateur(id):
	"""
	Supprime un utilisateur par son ID.
	"""
	result = users_collection.delete_one({"_id": ObjectId(id)})
	if result.deleted_count:
		return jsonify({"message": "Utilisateur supprimé avec succès."}), 200
	return jsonify({"erreur": "Utilisateur non trouvé."}), 404


# ----------- Routes Produits -----------

@app.route("/produits", methods=["GET"])
def get_produits():
	"""
	Récupère tous les produits.
	"""
	produits = products_collection.find()
	return dumps(produits), 200


@app.route("/produit/<int:id>", methods=["GET"])
def get_produit(id):
	"""
	Récupère un produit par son ID.
	"""
	produit = products_collection.find_one({"_id": id})
	if produit:
		return dumps(produit), 200
	return jsonify({"erreur": "Produit non trouvé."}), 404


@app.route("/produit", methods=["POST"])
def create_produit():
	"""
	Crée un nouveau produit avec les données fournies.
	"""
	data = request.json
	nouveau_produit = {
		"_id": data["_id"],
		"nom": data["nom"],
		"description": data["description"],
		"brand": data["brand"],
		"prix": data["prix"]
	}
	result = products_collection.insert_one(nouveau_produit)
	return jsonify({"message": "Produit créé avec succès", "id": nouveau_produit["_id"]}), 201


@app.route("/produit/<int:id>", methods=["DELETE"])
def delete_produit(id):
	"""
	Supprime un produit par son ID.
	"""
	result = products_collection.delete_one({"_id": id})
	if result.deleted_count:
		return jsonify({"message": "Produit supprimé avec succès."}), 200
	return jsonify({"erreur": "Produit non trouvé."}), 404


# ----------- Routes Avancées -----------

@app.route("/utilisateur/<string:id>/produits", methods=["GET"])
def get_produits_utilisateur(id):
	"""
	Récupère tous les produits appartenant à un utilisateur spécifique.
	"""
	utilisateur = users_collection.find_one({"_id": ObjectId(id)})
	if not utilisateur:
		return jsonify({"erreur": "Utilisateur non trouvé."}), 404

	# Récupère les IDs des produits associés à l'utilisateur
	product_ids = utilisateur.get("product_ids", [])
	produits = products_collection.find({"_id": {"$in": product_ids}})
	return dumps(produits), 200


@app.route("/utilisateur/<string:id>/produits/brand/<string:brand>", methods=["GET"])
def get_produits_utilisateur_par_marque(id, brand):
	"""
	Récupère les produits d'un utilisateur pour une marque donnée.
	"""
	utilisateur = users_collection.find_one({"_id": ObjectId(id)})
	if not utilisateur:
		return jsonify({"erreur": "Utilisateur non trouvé."}), 404

	# Filtrer les produits par marque
	product_ids = utilisateur.get("product_ids", [])
	produits = products_collection.find({"_id": {"$in": product_ids}, "brand": brand})
	return dumps(produits), 200


@app.route("/produits/prix/<string:min_prix>/<string:max_prix>", methods=["GET"])
def get_produits_par_prix(min_prix, max_prix):
	"""
	Récupère les produits dont le prix est compris entre min_prix et max_prix.
	"""
	produits = products_collection.find({"prix": {"$gte": float(min_prix), "$lte": float(max_prix)}})
	return dumps(produits), 200


@app.route("/produits/count", methods=["GET"])
def get_nombre_produits():
	"""
	Retourne le nombre total de produits.
	"""
	count = products_collection.count_documents({})
	return jsonify({"nombre_de_produits": count}), 200


@app.route("/utilisateurs/produits/count", methods=["GET"])
def get_utilisateurs_avec_nombre_produits():
	"""
	Retourne la liste des utilisateurs avec le nombre de produits qu'ils possèdent.
	"""
	utilisateurs = users_collection.aggregate([
		{
			"$lookup": {
				"from": "products",
				"localField": "product_ids",
				"foreignField": "_id",
				"as": "produits"
			}
		},
		{
			"$project": {
				"_id": 0,
				"email": 1,
				"nombre_de_produits": {"$size": "$produits"}
			}
		}
	])
	return dumps(utilisateurs), 200


# ----------- Lancer l'application -----------

if __name__ == "__main__":
	app.run(debug=True)
