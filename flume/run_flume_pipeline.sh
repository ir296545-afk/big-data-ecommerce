#!/usr/bin/env bash

set -e

SEGUNDOS=${1:-30}

# Caminho raiz do repositorio
export REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

FLUME_CONF="$REPO_ROOT/flume/flume.conf"
STAGING_DIR="$REPO_ROOT/flume/staging"
FLINK_DATA_DIR="$REPO_ROOT/flink/data"

# Diretorio de configuracao do Flume/Hadoop
FLUME_CONF_DIR="${FLUME_CONF_DIR:-/opt/flume/conf}"

# Verifica se o endereco do HDFS foi informado
if [ -z "${HDFS_HOST:-}" ]; then
  echo "ERRO: HDFS_HOST nao definido."
  echo 'Exemplo: export HDFS_HOST="192.168.3.172"'
  exit 1
fi

# Verifica se as bibliotecas Hadoop foram informadas
if [ -z "${HADOOP_CP:-}" ]; then
  echo "ERRO: HADOOP_CP nao definido."
  echo "Defina o classpath das bibliotecas Hadoop antes de executar."
  exit 1
fi

# Cria diretorios necessarios
mkdir -p "$STAGING_DIR" "$FLINK_DATA_DIR"

# Marcador para identificar somente arquivos gerados nesta execucao
RUN_MARKER="$STAGING_DIR/.flume_run_start"
touch "$RUN_MARKER"

echo "[1/4] Preparando diretorios..."
echo "Staging: $STAGING_DIR"
echo "Flink:   $FLINK_DATA_DIR"

echo "[2/4] Subindo Flume (agente 'eventos') por ${SEGUNDOS}s..."

flume-ng agent \
  --classpath "$HADOOP_CP" \
  --conf "$FLUME_CONF_DIR" \
  --conf-file "$FLUME_CONF" \
  --name eventos \
  -Dflume.root.logger=INFO,console &

FLUME_PID=$!

sleep "$SEGUNDOS"

echo "[3/4] Parando Flume (PID $FLUME_PID)..."

kill "$FLUME_PID" 2>/dev/null || true
wait "$FLUME_PID" 2>/dev/null || true

echo "[4/4] Procurando arquivo gerado para o Flink..."

ARQUIVO=$(
  find "$STAGING_DIR" \
    -maxdepth 1 \
    -type f \
    -newer "$RUN_MARKER" \
    ! -name ".flume_run_start" \
    -printf '%T@ %p\n' 2>/dev/null |
  sort -nr |
  head -1 |
  cut -d' ' -f2-
)

rm -f "$RUN_MARKER"

if [ -z "$ARQUIVO" ]; then
  echo "ERRO: nenhum arquivo novo foi encontrado em $STAGING_DIR."
  echo "Verifique os logs do Flume."
  exit 1
fi

mv "$ARQUIVO" "$FLINK_DATA_DIR/eventos.jsonl"

echo "OK: eventos.jsonl pronto em:"
echo "$FLINK_DATA_DIR/eventos.jsonl"

echo ""
echo "Fluxo executado:"
echo "Gerador -> Flume -> staging/Flink"
echo "                 -> HDFS"