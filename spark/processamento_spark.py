from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg

spark = SparkSession.builder \
    .appName("BigDataEcommerce") \
    .getOrCreate()

eventos = spark.read.json("spark/dados/eventos.json")

eventos.show(truncate=False)

compras = eventos.filter(col("tipo_evento") == "compra")

print("COMPRAS REALIZADAS:")
compras.show(truncate=False)

vendas_por_produto = compras.groupBy("produto").agg(
    count("*").alias("quantidade_vendas"),
    sum("valor").alias("valor_total"),
    avg("valor").alias("valor_medio")
)

print("RESUMO DE VENDAS POR PRODUTO:")
vendas_por_produto.show(truncate=False)