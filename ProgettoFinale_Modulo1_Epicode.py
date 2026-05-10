import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

""" Parte 2 – Importazione con Pandas """
df = pd.read_csv("vendite.csv")
print(df)

print("--------------------------------------------------------------------------")

print(f"Le prime 5 righe del file csv sono: {df.head(5)}")

print("--------------------------------------------------------------------------")

print(f"Il numero di righe è : {df.shape[0]} \n Il numero di colonne è: {df.shape[1]}")

print("--------------------------------------------------------------------------")

print(f"Ecco le info generali")
df.info()


""" Parte 3 – Elaborazioni con Pandas """
print("--------------------------------------------------------------------------")

#Si aggiunge la colonna Incasso ricavata dalla moltiplicazione di Quantità per incasso
df["Incasso"] = df["Quantità"]*df["Prezzo_unitario"]
print(df)


print("--------------------------------------------------------------------------")

#Calcoliamo l'incasso totale di tutta la colonna Incasso
incasso_totale = df["Incasso"].sum()
print(f"L'incasso totale è: {incasso_totale}")

print("--------------------------------------------------------------------------")

#Calcoliamo l'incasso medio per negozio

incasso_medio_negozio = df.groupby("Negozio").agg({
    "Incasso" : "mean"
})
print(f"L'incasso medio per negozio è: \n {incasso_medio_negozio}")
print("--------------------------------------------------------------------------")


#Mostriamo i 3 prodotti più ventudi

top_tre_prodotti = df["Prodotto"].value_counts().head(3)
print(f"I 3 prodotti più venduti sono: {top_tre_prodotti}")
print("--------------------------------------------------------------------------")
#Raggruppare i dati per negozio e prodotto e mostrare l'incasso medio

incasso_medio_gruppi = df.groupby(["Negozio", "Prodotto"])["Incasso"].mean()
print(f"{incasso_medio_gruppi}")

print("--------------------------------------------------------------------------")

""" Parte 4 – Uso di NumPy """
#Estrarre colonna quantità come array
array_quantita = df["Quantità"].to_numpy()
print(array_quantita)

#calcolare minimo, massimo, deviazione standard

quantità_minima = np.min(array_quantita)
quantità_massima = np.max(array_quantita)
quantità_deviazione_standard = np.std(array_quantita)
quantità_media = np.mean(array_quantita)
print(f"La quantità minima è: {quantità_minima}")
print(f"La quantità minima è: {quantità_massima}")
print(f"La deviazione standard è: {quantità_deviazione_standard}")
print(f"La quantità media è: {quantità_media}")

#calcolare la percentuale di vendite sopra la media

numero_quantità_sopra_media = np.sum(array_quantita > quantità_media)
percentuale_quantità_sorp_media = (numero_quantità_sopra_media/ len(array_quantita)*100)
print(f"La percentuale di vendite sopra la media è :{percentuale_quantità_sorp_media}%")

#creare un array 2D che contenga quantità e prezzo unitario
print("-----------------------------------------------------------------")

array2d = df[["Quantità", "Prezzo_unitario"]].to_numpy()
np.set_printoptions(suppress=True, precision=2)
print(array2d)

print("-----------------------------------------------------------------")

#calcolare l'incasso per ogni riga dell'array2d
incasso_righe_array2d = array2d[:, 0] * array2d[:, 1]
print(incasso_righe_array2d)

""" Parte 5 – Visualizzazioni con Matplotlib """

#grafico a barre 
df.groupby("Negozio")["Incasso"].sum().plot(kind="bar")
plt.show()

#Grafico a torta: percentuale di incassi per ciascun prodotto
df.groupby("Prodotto")["Incasso"].sum().plot(kind="pie", autopct='%1.1f%%')
plt.show()

#Grafico a linee: andamento giornaliero degli incassi totali della catena

plt.plot(df['Incasso'], marker='o', linestyle='-', color='green')
plt.title('Andamento Giornaliero degli Incassi')
plt.ylabel('Incasso (€)')
plt.xlabel('Ordine Temporale / Giorno')
plt.grid(True)
plt.show()

""" Parte 6 – Analisi Avanzata """

print("-----------------------------------------------------------------")
#Aggiungere nuova colonna Categoria
mappa_categorie = {
    "TV" : "Elettrodomestici",
    "Cuffie" : "Informatica",
    "Monitor": "Informatica",
    "Smartwatch" : "Indossabili",
    "Tablet" : "Informatica",
    "Laptop" : "Informatica",
    "Smartphone" : "Informatica"
}

df["Categoria"] = df["Prodotto"].map(mappa_categorie)

#Calcolare Incasso e Quantità media per ogni categoria
analisi = df.groupby("Categoria").agg({
    "Incasso" : "sum",
    "Quantità" : "mean"
})
print(analisi)

#salvare nuovo DataFrame aggiornato in nuovo file CSV
df.to_csv("vendite_analizzate.csv", index=False)







""" Parte 7 – Estensioni """

# --- 1. Grafico combinato: Incasso medio e Quantità media per categoria ---

# Prepariamo i dati raggruppati
analisi_estensioni = df.groupby("Categoria").agg({
    "Incasso": "mean",
    "Quantità": "mean"
}).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 6))

# Primo asse (Barre): Incasso Medio
color_incasso = 'steelblue'
ax1.set_xlabel('Categoria')
ax1.set_ylabel('Incasso Medio (€)', color=color_incasso, fontsize=12)
ax1.bar(analisi_estensioni['Categoria'], analisi_estensioni['Incasso'], color=color_incasso, alpha=0.6, label='Incasso Medio')
ax1.tick_params(axis='y', labelcolor=color_incasso)

# Secondo asse (Linea): Quantità Media
ax2 = ax1.twinx() 
color_quantita = 'darkred'
ax2.set_ylabel('Quantità Media Venduta', color=color_quantita, fontsize=12)
ax2.plot(analisi_estensioni['Categoria'], analisi_estensioni['Quantità'], color=color_quantita, marker='o', linewidth=3, label='Quantità Media')
ax2.tick_params(axis='y', labelcolor=color_quantita)

plt.title('Relazione tra Incasso Medio e Quantità Media per Categoria')
fig.tight_layout()
plt.show()


# --- 2. Funzione top_n_prodotti(n) ---

def top_n_prodotti(n):
    """
    Restituisce i primi n prodotti per incasso totale.
    """
    # Raggruppiamo per prodotto, sommiamo l'incasso e ordiniamo in modo decrescente
    risultato = df.groupby("Prodotto")["Incasso"].sum().sort_values(ascending=False).head(n)
    return risultato

# Esempio di utilizzo della funzione
n_desiderato = 3
top_prod = top_n_prodotti(n_desiderato)

print(f"I top {n_desiderato} prodotti per incasso totale sono:")
print(top_prod)