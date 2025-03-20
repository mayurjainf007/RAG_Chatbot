import os
import weaviate
import openai
import json
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from kafka import KafkaProducer, KafkaConsumer
from pyspark.sql import SparkSession
from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI()

# OpenAI API Key
openai.api_key = "your-openai-api-key"

# Connect to Weaviate
client = weaviate.Client("http://localhost:8080")

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize Spark Session
spark = SparkSession.builder.appName("RAGChatbot").getOrCreate()

# Dummy Healthcare Policy Data
data = [
    {"id": 1, "title": "Policy A", "content": "Covers general health expenses including hospitalization."},
    {"id": 2, "title": "Policy B", "content": "Includes maternity benefits and childcare."},
    {"id": 3, "title": "Policy C", "content": "Covers dental and vision care expenses."}
]

def preprocess_and_store_data(data):
    """Converts text into embeddings and stores them in Weaviate."""
    for item in data:
        embedding = OpenAIEmbeddings().embed_documents([item["content"]])[0]
        client.data_object.create(
            {
                "title": item["title"],
                "content": item["content"],
                "embedding": embedding
            },
            class_name="HealthcarePolicy"
        )

# Load data into Weaviate
preprocess_and_store_data(data)

@app.post("/query/")
def query_rag(question: str):
    """Retrieves relevant documents and generates an answer."""
    results = Weaviate(client).similarity_search(question, k=2)
    context = "\n".join([res.page_content for res in results])
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in healthcare policies."},
            {"role": "user", "content": f"Question: {question}\nContext: {context}"}
        ]
    )
    return {"answer": response["choices"][0]["message"]["content"]}

@app.post("/update_policy/")
def update_policy(new_policy: dict):
    """Sends updated policy data to Kafka."""
    producer.send("policy_updates", new_policy)
    return {"message": "Policy update sent."}

# Kafka Consumer to Process Updates
consumer = KafkaConsumer(
    "policy_updates",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    policy = message.value
    preprocess_and_store_data([policy])
    print(f"Updated policy stored: {policy}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
