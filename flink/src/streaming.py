
import json
import happybase
from datetime import datetime

from pyflink.common import Types, WatermarkStrategy, Duration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.file_system import (
    FileSource,
    StreamFormat,
)
from pyflink.datastream.window import SlidingEventTimeWindows
from pyflink.datastream.functions import MapFunction
from pyflink.common.time import Time


class ConverterEvento(MapFunction):
    def map(self, linha):
        evento = json.loads(linha)

        data = datetime.fromisoformat(evento["timestamp"])
        timestamp = int(data.timestamp() * 1000)

        return (
            timestamp,
            evento["tipo_evento"],
            float(evento["valor"]),
        )


class ExtrairTimestamp:
    def extract_timestamp(self, evento, record_timestamp):
        return evento[0]


class GravarAlertaHBase(MapFunction):
    def map(self, alerta):
        total = alerta[0]
        mensagem = alerta[1]

        if total > 5000:
            conexao = happybase.Connection("hbase", 9090)
            conexao.open()

            try:
                tabela = conexao.table("alertas")

                timestamp = datetime.now().isoformat()
                row_key = f"alerta-{timestamp}".encode()

                tabela.put(
                    row_key,
                    {
                        b"dados:mensagem": mensagem.encode(),
                        b"dados:valor": f"{total:.2f}".encode(),
                        b"dados:timestamp": timestamp.encode(),
                    },
                )

                print(
                    f"Alerta gravado no HBase: {row_key.decode()}"
                )

            finally:
                conexao.close()

        return mensagem


def main():
    ambiente = StreamExecutionEnvironment.get_execution_environment()
    ambiente.set_parallelism(1)

    fonte = FileSource.for_record_stream_format(
        StreamFormat.text_line_format(),
        "/opt/flink/data/eventos.jsonl",
    ).process_static_file_set().build()

    eventos = ambiente.from_source(
        fonte,
        WatermarkStrategy.no_watermarks(),
        "Leitura de eventos JSON",
    )

    eventos_convertidos = eventos.map(
        ConverterEvento(),
        output_type=Types.TUPLE([
            Types.LONG(),
            Types.STRING(),
            Types.DOUBLE(),
        ]),
    )

    eventos_com_tempo = eventos_convertidos.assign_timestamps_and_watermarks(
        WatermarkStrategy
        .for_bounded_out_of_orderness(Duration.of_seconds(5))
        .with_timestamp_assigner(ExtrairTimestamp())
    )

    compras = eventos_com_tempo.filter(
        lambda evento: evento[1] == "compra"
    )

    resultado = (
        compras
        .map(
            lambda evento: evento[2],
            output_type=Types.DOUBLE(),
        )
        .window_all(
            SlidingEventTimeWindows.of(
                Time.seconds(10),
                Time.seconds(5)
            )
        )
        .reduce(lambda valor1, valor2: valor1 + valor2)
    )

    alertas = resultado.map(
        lambda total: (
            total,
            (
                f"ALERTA DE VENDAS: R$ {total:.2f}"
                if total > 5000
                else f"Vendas na janela: R$ {total:.2f}"
            ),
        ),
        output_type=Types.TUPLE([
            Types.DOUBLE(),
            Types.STRING(),
        ]),
    )

    alertas_hbase = alertas.map(
        GravarAlertaHBase(),
        output_type=Types.STRING(),
    )   

    alertas_hbase.print()

    ambiente.execute("Processamento de compras com Flink")


if __name__ == "__main__":
    main()