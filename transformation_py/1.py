import csv
import pandas as pd
import numpy as np

def nettoyer_identifiant(identifiant):
    # Trouver la position du premier § dans l'identifiant
    index_section = identifiant.find('§')
    if index_section != -1:
        # Retourner l'identifiant tronqué jusqu'au premier §
        return identifiant[:index_section]
    else:
        # Retourner l'identifiant tel quel s'il n'y a pas de §
        return identifiant

def processer_fichier_entree(fichier_entree):
    # Charger les données en ne sélectionnant que les colonnes pertinentes
    data = pd.read_csv(fichier_entree)

    # Nettoyer les identifiants dans la colonne 'dcterms:identifier'
    data['dcterms:identifier'] = data['dcterms:identifier'].apply(nettoyer_identifiant)

    # Filtrage des lignes contenant des coordonnées multiples
    filtered_data = data[data['schema:geographicArea'].fillna('').str.contains('§')]

    # Création du DataFrame étendu avec des coordonnées séparées
    extended_data = pd.DataFrame()

    for _, row in filtered_data.iterrows():
        coords = row['schema:geographicArea'].split('§')
        for coord in coords:
            new_row = {col: row[col] for col in data.columns}  # Garder toutes les colonnes du document original
            new_row['schema:geographicArea'] = coord.strip()
            extended_data = pd.concat([extended_data, pd.DataFrame([new_row])], ignore_index=True)

    # Suppression des doublons
    extended_data.drop_duplicates(subset=['dcterms:identifier', 'schema:geographicArea'], inplace=True)

    # Extraction des latitudes et longitudes
    extended_data[['latitude', 'longitude']] = extended_data['schema:geographicArea'].str.split(',', expand=True)

    # Conversion en types numériques
    extended_data['latitude'] = pd.to_numeric(extended_data['latitude'], errors='coerce')
    extended_data['longitude'] = pd.to_numeric(extended_data['longitude'], errors='coerce')

    # Grouper les données par 'dcterms:identifier' pour effectuer les comparaisons
    grouped = extended_data.groupby('dcterms:identifier')

    # Fonction pour déterminer quelle ligne conserver selon les critères spécifiés
    def keep_most_precise(group):
        if len(group) == 1:
            return group  # Si une seule ligne, la conserver

        # Calculer les différences entre les latitudes et les longitudes
        lat_diffs = np.abs(group['latitude'].diff())
        lon_diffs = np.abs(group['longitude'].diff())

        # Préparer un masque pour garder la ligne la plus précise
        keep_mask = np.ones(len(group), dtype=bool)

        for i in range(1, len(group)):
            if lat_diffs.iloc[i] <= 3 and lon_diffs.iloc[i] <= 3:
                # Comparer les précisions des latitudes et longitudes
                curr_lat_precision = len(str(group['latitude'].iloc[i]).split('.')[-1])
                prev_lat_precision = len(str(group['latitude'].iloc[i-1]).split('.')[-1])
                curr_lon_precision = len(str(group['longitude'].iloc[i]).split('.')[-1])
                prev_lon_precision = len(str(group['longitude'].iloc[i-1]).split('.')[-1])

                if (curr_lat_precision < prev_lat_precision) or (curr_lon_precision < prev_lon_precision):
                    keep_mask[i] = False  # Supprimer la ligne actuelle si moins précise

                if (curr_lat_precision == prev_lat_precision) or (curr_lon_precision == prev_lon_precision):
                    keep_mask[i] = False  # Garder une ligne si même décimale

        return group[keep_mask]

    # Appliquer la fonction de filtrage et concaténer les résultats
    filtered_data = grouped.apply(keep_most_precise).reset_index(drop=True)

    # Identifier les lignes non retenues par le filtrage
    not_kept_indices = filtered_data.index.isin(filtered_data['dcterms:identifier'].unique())

    # Extraire les lignes non retenues du DataFrame original
    not_kept_data = data[~data['schema:geographicArea'].fillna('').str.contains('§')]

    # Combiner les DataFrames filtrés avec les lignes non retenues pour obtenir le résultat final
    final_data = pd.concat([filtered_data, not_kept_data], ignore_index=True)

    return final_data

# Appeler la fonction pour traiter materiality89.csv
df1 = processer_fichier_entree('donnees/materiality89.csv')

# Appeler la fonction pour traiter materiality88.csv
df2 = processer_fichier_entree('donnees/materiality88.csv')

# Concaténer les DataFrames en un seul
df_combined = pd.concat([df1, df2], ignore_index=True)

# Chemin vers le fichier de sortie combiné (bases.csv)
chemin_sortie = "donnees/bases.csv"

# Enregistrer le DataFrame combiné dans un nouveau fichier CSV
df_combined.to_csv(chemin_sortie, index=False)

print("Les fichiers CSV ont été combinés avec succès.")
