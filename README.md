# RAG-Based Chatbot for Healthcare Policies

## Overview
This project implements a **Retrieval-Augmented Generation (RAG) chatbot** using **LangChain, OpenAI LLMs, Weaviate (Vector Database), Kafka, Spark, PostgreSQL, FastAPI, and React.js**. It provides real-time responses to healthcare policy queries with efficient information retrieval and updates.

## Features
- **LLM-powered chatbot** using OpenAI GPT-4.
- **Weaviate vector database** for semantic search.
- **Kafka integration** for real-time policy updates.
- **Apache Spark processing** for handling large datasets.
- **PostgreSQL database** for structured data storage.
- **FastAPI backend** for chatbot API.
- **React.js frontend** for user interaction.
- **Docker & Docker Compose** setup for deployment.
- **Azure-ready deployment files**.

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL 13+
- Kafka & Spark setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo/rag-chatbot.git
cd rag-chatbot
```

### Step 2: Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Setup PostgreSQL Database
```bash
sudo -u postgres psql -c "CREATE DATABASE healthcare_policies;"
sudo -u postgres psql -d healthcare_policies -f database/schema.sql
```

### Step 4: Start Kafka and Spark Services
```bash
# Start Zookeeper
zookeeper-server-start.sh config/zookeeper.properties &

# Start Kafka Server
kafka-server-start.sh config/server.properties &

# Start Spark Session
pyspark
```

### Step 5: Run the Backend API
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 6: Install Frontend Dependencies & Run
```bash
cd frontend
npm install
npm start
```

### Step 7: Deploy using Docker
```bash
docker-compose up --build
```

## Usage
- Access the chatbot at `http://localhost:3000`.
- Use API for policy retrieval at `http://localhost:8000/docs`.

## Deployment
- Can be deployed on **Azure** using **Azure Container Instances** or **Azure Kubernetes Service (AKS)**.
- Modify `docker-compose.yaml` to match your cloud environment.

---
For any issues, create a ticket in the GitHub repository.

