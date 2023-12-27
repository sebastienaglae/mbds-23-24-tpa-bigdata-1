#!/bin/bash
echo "Moving to the Kafka directory..."
cd kafka_2.13-3.6.1

echo "Starting Kafka..."
bin/kafka-server-start.sh config/server.properties