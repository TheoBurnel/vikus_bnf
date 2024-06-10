import pandas as pd
import re

# Charger le fichier CSV
file_path = 'prepared.csv'  # Remplacez par le chemin de votre fichier
df = pd.read_csv(file_path)

# Dictionnaire pour stocker les lignes principales et les lignes supplémentaires
main_rows = {}
additional_rows = {}

# Colonnes à copier des lignes supplémentaires
columns_to_copy = ['_analyse', '_type_description', '_motif', '_couleur', '_materiau', '_technologie', '_certitude', '_date_analyse', '_rapport', '_source']

# Fonction pour extraire la base de l'identifiant (sans suffixe)
def get_base_identifier(identifier):
    match = re.search(r'_(\d+)$', identifier)
    if match:
        base_id = identifier[:match.start()]
        suffix = match.group(1)
        return base_id, suffix
    else:
        return identifier, None

# Organiser les lignes par base_id et suffixe
for idx, row in df.iterrows():
    base_id, suffix = get_base_identifier(row['dcterms:identifier'])
    if suffix == '001':
        main_rows[base_id] = row
    else:
        if base_id not in additional_rows:
            additional_rows[base_id] = []
        additional_rows[base_id].append(row[columns_to_copy])

# Nouvelle liste pour stocker les lignes combinées
combined_rows = []

# Réorganiser les lignes
for base_id, main_row in main_rows.items():
    combined_data = main_row.tolist()
    if base_id in additional_rows:
        for add_row in additional_rows[base_id]:
            combined_data.extend(add_row.tolist())
    combined_rows.append(combined_data)

# Convertir la liste de nouvelles lignes en DataFrame
# Créer une liste des nouvelles colonnes, ajoutant des suffixes pour les colonnes supplémentaires
new_columns = list(df.columns)
for i in range(1, len(additional_rows.values())):
    new_columns.extend([f"{col}_{i+1}" for col in columns_to_copy])

# Assurez-vous que chaque ligne a le même nombre de colonnes
max_cols = max(len(row) for row in combined_rows)
for row in combined_rows:
    while len(row) < max_cols:
        row.append('')  # Ajouter des valeurs vides pour les colonnes manquantes

# Créer le nouveau DataFrame
new_df = pd.DataFrame(combined_rows, columns=new_columns[:max_cols])

# Sauvegarder le fichier réorganisé
output_file_path = 'ligne1.csv'  # Remplacez par le chemin de sortie souhaité
new_df.to_csv(output_file_path, index=False)

print(f"Le fichier a été réorganisé et sauvegardé sous {output_file_path}")
