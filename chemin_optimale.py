
from math import radians, sin, cos, sqrt, atan2
import pandas as pd

# Fonction pour calculer la distance à vol d'oiseau (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Rayon de la Terre en mètres
    dlat = radians(lat2 - lat1)
    dlon = radians(lat2 - lon2)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Charger le dataset
file_path = r"C:\\Users\\LENOVO\\Downloads\\casablanca_delivery_dataset.csv"
data = pd.read_csv(file_path)

# Définir les coordonnées de l'entreprise et de l'adresse du client final
company_lat, company_lon = 33.5898, -7.6039  # Centre de Casablanca
client_final_lat, client_final_lon = 3.5748, -9.6200  # Exemple de client final

# Étape 1 : Filtrer les points spécifiques à visiter
# Sélectionner aléatoirement quelques clients pour le test
points_to_visit = data.sample(n=5).copy()  # Exemple : prendre 5 clients aléatoires
points_to_visit['Latitude'] = points_to_visit['Latitude'].astype(float)
points_to_visit['Longitude'] = points_to_visit['Longitude'].astype(float)

# Séparer le client final
final_point = pd.DataFrame([{
    'City': "Destination finale",
    'Address': "Client final",
    'Latitude': client_final_lat,
    'Longitude': client_final_lon
}])

# Étape 2 : Calcul de l'itinéraire optimal pour les points hors client final
current_lat, current_lon = company_lat, company_lon  # L'entreprise est le point de départ
route = []
total_distance = 0  # Distance totale à parcourir

while not points_to_visit.empty:
    # Calcul de la distance à partir de la position actuelle pour tous les points restants
    points_to_visit['Distance_to_current'] = points_to_visit.apply(
        lambda row: haversine(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1
    )
    # Trouver le point le plus proche
    closest_point = points_to_visit.loc[points_to_visit['Distance_to_current'].idxmin()]

    # Ajouter ce point à l'itinéraire
    route.append({
        "City": closest_point["City"],
        "Address": closest_point["Address"],
        "Distance_m": closest_point["Distance_to_current"]
    })
    total_distance += closest_point["Distance_to_current"]  # Ajouter la distance parcourue

    # Mettre à jour la position actuelle
    current_lat, current_lon = closest_point["Latitude"], closest_point["Longitude"]

    # Supprimer ce point des points restants
    points_to_visit = points_to_visit.drop(closest_point.name)

# Étape 3 : Ajouter le client final à la fin de l'itinéraire
client_distance = haversine(current_lat, current_lon, client_final_lat, client_final_lon)
route.append({
    "City": "Destination finale",
    "Address": "Client final",
    "Distance_m": client_distance
})
total_distance += client_distance  # Ajouter la distance pour atteindre le client final

# Afficher le résultat organisé
print("Pour transmettre cette commande, voici le chemin optimal :\n")
for i, step in enumerate(route, start=1):
    if i == len(route):  # Dernier point (client final)
        print(f"{i}. Pour atteindre le client final, rendez-vous à l'adresse : {step['Address']}.")
    else:
        print(f"{i}. Avant de continuer, visitez l'adresse suivante : {step['Address']}.")

# Afficher la distance totale
print(f"\nLa distance totale à parcourir est : {total_distance:.2f} mètres.")
