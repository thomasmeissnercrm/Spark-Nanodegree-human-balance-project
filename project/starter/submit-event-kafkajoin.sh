#!/bin/bash
docker exec -it spark-nanodegree-human-balance_spark_1 /opt/bitnami/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 /home/thomas/IdeaProjects/Spark-Nanodegree-human-balance/project/starter/submit-event-kafkajoin.sh | tee ../../spark/logs/kafkajoin.log