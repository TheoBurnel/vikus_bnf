import pandas as pd

# Charger le fichier CSV en spécifiant les colonnes à conserver
cols_to_keep = [
    'schema:artform', 'schema:creator', 'schema:locationCreated', 'crm:P4_has_time-span', 
    'dcterms:identifier', 'dcterms:image', 'crm:P2_has_type', 'dcterms:type', 'dcterms:subject', 
    'schema:artMedium', 'schema:color', 'schema:material', 'schema:status', 'schema:measurementMethod', 
    'schema:hasMeasurement', 'schema:observationDate', 'dcterms:abstract', 'dcterms:isReferencedBy', 
    'crm:P54_has_current_permanent_location', 'dcterms:title', 'dcterms:references'
]

file_path = 'bases_images_merged.csv'  # Remplacez par le chemin de votre fichier
df = pd.read_csv(file_path, usecols=cols_to_keep)

# Supprimer les doublons de la colonne 'dcterms:identifier'
df = df.drop_duplicates(subset=['dcterms:identifier'])

# Sauvegarder le fichier CSV sans doublons
output_file_path = 'doublons.csv'  # Remplacez par le chemin de sortie souhaité
df.to_csv(output_file_path, index=False)

print(f"Les doublons ont été supprimés et le fichier a été sauvegardé sous {output_file_path}")
