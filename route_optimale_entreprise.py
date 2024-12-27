from flask import Flask, request, jsonify
from math import radians, sin, cos, sqrt, atan2
import pandas as pd

app = Flask(__name__)

# Fonction pour calculer la distance (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Rayon moyen de la Terre en mètres
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Charger les données à partir d'un fichier CSV
file_path = r"C:\\Users\\LENOVO\\Downloads\\casablanca_delivery_dataset.csv"
data = pd.read_csv(file_path)

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    try:
        # Récupérer les données envoyées par la requête
        request_data = request.get_json()
        company_lat = float(request_data['company_lat'])
        company_lon = float(request_data['company_lon'])
        client_lat = float(request_data['client_lat'])
        client_lon = float(request_data['client_lon'])

        # Calculer la distance entre l'entreprise et le client
        distance = haversine(company_lat, company_lon, client_lat, client_lon)
        
        # Bonus : Si le fichier contient des données de livraison intermédiaires
        points_to_visit = data.sample(n=5).copy()  # Prendre 5 clients pour le test
        points_to_visit['Latitude'] = points_to_visit['Latitude'].astype(float)
        points_to_visit['Longitude'] = points_to_visit['Longitude'].astype(float)

        # Calculer un itinéraire optimal
        current_lat, current_lon = company_lat, company_lon
        route = []
        total_distance = 0

        while not points_to_visit.empty:
            points_to_visit['Distance_to_current'] = points_to_visit.apply(
                lambda row: haversine(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1
            )
            closest_point = points_to_visit.loc[points_to_visit['Distance_to_current'].idxmin()]
            route.append({
                "City": closest_point["City"],
                "Address": closest_point["Address"],
                "Distance_m": closest_point["Distance_to_current"]
            })
            total_distance += closest_point["Distance_to_current"]
            current_lat, current_lon = closest_point["Latitude"], closest_point["Longitude"]
            points_to_visit = points_to_visit.drop(closest_point.name)

        # Ajouter le client final à la fin
        client_distance = haversine(current_lat, current_lon, client_lat, client_lon)
        route.append({
            "City": "Client final",
            "Address": "Client",
            "Distance_m": client_distance
        })
        total_distance += client_distance

        # Préparer la réponse JSON
        response_data = {
            "route": [{"city": step["City"], "address": step["Address"], "distance_m": step["Distance_m"] / 1000} for step in route],
            "total_distance_km": total_distance / 1000
        }
        
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
