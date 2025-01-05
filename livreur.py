import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
CORS(app)

# Données simulées pour les livreurs
livreurs = {
    "john_doe": {
        "password": "password123",
        "schedule": [
            {"date": "2025-01-05", "product": "Laptop", "route": "Warehouse → Client A"},
            {"date": "2025-01-06", "product": "Phone", "route": "Warehouse → Client B"}
        ]
    },
    "jane_doe": {
        "password": "securepassword",
        "schedule": [
            {"date": "2025-01-05", "product": "Tablet", "route": "Warehouse → Client C"},
            {"date": "2025-01-07", "product": "Monitor", "route": "Warehouse → Client D"}
        ]
    }
}

# Données simulées pour les distances et le trafic
distance_matrix = np.array([
    [0, 10, 15, 20],  # Warehouse → Clients A, B, C, D
    [10, 0, 35, 25],  # Client A → Clients B, C, D
    [15, 35, 0, 30],  # Client B → Clients A, C, D
    [20, 25, 30, 0]   # Client C → Clients A, B, D
])

traffic_conditions = np.random.randint(1, 3, size=distance_matrix.shape)  # 1: fluide, 2: modéré

# Fonction d'optimisation avec l'algorithme des colonies de fourmis
def ant_colony_optimization(distance_matrix, n_ants=10, n_iterations=50, alpha=1, beta=2, evaporation_rate=0.5):
    n_nodes = len(distance_matrix)
    pheromone = np.ones((n_nodes, n_nodes))
    best_route = None
    best_distance = float('inf')

    for _ in range(n_iterations):
        routes = []
        distances = []

        for _ in range(n_ants):
            route = [0]  # Départ depuis l'entrepôt
            visited = set(route)

            while len(visited) < n_nodes:
                current = route[-1]
                probabilities = []

                for next_node in range(n_nodes):
                    if next_node not in visited:
                        prob = (
                            pheromone[current][next_node] ** alpha *
                            (1 / distance_matrix[current][next_node]) ** beta
                        )
                        probabilities.append((next_node, prob))

                total_prob = sum(prob[1] for prob in probabilities)
                probabilities = [(node, prob / total_prob) for node, prob in probabilities]
                chosen = max(probabilities, key=lambda x: x[1])[0]
                route.append(chosen)
                visited.add(chosen)

            route.append(0)  # Retour à l'entrepôt
            routes.append(route)

            distance = sum(
                distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1)
            )
            distances.append(distance)

        best_idx = np.argmin(distances)
        if distances[best_idx] < best_distance:
            best_distance = distances[best_idx]
            best_route = routes[best_idx]

        # Mise à jour des phéromones
        pheromone *= (1 - evaporation_rate)
        for i, route in enumerate(routes):
            for j in range(len(route) - 1):
                pheromone[route[j]][route[j + 1]] += 1 / distances[i]

    return best_route, best_distance

# Ajustement en temps réel avec un modèle supervisé
def adjust_route_in_real_time(features):
    # Exemple : modèle supervisé pré-entraîné (Random Forest ici)
    # Les "features" incluent le trafic, la météo, etc.
    model = RandomForestRegressor()
    # Données d'entraînement fictives
    X_train = np.random.rand(100, 3)  # Exemples de trafic, météo, autres données
    y_train = np.random.rand(100) * 10  # Délais simulés
    model.fit(X_train, y_train)

    prediction = model.predict([features])  # Prévoir le retard en temps réel
    return prediction[0]

@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    traffic = data.get('traffic_conditions', traffic_conditions)
    route, distance = ant_colony_optimization(distance_matrix + traffic)
    return jsonify({"route": route, "distance": distance})

@app.route('/adjust_route', methods=['POST'])
def adjust_route():
    data = request.json
    traffic = data.get('traffic')
    weather = data.get('weather')
    additional = data.get('additional', 1)  # Donnée additionnelle fictive
    delay_prediction = adjust_route_in_real_time([traffic, weather, additional])
    return jsonify({"adjusted_delay": delay_prediction})

# Endpoints existants (authentification, emploi du temps)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in livreurs and livreurs[username]['password'] == password:
        return jsonify({"message": "Login successful", "username": username}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/schedule/<username>', methods=['GET'])
def get_schedule(username):
    if username in livreurs:
        return jsonify(livreurs[username]['schedule']), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
