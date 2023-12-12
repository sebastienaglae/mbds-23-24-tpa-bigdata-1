#!/bin/bash

echo "Downloading and extracting Kafka connect..."
curl -O https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-jdbc/versions/10.7.4/confluentinc-kafka-connect-jdbc-10.7.4.zip

echo "Extracting Kafka connect..."
unzip confluentinc-kafka-connect-jdbc-10.7.4.zip

echo "Moving to the Kafka connect directory..."
cd confluentinc-kafka-connect-jdbc-10.7.4

echo "Creating the connector configuration file..."
mkdir config
touch config/connector.properties

cat <<EOF > config/connector.properties
name=my-postgres-connector
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
tasks.max=1
connection.url=jdbc:postgresql://your-postgres-host:5432/your-database
connection.user=your-username
connection.password=your-password
mode=timestamp+incrementing
timestamp.column.name=timestamp_column
incrementing.column.name=id
table.whitelist=car_dealer,client,immatriculation,marketing
EOF
