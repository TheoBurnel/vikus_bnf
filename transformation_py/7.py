import pandas as pd

# Charger le fichier CSV
file_path = 'donnees/ligne1.csv'  # Remplacez par le chemin de votre fichier
df = pd.read_csv(file_path)

# Identifier les colonnes qui suivent le motif '_materiau'
materiau_columns = [col for col in df.columns if col.startswith('_matériau')]

# Ajouter une colonne 'keywords' qui cumule le contenu des colonnes '_materiau'
df['keywords'] = df[materiau_columns].apply(lambda row: ','.join(row.dropna().astype(str)), axis=1)

# Supprimer les doublons dans la colonne 'keywords'
def remove_duplicates(keywords):
    keywords_list = keywords.split(',')  # Convertir la chaîne en liste
    unique_keywords = set(keywords_list)  # Convertir la liste en ensemble pour supprimer les doublons
    return ','.join(unique_keywords)  # Convertir l'ensemble en chaîne séparée par des virgules

df['keywords'] = df['keywords'].apply(remove_duplicates)

# Réorganiser le DataFrame pour mettre 'keywords' au début
columns = ['keywords'] + [col for col in df.columns if col != 'keywords']
df = df[columns]

# Sauvegarder le fichier réorganisé
output_file_path = 'donnees/keywords.csv'  # Remplacez par le chemin de sortie souhaité
df.to_csv(output_file_path, index=False)

print(f"Le fichier a été réorganisé et sauvegardé sous {output_file_path}")
