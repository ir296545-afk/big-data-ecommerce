from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, to_timestamp, current_date, date_sub, to_date

# Inicia o Apache Spark
spark = SparkSession.builder \
    .appName("BigDataEcommerce") \
    .getOrCreate()

# Lê os eventos do arquivo JSON
eventos = spark.read.json("spark/dados/eventos.json")

# Converte o campo timestamp de texto para data e hora
eventos = eventos.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"))
)

# Mostra todos os eventos
eventos.show(truncate=False)

# Filtra os eventos do dia anterior
eventos_dia_anterior = eventos.filter(
    to_date(col("timestamp")) == date_sub(current_date(), 1)
)

print("EVENTOS DO DIA ANTERIOR:")
eventos_dia_anterior.show(truncate=False)

# Filtra somente os eventos que são compras
compras = eventos_dia_anterior.filter(col("tipo_evento") == "compra")

print("COMPRAS REALIZADAS:")
compras.show(truncate=False)

# Agrupa as compras por produto e calcula os resultados
vendas_por_produto = compras.groupBy("produto").agg(
    count("*").alias("quantidade_vendas"),
    sum("valor").alias("valor_total"),
    avg("valor").alias("valor_medio")
)

print("RESUMO DE VENDAS POR PRODUTO:")
vendas_por_produto.show(truncate=False)