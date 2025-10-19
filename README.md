# AutoChef
This repository contains the API layers for AutoChef - a GenAI-powered Recipe Generator.

## Services
- **Java API Gateway** (`autochefjavaservice/`) - Spring Boot service that acts as a gateway
- **Python LLM Service** (`autochefpythonservice/`) - FastAPI service for recipe generation

## Quick Start

Java API Gateway : cd autochefjavaservice
./mvnw spring-boot:run

Python Fast API Server : cd autochefpythonservice
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 5001 --reload
