# Compliance AI Assistant System

This is a full-stack, microservices-based application designed to provide intelligent compliance consulting services. It features an AI-powered chat interface that helps users navigate regulatory requirements by leveraging a comprehensive knowledge base of regulations and laws.

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Development](#development)
- [License](#license)

## Architecture

The system is built with a microservices architecture, containerized with Docker, and orchestrated with Docker Compose.

- **Frontend**: A [Next.js](https://nextjs.org/) application serving the user interface. It provides a modern, responsive dashboard for users to interact with the AI assistant.
- **Backend**: A [Django](https://www.djangoproject.com/) REST API that manages business logic, user authentication, chat sessions, and communication with the AI service.
- **AI Service (LightRAG)**: A dedicated service that integrates with knowledge graphs ([Neo4j](https://neo4j.com/)), vector databases ([ChromaDB](https://www.trychroma.com/)), and Large Language Models (LLMs) to provide intelligent responses.
- **Databases**:
  - **PostgreSQL**: The primary relational database for the backend service.
  - **Neo4j**: A graph database for storing and querying complex regulatory relationships.
  - **ChromaDB**: A vector database for efficient similarity searches required for embeddings.
- **Reverse Proxy (Nginx)**: An [Nginx](https://www.nginx.com/) server that acts as a reverse proxy, routing incoming traffic to the appropriate frontend or backend service.

## Features

- **AI-Powered Chat Interface**: An interactive chat for compliance-related queries.
- **Comprehensive Knowledge Base**: Manages a vast collection of regulations and laws.
- **User Authentication**: Secure registration and login system.
- **Thread-Based Conversations**: Organizes user interactions into distinct conversation threads.
- **Multi-language Support**: Fully localized for English and Persian (Farsi).
- **Modern UI/UX**: A responsive and intuitive dashboard built with modern web technologies.
- **RESTful API**: A well-structured API for seamless frontend-backend communication.

## Technology Stack

| Component         | Technologies                                                              |
| ----------------- | ------------------------------------------------------------------------- |
| **Frontend**      | Next.js, TypeScript, React, Tailwind CSS, Radix UI, next-intl             |
| **Backend**       | Django, Django REST Framework, Python                                     |
| **AI / ML**       | LightRAG, OpenAI-compatible APIs (for LLMs and Embeddings)                |
| **Databases**     | PostgreSQL (with pgvector), Neo4j, ChromaDB                               |
| **Containerization**| Docker, Docker Compose                                                    |
| **Web Server**    | Nginx                                                                     |

## Project Structure

The monorepo is organized into the following key directories:

```text
.
├── backend/         # Django REST API service
├── frontend/        # Next.js web application
├── deployment/      # Docker Compose and environment configurations
├── nginx/           # Nginx reverse proxy configuration
├── LightRAG/        # AI service submodule/code (RAG with graphs)
├── data/            # Raw scraped & test data
├── databases/       # Local data persistence for databases (mounted via volumes)
└── LICENSE          # Project license
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Deployment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/compliance-ai-assistant-system.git
   cd compliance-ai-assistant-system
   ```

2. **Configure Environment Variables:**
   The system relies on environment variables for configuration. The main configuration file for the AI service is `deployment/lightrag.env`. You may need to provide your own API keys for LLM and embedding services.

3. **Run the application:**
   Use Docker Compose to build and run all the services.

   ```bash
   cd deployment
   docker-compose up --build -d
   ```

4. **Access the application:**
   - The frontend application will be available at `http://localhost:8000`.
   - The backend API is accessible at `http://localhost:8000/api/`.
   - The LightRAG service runs on port `9621`.

## Configuration

- **Service Configuration**: The `deployment/docker-compose.yaml` file defines all the services, networks, and volumes.
- **AI Service**: The `deployment/lightrag.env` file contains critical settings for the LightRAG service, including API keys for LLMs, database connections, and model parameters.
- **Nginx**: The reverse proxy is configured in `nginx/default.conf`.

## Development

For detailed instructions on how to set up a local development environment for the frontend and backend, please refer to their respective README files:

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## License

This project is licensed under the [MIT License](./LICENSE).
