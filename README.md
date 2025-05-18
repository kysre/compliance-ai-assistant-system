# Compliance AI Assistant System

This project is a Compliance Intelligent Assistant System developed as part of a Bachelor's degree program. It leverages Large Language Models (LLMs) and implements Retrieval-Augmented Generation (RAG) to enhance compliance processes and ensure adherence to regulatory requirements.

## Project Structure

The system includes a Django backend with a dedicated compliance application that handles regulatory compliance data management.

## Database Access

### Neo4j Graph Database

- Access the Neo4j web browser at: <http://localhost:7474/browser/>
- Login credentials: neo4j/lightrag
- To visualize the graph structure, run: `MATCH (n) RETURN (n)`

### MongoDB

- View MongoDB data through the MongoDB Express interface: <http://localhost:8081/db/lightrag/>
- Login credentials are configured in the docker-compose file

### Django Admin

- Access the Django administrative interface at: <http://localhost:8000/admin/>
- Use this interface to manage compliance models and application data

## Development Setup

The project uses Docker Compose for containerization of services. See `deployment/docker-compose.yaml` for configuration details.
