import glob
import pandas as pd
import dask.dataframe as dd
from pyspark.sql import SparkSession
import os
import matplotlib.pyplot as plt
from pyspark.sql import functions


#1.1 leggere file JSON con Pandas, usa il ciclo for e calcola la somma totale della colonna amount
totale_amount = 0

for file in glob.glob("./data_local/json/*.jsonl"):
    df = pd.read_json(file, lines=True)
    totale_amount += (df["amount"].sum())

print(totale_amount)


#1.2 Utilizza la libreria dask.dataframe, leggi tutti i file JSON in un colpo solo usando il carattere jolly (*.json), raggruppa le vendite per payment_type e calcola la media degli importi.

#non risulta predente la colonna payment_type, dunque scelgo una nuova colonna (month) per effettuare ugualmente il groupby

df_Dask = dd.read_json("./data_local/json/*.jsonl", lines=True)

media_for_moth = df_Dask.groupby("month")["amount"].mean().compute()

print(media_for_moth)


#2 Pipeline ETL con PySpark
#2.1 Inizializzazione SparkSession

os.environ["JAVA_HOME"]   = r"C:\Java\jdk25"
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = (
    r"C:\hadoop\bin;" + r"C:\Java\jdk25\bin;" + os.environ["PATH"]
)


spark = SparkSession.builder \
    .appName("ETL_con_PySpark") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


#2.2 Estrazione delle tabelle dai file parquet

df_transazione = spark.read.parquet("./data_local/parquet/transactions_batch_*.parquet")
df_prodotti = spark.read.parquet("./data_local/parquet/products.parquet")
df_regioni = spark.read.parquet("./data_local/parquet/regions.parquet")


#2.3 Unire Tabelle con JOIN e creare un dataframe finale
df_joined = df_transazione \
    .join(df_prodotti, on="product_id", how="inner") \
    .join(df_regioni, on="region_id", how="inner")

df_finale = df_joined.select(
    "transaction_id",
    "region_name",
    "category",
    "amount",
    "year"
)

df_finale.show(5)

#2.4 Salva il risultato in formato parquet

df_finale.write \
    .mode("overwrite") \
    .partitionBy("year") \
    .parquet("./data_local/processed_sales")


#3 Data Visualization
#3.1 Calcolare il fatturato totale per categoria ed eseguire l'azione ToPandas()

df_fatturato = df_finale.groupby(df_finale["category"]).agg(functions.sum("amount").alias("fatturato_totale"))

pandas_fatturato = df_fatturato.toPandas()
print(pandas_fatturato.head())

#3.2 Utilizzare Seaborn o Matplotlib per generare un grafico a barre che mostri il fatturato per ogni categoria

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(pandas_fatturato["category"], pandas_fatturato["fatturato_totale"] , color="blue")
ax.set_title("Fatturato per ogni categoria")
ax.set_xlabel("Categoria")
ax.set_ylabel("Fatturato")

#3.3 Salvare il grafico come immagine fatturato_per_categoria.png

plt.savefig("fatturato_per_categoria.png")
plt.show()


#4 Monitoraggio Live
#4.1 Script che legge la cartella json
schema = spark.read.json("./data_local/json").schema
schema_visibile = spark.read.json("./data_local/json").printSchema()

#4.2 Calcolare in tempo reale

df_stream = spark.readStream \
    .schema(schema) \
    .json("./data_local/json")


conteggio = df_stream.groupBy("region_id").count()

#4.3 stampare a video
query = conteggio.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()