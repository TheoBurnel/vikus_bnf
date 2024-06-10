import pandas as pd

# Charger le fichier CSV dans un DataFrame pandas
df = pd.read_csv('data/data.csv')

# Remplacer les valeurs manquantes dans la colonne 'year' par "indéterminé"
df['year'] = df['year'].fillna('indéterminé')

# Fonction pour formater les années
def format_year_range(year_range):
    if year_range == 'indéterminé':
        return year_range
    if isinstance(year_range, str):
        start_year, end_year = year_range.split('-')
        start_year = start_year.zfill(4)
        end_year = end_year.zfill(4)
        return f"{start_year}-{end_year}"
    return year_range

# Appliquer la fonction sur la colonne 'year'
df['year'] = df['year'].apply(format_year_range)

# Trier le DataFrame par ordre chronologique en fonction de la colonne 'year'
df_sorted = df.sort_values(by='year')

# Afficher le DataFrame trié
print(df_sorted)

# Sauvegarder le DataFrame trié dans un nouveau fichier CSV
df_sorted.to_csv('data/data.csv', index=False)

print("Les dates ont été mises à jour et le fichier trié a été enregistré dans 'data/data.csv'.")
