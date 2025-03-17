FROM python:3.9.2-buster
# FROM openjdk:19-buster

RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

ENV MB_PLUGINS_DIR=/home/plugins/
COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD https://downloads.metabase.com/v0.52.4/metabase.jar /home
ADD https://github.com/MotherDuck-Open-Source/metabase_duckdb_driver/releases/download/0.2.12/duckdb.metabase-driver.jar /home/plugins/

RUN chmod 744 /home/plugins/duckdb.metabase-driver.jar

CMD ["java", "-jar", "/home/metabase.jar"]