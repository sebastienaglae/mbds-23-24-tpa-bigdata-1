#!/bin/bash
cd kafka_2.13-3.6.1
# Start Zookeeper
echo "Starting Zookeeper..."
bin/zookeeper-server-start.sh config/zookeeper.properties
