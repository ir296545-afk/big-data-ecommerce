FROM openeuler/hbase:2.6.5-oe2403sp3

RUN yum install -y hostname && \
    yum clean all && \
    rm -rf /var/cache/yum

COPY start-hbase.sh /usr/local/bin/start-hbase.sh

RUN chmod +x /usr/local/bin/start-hbase.sh