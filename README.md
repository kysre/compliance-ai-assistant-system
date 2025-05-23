# Compliance AI Assistant System

This project is a Compliance Intelligent Assistant System developed as part of a Bachelor's degree program. It leverages Large Language Models (LLMs) and implements Retrieval-Augmented Generation (RAG) to enhance compliance processes and ensure adherence to regulatory requirements.

## Project Structure

The system includes a Django backend with a dedicated compliance application that handles regulatory compliance data management.

## Database Access

### pgvector Database

This is a Postgres database used for both the Django backend and lightrag.
On first startup, you should perform the following steps:

- Connect to the database:

  ```sh
  psql -h localhost -U postgres -d postgres -p 5432
  ```

- Then, run the following SQL commands:

  ```postgresql
  CREATE DATABASE lightrag;
  \c lightrag
  CREATE EXTENSION IF NOT EXISTS vector;
  ```

### Neo4j Graph Database

- You can access the [Neo4j web browser](http://localhost:7474/browser/)
- Login credentials: `neo4j/lightrag`
- To visualize the graph structure, run:

```cypher
MATCH (n) RETURN (n)
```

### Django Admin

- You can access the [Django administrative interface](http://localhost:8000/admin/)
- Use this interface to manage compliance models and application data

## Development Setup

The project uses Docker Compose for containerization of services. See `deployment/docker-compose.yaml` for configuration details.
