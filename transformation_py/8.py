import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('donnees/keywords.csv')

# Fonction pour convertir une date en demi-siècle
def convert_to_half_century(year):
    if pd.isna(year):
        return year  # Retourne la valeur d'origine si elle est NaN
    year = int(year)
    start = (year // 50) * 50 + 1
    end = start + 49
    return f"{start}-{end}"

# Appliquer la conversion à la colonne crm:P4_has_time-span_0
df['year'] = df['year'].apply(convert_to_half_century)

# Sauvegarder les modifications dans un nouveau fichier CSV
df.to_csv('data/data.csv', index=False)
