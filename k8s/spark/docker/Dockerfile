FROM apache/spark-py:v3.3.0 AS base

USER root

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    build-essential \
    software-properties-common

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH

WORKDIR ${SPARK_HOME}

ARG SPARK_DEFAULTS_CONF=spark-defaults.conf


# Install python deps
FROM base AS pyspark-base

COPY requirements.txt .
RUN pip3 install -r requirements.txt


FROM pyspark-base AS pyspark

COPY ${SPARK_DEFAULTS_CONF} "${SPARK_HOME}/conf/spark-defaults.conf"


FROM pyspark as spark-iceberg

ARG MAVEN_REPO=https://repo1.maven.org/maven2/org
ARG MAVEN_iceberg_REPO="${MAVEN_REPO}/apache/iceberg"
ARG SPARK_MAJOR_VERSION=3.3
ARG SCALA_VERSION=2.12

ARG ICEBERG_VERSION=1.4.3
ARG ICEBERG_SPARK_SCALA="iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12"
ARG JAR_PACKAGE="${ICEBERG_SPARK_SCALA}-${ICEBERG_VERSION}.jar"

ARG POSTGRES_VERSION=42.6.0

# Download iceberg spark runtime
RUN wget ${MAVEN_iceberg_REPO}/${ICEBERG_SPARK_SCALA}/${ICEBERG_VERSION}/${JAR_PACKAGE} -O ${SPARK_HOME}/jars/${JAR_PACKAGE}

# Download Java AWS bundle
RUN wget ${MAVEN_iceberg_REPO}/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar -O ${SPARK_HOME}/jars/iceberg-aws-bundle-${ICEBERG_VERSION}.jar

# Install PostgreSQL JDBC Driver
RUN wget $MAVEN_REPO/postgresql/postgresql/$POSTGRES_VERSION/postgresql-$POSTGRES_VERSION.jar \
    -O $SPARK_HOME/jars/postgresql-$POSTGRES_VERSION.jar


ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*