# Trabalho Prático AP1 — Arquitetura de Big Data em Tempo Real

## Big Data — Sistemas de Informação

Projeto desenvolvido para a disciplina de Big Data.

### Tema

Monitoramento de vendas e logística de um e-commerce por meio de uma arquitetura de Big Data capaz de realizar processamento em tempo real (streaming) e processamento em lote (batch).

## Integrantes — Grupo 7

- Heldemar Soares Braga
- Juan Carlos Ribeiro Vieira
- Nívia Lara Camurça de Oliveira Lima
- José Ivan Luz Ramos
- Francisco Guilherme Mata Santos

## Arquitetura do projeto

O pipeline de dados seguirá o seguinte fluxo:

```text
gerador.py
    ↓
Apache Flume
    ├──→ Apache Flink → HBase
    │
    └──→ HDFS → Apache Spark → Hive
