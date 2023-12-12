#!/bin/bash

echo "Moving to the Kafka directory..."
cd kafka_2.13-3.6.1

echo "Starting Connect Distributed..."
bin/connect-distributed.sh config/connect-distributed.properties

# Register the JDBC connector
# curl -X POST -H "Content-Type: application/json" --data @config/connector.properties http://localhost:8083/connectors
