import pandas as pd

# Charger les fichiers CSV dans des dataframes
bases_df = pd.read_csv('donnees/bases.csv')
images_df = pd.read_csv('donnees/images.csv')

# Effectuer la jointure sur la colonne 'dcterms:identifier'
merged_df = pd.merge(bases_df, images_df[['dcterms:identifier', 'dcterms:image']], 
                     on='dcterms:identifier', how='left')

# Enregistrer le dataframe fusionné dans un nouveau fichier CSV
merged_df.to_csv('donnees/bases_images_merged.csv', index=False)
