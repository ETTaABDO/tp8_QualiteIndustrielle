import pandas as pd
import matplotlib.pyplot as plt

# Activité 8 - Application au domaine de la qualité industrielle

# 1. Importation
df = pd.read_csv("qualite_industrielle.csv")

# 2. Exploration
print("===== STRUCTURE DU DATASET =====")
print("Dimensions (lignes, colonnes) :", df.shape)
print("\n5 premières lignes :")
print(df.head())
print("\nNoms des colonnes :")
print(df.columns.tolist())
print("\nInformations générales :")
df.info()

print("\n===== VERIFICATION DES DONNEES =====")
print("\nValeurs manquantes par colonne :")
print(df.isnull().sum())
print("\nNombre de lignes en double :", df.duplicated().sum())

print("\n===== ANALYSE DES DONNEES =====")
print("\nStatistiques des variables numériques :")
print(df.describe())
print("\nNombre de contrôles par produit :")
print(df["Produit"].value_counts())
print("\nRésultats des contrôles qualité :")
print(df["Resultat"].value_counts())
print("\nNombre de défauts par produit (somme) :")
print(df.groupby("Produit")["Nb_Defauts"].sum().sort_values(ascending=False))
print("\nTaux moyen de défauts par ligne de production :")
print(df.groupby("Ligne_Production")["Taux_Defauts_pct"].mean().sort_values(ascending=False))
print("\nCoût moyen de non-qualité par résultat :")
print(df.groupby("Resultat")["Cout_Non_Qualite_DH"].mean())

# 3. Nettoyage
# Supprimer les lignes entièrement identiques.
df = df.drop_duplicates()

# Remplir les valeurs numériques manquantes par la médiane et les textes
# manquants par la valeur la plus fréquente, uniquement si nécessaire.
for col in df.columns:
    if df[col].isnull().any():
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])
            else:
                df[col] = df[col].fillna("Inconnu")

df.to_csv("qualite_industrielle_nettoyee.csv", index=False)
print("\nFichier sauvegardé : qualite_industrielle_nettoyee.csv")
print("Dimensions après nettoyage :", df.shape)

# 4. Graphiques
# Graphique 1 : nombre de contrôles par résultat
plt.figure(figsize=(7, 5))
df["Resultat"].value_counts().plot(kind="bar")
plt.title("Répartition des résultats du contrôle qualité")
plt.xlabel("Résultat")
plt.ylabel("Nombre de contrôles")
plt.xticks(rotation=0)
plt.tight_layout()

# Graphique 2 : taux moyen de défauts par produit
plt.figure(figsize=(8, 5))
df.groupby("Produit")["Taux_Defauts_pct"].mean().sort_values(ascending=False).plot(kind="bar")
plt.title("Taux moyen de défauts par produit")
plt.xlabel("Produit")
plt.ylabel("Taux moyen de défauts (%)")
plt.xticks(rotation=0)
plt.tight_layout()

# Graphique 3 : taux moyen de défauts par ligne de production
plt.figure(figsize=(8, 5))
df.groupby("Ligne_Production")["Taux_Defauts_pct"].mean().sort_values(ascending=False).plot(kind="bar")
plt.title("Taux moyen de défauts par ligne de production")
plt.xlabel("Ligne de production")
plt.ylabel("Taux moyen de défauts (%)")
plt.xticks(rotation=0)
plt.tight_layout()

# Graphique 4 : coût de non-qualité selon le résultat
plt.figure(figsize=(7, 5))
df.boxplot(column="Cout_Non_Qualite_DH", by="Resultat")
plt.title("Coût de non-qualité selon le résultat")
plt.suptitle("")
plt.xlabel("Résultat")
plt.ylabel("Coût de non-qualité (DH)")
plt.tight_layout()

# Graphique 5 : distribution des taux de défauts
plt.figure(figsize=(7, 5))
df["Taux_Defauts_pct"].plot(kind="hist", bins=10, edgecolor="black")
plt.title("Distribution des taux de défauts")
plt.xlabel("Taux de défauts (%)")
plt.ylabel("Nombre de contrôles")
plt.tight_layout()

# Graphique 6 : relation entre défauts et coût de non-qualité
plt.figure(figsize=(7, 5))
plt.scatter(df["Nb_Defauts"], df["Cout_Non_Qualite_DH"])
plt.title("Relation entre le nombre de défauts et le coût de non-qualité")
plt.xlabel("Nombre de défauts")
plt.ylabel("Coût de non-qualité (DH)")
plt.tight_layout()

# Affiche toutes les figures dans des fenêtres graphiques.
plt.show()