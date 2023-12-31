# Analyse de la Clientèle d'un Concessionnaire Automobile pour la Recommandation de Modèles de Véhicules
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Apache Hadoop](https://img.shields.io/badge/Apache%20Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black)
![GoLand](https://img.shields.io/badge/GoLand-0f0f0f?&style=for-the-badge&logo=goland&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=flat-square&logo=apachespark&logoColor=black)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)
![Unity](https://img.shields.io/badge/unity-%23000000.svg?style=for-the-badge&logo=unity&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

## Objetifs

Le projet vise à utiliser les connaissances en Big Data, Data Visualization et Machine Learning pour aider un concessionnaire automobile. Les objectifs incluent la recommandation optimale de modèles de véhicules, la catégorisation des véhicules, et la mise en place d'un Data Lake. Il implique également l'utilisation d'Access Drivers, d'un bus de données, d'outils d'analyse, et la création d'un programme Map/Reduce pour adapter un fichier spécifique.

Le projet nécessite l'analyse exploratoire des données, l'identification des catégories de véhicules, la fusion des données clients et immatriculations, et la création d'un modèle de classification. Un rapport détaillé et des scripts sont requis pour documenter les choix, processus et résultats. En résumé, l'objectif est d'optimiser la recommandation de véhicules en utilisant des techniques avancées d'analyse de données.

## Informations
**Durée du projet** : 19 Octobre 2023 - 31 décembre 2023

**Nom des étudiants** :
- AGLAE Sébastien
- BONE Ernesto
- CHIAPPE Mike
- LAPSHINA Valeriia
- VINCENT Yehoudi

**Nom des encadrants** :
- PASQUIER Nicolas
- MOPOLO Gabriel
- SIMONIAN Sergio
- WINKLER Marco

**Vidéos** :
- AGLAE : Grafana - https://youtu.be/9AnevnBoNO8 
- AGLAE : API - https://youtu.be/ERGNREAvZtM 

Tous le projet est hébergé sur **135.181.84.87**.

## Acceder aux outils
Voici les outils:
- Grafana
  - [Acceder au dashboard Grafana](http://135.181.84.87:3000/public-dashboards/3b26974c3fb34f5d83cd0d3deeec0e95)
  - [Documentation](./grafana_sql/description.md)
  - [Requêtes SQL](./grafana_sql)
  - [Projet](./grafana_sql)
![Grafana dashboard](./grafana_sql/grafana_screenshot.png)
- API
  - [Acceder a Postman](https://www.postman.com/red-spaceship-151642/workspace/grails/collection/14060252-3261c536-7dac-4a53-8b8c-6f5cd131cb31?action=share&creator=14060252)
  - [Projet](./data_api)
 
## Techno
Notre stack :
- Postgres
- Mongo
- Sqlite
- Redis
- Spark
- Hadoop
- Nats/Jetstream
- Go
- Python
- Grafana

Nos programmes :
- Données API : go, postgres
- Extracteur de données CO2 : python, spark
- Traitement des données : mongo, redis, python, spark, sqlite, nats
- Insertion de données : mongo, redis, hadoop, python, spark
- Connecteur Databus : go, nats/jetstream
- Visualisation Grafana : postgres

## Description de la hierarchie du projet
```bash
.
├── data_api
├── data_extractor
├── data_treater
├── data_upload
├── databus_connector
├── grafana_sql
├── kafka
├── machine_learning
└── sql_script
```
