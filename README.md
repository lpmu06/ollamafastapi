A conversational AI assistant built with FastAPI and LangChain that helps users with registration and configuration tasks.

## Overview

### In development.

This project implements a chatbot assistant that can:
- Handle user registration flows
- Process configuration requests 
- Provide structured responses using LLM chains
- Run in containerized environment with Docker

## Tech Stack

- FastAPI - Web framework for building APIs
- LangChain - Framework for developing LLM applications
- Docker - Containerization platform
- Ollama - Local LLM runtime (optional)
- OpenAI GPT Models - Cloud LLM provider

## Getting Started

The project uses Docker Compose to run the required services. Basic commands:

docker compose up --build		            # Para rodar o docker compose

# To verify if the container and the model are running.
docker ps -a		                        # To see the containers
docker exec -it "nome_do_container" bash	# To enter the container
ollama list                                 # To see the models (execute command inside the container)


# To access the API
http://localhost:8000/ask?prompt="Olá, como vai?"  #Without quotes ""

