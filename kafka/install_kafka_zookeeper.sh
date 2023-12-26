#!/bin/bash

echo "Downloading and extracting Kafka..."
curl -O https://downloads.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz

echo "Extracting Kafka..."
tar -xzf kafka_2.13-3.6.1.tgz