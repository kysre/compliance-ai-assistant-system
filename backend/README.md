
# Backend README

## Overview

This is the backend service for the Compliance AI Assistant System, a Django-based REST API that provides intelligent compliance consulting services. The system helps users navigate regulatory requirements through an AI-powered chat interface with access to a comprehensive knowledge base of regulations and laws.

## Architecture

The backend is built using Django 5.1  and consists of two main applications:

### Core Applications

1. **Compliance App** (`compliance/`) - Manages regulatory data and knowledge base
   - Handles regulation storage and retrieval
   - Provides compliance consulting services through AI integration

2. **Chats App** (`chats/`) - Manages conversational interfaces
   - Handles user chat sessions with thread-based conversations
   - Supports user and assistant message roles
   - Manages chat users and message history

### Key Features

- **Multi-language Support**: Configured for Persian (Farsi) language
- **REST API**: Built with Django REST Framework with token authentication
- **CORS Support**: Configured for cross-origin requests
- **Date Support**: Jalali calendar integration for Persian dates

## Technology Stack

- **Framework**: Django 5.1.7 with Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Knowledge Graph**: Neo4j with LightRAG integration
- **AI Integration**: OpenAI-compatible APIs for embeddings and LLM
- **Containerization**: Docker with multi-stage builds
- **Language**: Python 3.11

## Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (for production)
- Neo4j (for graph database)

### Local Development Setup

1. **Install Dependencies**:

   ```bash
   make install
   ```

2. **Environment Configuration**:
   Copy and configure environment variables:

   ```bash
   cp .env.sample .env
   ```

3. **Database Setup**:

   ```bash
   make migrations
   ```

4. **Run Development Server**:

   ```bash
   make run-admin-local
   ```

## Environment Variables

Key environment variables that need to be configured:

### Django Configuration

- `DJANGO_SETTINGS_MODULE`: Django settings module
- `ALLOWED_HOSTS`: Allowed host domains
- `DATABASE_*`: PostgreSQL connection settings

### AI Integration

- `EMBEDDING_MODEL`: Text embedding model (e.g., text-embedding-3-large)
- `EMBEDDING_BASE_URL`: OpenAI-compatible embedding API endpoint
- `LLM_MODEL`: Language model for chat responses
- `LLM_BASE_URL`: OpenAI-compatible LLM API endpoint

### Knowledge Graph

- `NEO4J_URI`: Neo4j database connection
- `POSTGRES_*`: PostgreSQL settings for LightRAG

## Docker Deployment

The backend includes Docker configuration for containerized deployment:

```bash
docker build -t compliance-ai-backend .
docker run -p 8000:8000 compliance-ai-backend
```

### Docker Features

- Multi-stage build optimization
- Health check endpoint configuration
- Static files collection
- Production-ready gunicorn setup

## Development Workflow

### Code Quality Tools

The project includes several make targets for code quality:

- `make format-check`: Check code formatting with Black
- `make format-fix`: Auto-format code with Black
- `make import-check`: Check import order with isort
- `make import-fix`: Fix import order with isort

### Data Management

- `make import-rules`: Import regulatory rules into the knowledge graph
- `make messages`: Compile translation messages for Persian localization

## Testing & Benchmarking

The backend includes comprehensive benchmarking tools in the `benchmark/` directory:

- Performance evaluation notebooks
- Sample test data for different AI models
- Evaluation results for various retrieval strategies (global, local, hybrid, naive)

## API Structure

The API follows REST conventions with token-based authentication. Main endpoints include:

You're asking me to add the API endpoints for the `chats` app to the README. Based on the codebase context, the `chats` app provides authentication and conversation management functionality.

Here's the updated API Endpoints section for the README:

## API Endpoints

### Compliance API

- `GET /api/compliance/regulations/` - List regulations with pagination
- `POST /api/compliance/regulations/` - Create new regulation

### Chats API

#### Authentication

- `POST /api/chats/register/` - User registration
- `POST /api/chats/login/` - User authentication and token generation

#### Thread Management

- `GET /api/chats/threads/` - List user's conversation threads
- `POST /api/chats/threads/` - Create new thread (or reuse empty thread)
- `DELETE /api/chats/threads/<uuid:thread_id>/` - Delete specific thread

#### Message Management

- `GET /api/chats/threads/<uuid:thread_id>/messages/` - Get messages for a thread
- `POST /api/chats/threads/<uuid:thread_id>/messages/` - Send message and get AI response

**Note**
All endpoints except registration and login require token authentication.

The chats app implements smart thread reuse to avoid creating empty threads unnecessarily, and includes automatic thread title generation based on the first message content. The system integrates with LightRAG for AI-powered responses and supports various query modes for different types of compliance analysis.

## Utilities

- **Web Scraping**: Utility for regulatory data collection
- **Management Commands**: Custom Django management commands for data import and processing

## Notes

- The system is specifically designed for Persian/Farsi language compliance requirements
- It integrates with LightRAG for advanced knowledge graph functionality
- The architecture supports both development (SQLite) and production (PostgreSQL) database configurations
- The system uses UUID-based primary keys for enhanced security and scalability in distributed environments
- Docker health checks are configured to ensure service availability in production deployments
