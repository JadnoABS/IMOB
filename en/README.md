# IMOB 
##  Real estate lead capture and distribution

> **The heart of real-time lead capture and distribution for real estate agencies.**

[🇧🇷 Leia em Português](../README.md)

![Project Status](https://img.shields.io/badge/Status-Under%20development-yellow?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.14+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Kafka](https://img.shields.io/badge/Apache_Kafka-4.3.0-231F20?style=for-the-badge&logo=apache-kafka)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-4EA94B?style=for-the-badge&logo=mongodb)
![Redis](https://img.shields.io/badge/Redis-Alpine-DC382D?style=for-the-badge&logo=redis)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

---

## 📖 About the Project

**IMOB** is a distributed system designed to solve the challenge of high-scale real estate lead ingestion and processing. Built from the perspective of the *Twelve-Factor App* methodology, the system focuses on bringing excellence and simplicity to the daily lives of realtors through technology and observability.

The architecture is divided into two main microservices:
1. **Capture API:** Responsible for receiving, validating via Pydantic, persisting the raw data, and quickly publishing the event to the message broker.
2. **Processing Worker:** A resilient consumer that reacts to events, ensuring notification delivery without duplication through idempotency control and implementing a readiness check for Kafka.

---

## ✨ Main Features

* **🚀 Asynchronous Ingestion:** API built with FastAPI and non-blocking processing via Motor (MongoDB async) for maximum throughput.
* **📨 Resilient Messaging:** Robust integration with Apache Kafka for service decoupling and delivery guarantee.
* **🛡️ Idempotency:** State control using Redis to ensure no lead is notified in duplicate during message broker *retry* scenarios.
* **📊 Structured Observability:** Centralized and standardized JSON logs for easy ingestion into Logstash, plus metrics exported natively to Prometheus/Grafana.
* **🐳 Infrastructure as Code:** Complete orchestration of the development and testing environment using Docker Compose and Makefile.

---

## 📋 Prerequisites

To run this project on your machine, you will only need:

* `docker`
* `docker-compose`
* `make`

---

## ⚙️ Installation & Execution Guide

The entire ecosystem (database, cache, messaging, and microservices) is automated via Make. Follow the steps below:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/JadnoABS/IMOB](https://github.com/JadnoABS/IMOB)
   cd IMOB
   ```

2. **Setup the environment:**
   Run the command below to automatically create the `.env` and `.env.test` files from the sample file:
   ```bash
   make setup
   ```

3. **Start the infrastructure and applications:**
   ```bash
   make rebuild
   ```
   *(Docker will start MongoDB, Redis, and Kafka. The API and Worker will automatically wait for Kafka to be healthy before connecting).*

4. **Watch the logs in real-time:**
   ```bash
   make logs
   ```
   *(To view specific services, use `make logs-api` or `make logs-worker`).*

5. **Run the test suite (via isolated ephemeral container):**
   ```bash
   make test
   ```

6. **Clean the environment (Caches, Pytest, etc.):**
   ```bash
   make clean
   ```
   *(To destroy everything, including database volumes, use `make deep-clean`).*

---

## 💻 Usage / Demonstration

With the application running, the API will be available on port `8000`. You can access the interactive documentation (Swagger UI) by navigating to:
👉 `http://localhost:8000/docs`

**Example Lead creation request via cURL:**
```bash
curl -X 'POST' \
  'http://localhost:8000/leads' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Jadno Barbosa",
  "email": "_@jadno.tech",
  "phone": "77777777777",
  "property_id": "IMO-8472"
}'
```

**Expected Behavior:**

1. The API will return `HTTP 201 Created`.
2. The data will be persisted in MongoDB.
3. An event will be published to the Kafka topic.
4. The Worker will consume the event, validate duplication in Redis, and log the simulated notification dispatch in the console.

---

## 🛠️ Technologies Used

* **Language:** Python >= 3.14
* **API Framework:** FastAPI, Uvicorn, Pydantic
* **Database / Cache:** MongoDB 7.0 (via Motor Async), Redis Alpine
* **Messaging:** Apache Kafka 4.3.0 (Confluent-Kafka, KRaft mode)
* **Testing:** Pytest (executed via Docker Profiles)
* **DevOps / SRE:** Docker Compose (v3.8), Makefile, JSON Logging, Prometheus Instrumentator

---

## 📞 Contact

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/YOUR_LINKEDIN/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/YOUR_USERNAME/)
