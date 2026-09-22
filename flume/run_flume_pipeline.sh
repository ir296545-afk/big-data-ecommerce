
set -e

SEGUNDOS=${1:-30}
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FLUME_CONF="$REPO_ROOT/flume/flume.conf"
STAGING_DIR="$REPO_ROOT/flume/staging"
FLINK_DATA_DIR="$REPO_ROOT/flink/data"

mkdir -p "$STAGING_DIR" "$FLINK_DATA_DIR"

echo "[1/4] Limpando staging anterior..."
rm -f "$STAGING_DIR"/FlumeData.*

echo "[2/4] Subindo Flume (agente 'eventos') por ${SEGUNDOS}s..."
flume-ng agent \
  --conf "$REPO_ROOT/flume/conf" \
  --conf-file "$FLUME_CONF" \
  --name eventos \
  -Dflume.root.logger=INFO,console &

FLUME_PID=$!
sleep "$SEGUNDOS"

echo "[3/4] Parando Flume (PID $FLUME_PID)..."
kill "$FLUME_PID" 2>/dev/null || true
wait "$FLUME_PID" 2>/dev/null || true

echo "[4/4] Movendo arquivo coletado para $FLINK_DATA_DIR/eventos.jsonl..."
ARQUIVO=$(ls -t "$STAGING_DIR"/FlumeData.* 2>/dev/null | head -1)

if [ -z "$ARQUIVO" ]; then
  echo "ERRO: nenhum arquivo encontrado em $STAGING_DIR — verifique se o Flume rodou corretamente."
  exit 1
fi

mv "$ARQUIVO" "$FLINK_DATA_DIR/eventos.jsonl"
echo "OK: eventos.jsonl pronto em $FLINK_DATA_DIR/eventos.jsonl"
echo "Agora é só subir o docker-compose do Flink."
