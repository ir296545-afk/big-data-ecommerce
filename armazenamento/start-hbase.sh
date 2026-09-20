#!/bin/sh

/usr/local/hbase/bin/start-hbase.sh

echo "HBase iniciado. Mantendo o container em execução..."

tail -f /dev/null