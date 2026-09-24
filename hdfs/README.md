# HDFS - Big Data E-commerce

Este diretório contém a configuração do Apache HDFS utilizada no projeto Big Data E-commerce.

O HDFS é responsável pelo armazenamento dos eventos brutos gerados pelo sistema.

Fluxo utilizado:

```text
Gerador Python
      |
      v
Apache Flume
   /       \
  v         v
Flink      HDFS
             |
             v
 /ecommerce/raw/eventos
```

## Estrutura do HDFS

O ambiente utiliza dois serviços:

* NameNode: responsável pelo gerenciamento dos metadados do HDFS.
* DataNode: responsável pelo armazenamento dos blocos de dados.

A configuração utiliza Hadoop 3.2.1 através de containers Docker.

## Portas utilizadas

| Serviço  | Porta | Função                    |
| -------- | ----: | ------------------------- |
| NameNode |  9000 | Comunicação com o HDFS    |
| NameNode |  9870 | Interface web             |
| DataNode |  9864 | Interface web do DataNode |
| DataNode |  9866 | Transferência de blocos   |

## Configuração do endereço do DataNode

Antes de iniciar os containers, é necessário informar o endereço IPv4 da máquina.

No PowerShell, consulte o endereço com:

```powershell
Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null} | Select-Object InterfaceAlias,IPv4Address
```

Depois defina a variável:

```powershell
$env:HDFS_DATANODE_HOSTNAME="SEU_IP"
```

Exemplo:

```powershell
$env:HDFS_DATANODE_HOSTNAME="192.168.3.172"
```

O endereço IP não fica fixado no `docker-compose.yml`, permitindo que o projeto seja executado em máquinas diferentes.

## Iniciar o HDFS

Na raiz do projeto:

```powershell
docker compose -f .\hdfs\docker-compose.yml up -d
```

Verifique os containers:

```powershell
docker compose -f .\hdfs\docker-compose.yml ps
```

Devem estar disponíveis:

```text
ecommerce-namenode
ecommerce-datanode
```

## Interface Web

A interface do NameNode pode ser acessada em:

```text
http://localhost:9870
```

## Diretório dos eventos

Os eventos brutos são armazenados em:

```text
/ecommerce/raw/eventos
```

Para criar o diretório:

```powershell
docker exec ecommerce-namenode hdfs dfs -mkdir -p /ecommerce/raw/eventos
```

## Permissão de escrita

O Flume executado pelo WSL precisa ter permissão para gravar no diretório.

Para identificar o usuario
