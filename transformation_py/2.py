import pandas as pd

# Chemins vers vos fichiers CSV d'origine
chemin_fichier_entree_1 = 'donnees/artwork88.csv'
chemin_fichier_entree_2 = 'donnees/artwork89.csv'

# Chemin pour sauvegarder le fichier CSV filtré combiné
chemin_fichier_sortie = 'donnees/images.csv'

# Fonction pour charger et traiter un fichier CSV
def process_file(chemin_fichier):
    # Lire le fichier CSV d'entrée en ne chargeant que les colonnes nécessaires
    colonnes_a_garder = ['crm:P59_has_section', 'schema:artworkSurface', 'dcterms:image']
    df = pd.read_csv(chemin_fichier, usecols=colonnes_a_garder)

    # Créer une nouvelle colonne 'dcterms:identifier' en combinant les deux colonnes
    df['dcterms:identifier'] = df['crm:P59_has_section'].astype(str) + '§' + df['schema:artworkSurface'].astype(str)

    # Diviser les lignes en fonction du symbole '§' dans 'dcterms:identifier'
    new_rows = []
    for index, row in df.iterrows():
        identifiers = row['dcterms:identifier'].split('§')
        for identifier in identifiers:
            new_row = {'dcterms:identifier': identifier, 'dcterms:image': row['dcterms:image']}
            new_rows.append(new_row)

    # Créer un nouveau DataFrame avec les lignes divisées
    df_filtre = pd.DataFrame(new_rows)
    return df_filtre

# Charger et traiter les deux fichiers d'entrée
df_entree_1 = process_file(chemin_fichier_entree_1)
df_entree_2 = process_file(chemin_fichier_entree_2)

# Concaténer les DataFrames résultants
df_combine = pd.concat([df_entree_1, df_entree_2], ignore_index=True)

# Supprimer les doublons dans la colonne 'dcterms:identifier'
df_combine = df_combine.drop_duplicates(subset='dcterms:identifier')

# Enregistrer le fichier CSV filtré combiné
df_combine.to_csv(chemin_fichier_sortie, index=False)
