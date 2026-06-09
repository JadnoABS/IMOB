# IMOB
## Captura e Distribuição de Leads Imobiliários.

> **O coração da captura e distribuição de leads em tempo real para imobiliárias.**

[🇺🇸 Read this in English](en/README.md)

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.14+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Kafka](https://img.shields.io/badge/Apache_Kafka-4.3.0-231F20?style=for-the-badge&logo=apache-kafka)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-4EA94B?style=for-the-badge&logo=mongodb)
![Redis](https://img.shields.io/badge/Redis-Alpine-DC382D?style=for-the-badge&logo=redis)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

---

## 📖 Sobre o Projeto

O **IMOB** é um sistema distribuído projetado para resolver o desafio de ingestão e processamento de leads imobiliários em alta escala. Construído sob a ótica da metodologia *Twelve-Factor App*, o sistema é focado em trazer excelência e simplicidade para o dia a dia dos corretores por meio de tecnologia e observabilidade.

A arquitetura é dividida em dois microsserviços principais:
1. **API de Captura:** Responsável por receber, validar via Pydantic, persistir o dado bruto e publicar o evento rapidamente no mensageiro.
2. **Worker de Processamento:** Consumidor resiliente que reage aos eventos, garantindo a entrega da notificação sem duplicidade através de um controle de idempotência e implementando checagem de prontidão (Readiness Check) para o Kafka.

---

## ✨ Principais Funcionalidades

* **🚀 Ingestão Assíncrona:** API construída com FastAPI e processamento não-bloqueante via Motor (MongoDB async) para máxima vazão.
* **📨 Mensageria Resiliente:** Integração robusta com Apache Kafka para desacoplamento de serviços e garantia de entrega.
* **🛡️ Idempotência:** Controle de estado utilizando Redis para garantir que nenhum lead seja notificado em duplicidade em cenários de *retry*.
* **📊 Observabilidade Estruturada:** Logs centralizados e padronizados em JSON para fácil ingestão no Logstash, além de métricas exportadas nativamente para Prometheus/Grafana.
* **🐳 Infraestrutura como Código:** Orquestração completa do ambiente de desenvolvimento e testes através do Docker Compose e Makefile.

---

## 📋 Pré-requisitos

Para rodar este projeto na sua máquina, você precisará apenas de:

* `docker`
* `docker-compose`
* `make`

---

## ⚙️ Guia de Instalação e Execução

Todo o ecossistema (banco de dados, cache, mensageria e microsserviços) é orquestrado de forma automatizada via Make. Siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/JadnoABS/IMOB](https://github.com/JadnoABS/IMOB)
   cd IMOB
   ```

2. **Configure o ambiente:**
   Execute o comando abaixo para criar automaticamente os arquivos `.env` e `.env.test` a partir do arquivo de exemplo:
   ```bash
   make setup
   ```

3. **Suba a infraestrutura e as aplicações:**
   ```bash
   make rebuild
   ```
   *(O Docker iniciará o MongoDB, Redis e Kafka. A API e o Worker aguardarão automaticamente o Kafka estar saudável antes de conectarem).*

4. **Acompanhe os logs em tempo real:**
   ```bash
   make logs
   ```
   *(Para ver serviços específicos, use `make logs-api` ou `make logs-worker`).*

5. **Para rodar a suíte de testes (via container efêmero isolado):**
   ```bash
   make test
   ```

6. **Para limpar o ambiente (Caches, Pytest, etc.):**
   ```bash
   make clean
   ```
   *(Para destruir tudo, incluindo os dados dos bancos de dados, use `make deep-clean`).*

---

## 💻 Como Usar / Demonstração

Com a aplicação rodando, a API estará disponível na porta `8000`. Você pode acessar a documentação interativa (Swagger UI) navegando até:
👉 `http://localhost:8000/docs`

**Exemplo de requisição de criação de Lead via cURL:**
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

**Comportamento Esperado:**

1. A API retornará `HTTP 201 Created`.
2. O dado será persistido no MongoDB.
3. Um evento será publicado no tópico do Kafka.
4. O Worker consumirá o evento, validará a duplicidade no Redis e logará o envio da notificação simulada no console.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python >= 3.14
* **API Framework:** FastAPI, Uvicorn, Pydantic
* **Banco de Dados / Cache:** MongoDB 7.0 (via Motor Async), Redis Alpine
* **Mensageria:** Apache Kafka 4.3.0 (Confluent-Kafka, modo KRaft)
* **Testes:** Pytest (executado via Docker Profiles)
* **DevOps / SRE:** Docker Compose (v3.8), Makefile, JSON Logging, Prometheus Instrumentator

---

## 📞 Contato 

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jadno-barbosa/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/JadnoABS/)
