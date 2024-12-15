## Endpoints

### GitHub Repository: 

### Racine

#### `GET /`
- **Description**: Retourne un message de bienvenue.
- **Réponse**:
  - `200 OK`: `{"message": "Bienvenue sur l'API de gestion des utilisateurs et produits."}`

### Utilisateurs

#### `GET /utilisateurs`
- **Description**: Récupère tous les utilisateurs.
- **Réponse**:
  - `200 OK`: Liste des utilisateurs au format JSON.

#### `GET /utilisateur/<string:id>`
- **Description**: Récupère un utilisateur par son ID.
- **Paramètres**:
  - `id` (string): L'ID de l'utilisateur.
- **Réponse**:
  - `200 OK`: Données de l'utilisateur au format JSON.
  - `404 Not Found`: `{"erreur": "Utilisateur non trouvé."}`

#### `POST /utilisateur`
- **Description**: Crée un nouvel utilisateur avec les données fournies.
- **Corps de la requête** (JSON):
  - `nom` (string): Nom de l'utilisateur.
  - `prenom` (string): Prénom de l'utilisateur.
  - `email` (string): Email de l'utilisateur.
  - `password` (string): Mot de passe de l'utilisateur.
  - `product_ids` (liste, optionnel): Liste des IDs de produits associés à l'utilisateur.
- **Réponse**:
  - `201 Created`: `{"message": "Utilisateur créé avec succès", "id": "<new_user_id>"}`

#### `DELETE /utilisateur/<string:id>`
- **Description**: Supprime un utilisateur par son ID.
- **Paramètres**:
  - `id` (string): L'ID de l'utilisateur.
- **Réponse**:
  - `200 OK`: `{"message": "Utilisateur supprimé avec succès."}`
  - `404 Not Found`: `{"erreur": "Utilisateur non trouvé."}`

### Produits

#### `GET /produits`
- **Description**: Récupère tous les produits.
- **Réponse**:
  - `200 OK`: Liste des produits au format JSON.

#### `GET /produit/<int:id>`
- **Description**: Récupère un produit par son ID.
- **Paramètres**:
  - `id` (int): L'ID du produit.
- **Réponse**:
  - `200 OK`: Données du produit au format JSON.
  - `404 Not Found`: `{"erreur": "Produit non trouvé."}`

#### `POST /produit`
- **Description**: Crée un nouveau produit avec les données fournies.
- **Corps de la requête** (JSON):
  - `_id` (int): ID du produit.
  - `nom` (string): Nom du produit.
  - `description` (string): Description du produit.
  - `brand` (string): Marque du produit.
  - `prix` (float): Prix du produit.
- **Réponse**:
  - `201 Created`: `{"message": "Produit créé avec succès", "id": <new_product_id>}`

#### `DELETE /produit/<int:id>`
- **Description**: Supprime un produit par son ID.
- **Paramètres**:
  - `id` (int): L'ID du produit.
- **Réponse**:
  - `200 OK`: `{"message": "Produit supprimé avec succès."}`
  - `404 Not Found`: `{"erreur": "Produit non trouvé."}`

### Avancé

#### `GET /utilisateur/<string:id>/produits`
- **Description**: Récupère tous les produits associés à un utilisateur spécifique.
- **Paramètres**:
  - `id` (string): L'ID de l'utilisateur.
- **Réponse**:
  - `200 OK`: Liste des produits au format JSON.
  - `404 Not Found`: `{"erreur": "Utilisateur non trouvé."}`

#### `GET /utilisateur/<string:id>/produits/brand/<string:brand>`
- **Description**: Récupère les produits d'une marque spécifique associés à un utilisateur.
- **Paramètres**:
  - `id` (string): L'ID de l'utilisateur.
  - `brand` (string): La marque des produits.
- **Réponse**:
  - `200 OK`: Liste des produits au format JSON.
  - `404 Not Found`: `{"erreur": "Utilisateur non trouvé."}`

#### `GET /produits/prix/<string:min_prix>/<string:max_prix>`
- **Description**: Récupère les produits dans une fourchette de prix spécifiée.
- **Paramètres**:
  - `min_prix` (string): Prix minimum.
  - `max_prix` (string): Prix maximum.
- **Réponse**:
  - `200 OK`: Liste des produits au format JSON.

#### `GET /produits/count`
- **Description**: Retourne le nombre total de produits.
- **Réponse**:
  - `200 OK`: `{"nombre_de_produits": <count>}`

#### `GET /utilisateurs/produits/count`
- **Description**: Retourne une liste d'utilisateurs avec le nombre de produits qu'ils possèdent.
- **Réponse**:
  - `200 OK`: Liste des utilisateurs avec le nombre de produits au format JSON.
    """