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

The project uses Docker Compose to run the required services. 

### Basic commands:

To create and run the docker compose

- docker compose up --build		            

To verify if the container and the model are running.

- docker ps -a		                        

To enter the container

- docker exec -it "nome_do_container" bash	

To see the models (execute command inside the container)

- ollama list                                


### To access the API
http://localhost:8000/
http://localhost:8000/docs

### To ask a question directly
http://localhost:8000/ask?prompt="Insert your question here"  (Without quotes "")

---------------------------------------------------------------------------------------------------------------------------------------------

# Em português:

Um assistente conversacional construído com FastAPI e LangChain que ajuda os usuários com tarefas de registro e configuração.

## Visão geral

### Em desenvolvimento.

Este projeto implementa um assistente conversacional que pode:
- Manipular fluxos de registro de usuários
- Processar solicitações de configuração
- Fornecer respostas estruturadas usando cadeias de LLM
- Executar em um ambiente contêinerizado com Docker

## Tech Stack

- FastAPI - Framework para construção de APIs
- LangChain - Framework para desenvolvimento de aplicações LLM
- Docker - Plataforma de contêineres
- Ollama - Runtime LLM local (opcional)
- OpenAI GPT Models - Provedor de LLM em nuvem

## Iniciando

O projeto usa Docker Compose para executar os serviços necessários. 

### Comandos básicos:

Para criar e rodar o docker compose: 

- docker compose up --build		            


Para verificar se o contêiner e o modelo estão em execução.

- docker ps -a		                        

Para entrar no contêiner

- docker exec -it "nome_do_container" bash	

Para ver os modelos (execute o comando dentro do contêiner)

- ollama list                                


### Para acessar a API

http://localhost:8000/

http://localhost:8000/docs

### Para realizar uma pergunta diretamente

http://localhost:8000/ask?prompt="Insira aqui sua pergunta"  (Sem aspas "")
