#!/bin/bash

# Setup Script for RAG-Based Chatbot

# Step 1: Install Python Dependencies
pip install -r backend/requirements.txt

# Step 2: Setup PostgreSQL Database
sudo -u postgres psql -c "CREATE DATABASE healthcare_policies;"
sudo -u postgres psql -d healthcare_policies -f database/schema.sql

# Step 3: Start Kafka & Spark
zookeeper-server-start.sh config/zookeeper.properties &
kafka-server-start.sh config/server.properties &
pyspark &

# Step 4: Start Backend API
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
cd ..

# Step 5: Start Frontend
cd frontend
npm install
npm start &
cd ..

# Step 6: Deploy with Docker
sudo docker-compose up --build
