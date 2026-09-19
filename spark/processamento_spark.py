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

# Filtra os eventos de entrega do dia anterior
entregas = eventos_dia_anterior.filter(
    col("tipo_evento") == "entrega"
)

print("ENTREGAS REALIZADAS:")
entregas.show(truncate=False)

resumo_entregas = entregas.groupBy("produto").agg(
    count("*").alias("quantidade_entregas")
)

print("RESUMO DE ENTREGAS POR PRODUTO:")
resumo_entregas.show(truncate=False)

# Cruza as vendas com as entregas usando o produto
vendas_entregas = vendas_por_produto.join(
    resumo_entregas,
    on="produto",
    how="left"
).fillna(0, subset=["quantidade_entregas"])

print("CRUZAMENTO DE VENDAS E ENTREGAS:")
vendas_entregas.show(truncate=False)