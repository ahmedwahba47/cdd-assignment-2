# Container Design & Deployment - Project #2

## Book Management Microservice

**Student:** Ahmed Wahba (A00336722)
**Module:** Container Design & Deployment
**Date:** December 2025

A Java Spring Boot microservice for managing books, demonstrating container orchestration with Docker Compose, Docker Swarm, and Kubernetes.

## Tech Stack

- **Java 25 LTS** with Spring Boot 4.0.1
- **MySQL 8.4 LTS** for database
- **Docker** for containerization
- **ELK Stack** (Elasticsearch, Logstash, Kibana) for logging

## Project Structure

```
cdd2/
├── bookservice/              # Java Spring Boot Application
│   ├── src/
│   ├── pom.xml
│   └── Dockerfile
├── docker-compose/           # Docker Compose configurations
│   ├── docker-compose.yml
│   ├── docker-compose-elk.yml
│   └── init-db.sql
├── docker-swarm/             # Docker Swarm configuration
│   └── docker-stack.yml
├── kubernetes/               # Kubernetes manifests
│   ├── namespace.yaml
│   ├── mysql-*.yaml
│   ├── bookservice-*.yaml
│   └── kustomization.yaml
├── helm/                     # Helm chart
│   └── bookservice-chart/
├── elk/                      # ELK stack configuration
│   └── logstash/
├── report/                   # PDF report generator
│   └── generate_report.py
├── scripts/                  # Test scripts
│   └── test_deployment.sh
└── postman/                  # Postman collection
```

## Prerequisites

- Docker & Docker Compose
- Kubernetes (Minikube recommended)
- Helm 3
- Java 25 (for local development)
- Maven (for local development)

## Quick Start

### Build the Docker Image

```bash
cd bookservice
docker build -t bookservice:1.0.0 .
```

### Docker Compose (Port 8080)

```bash
cd docker-compose
docker compose up -d
# Access: http://localhost:8080/api/books
```

### Docker Swarm (Port 8081)

```bash
docker swarm init
docker stack deploy -c docker-swarm/docker-stack.yml bookstack
# Access: http://localhost:8081/api/books
```

### Kubernetes (Port 30080)

```bash
# Start minikube and load image
minikube start --driver=docker
minikube image load bookservice:1.0.0

# Apply all manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/mysql-secret.yaml
kubectl apply -f kubernetes/mysql-configmap.yaml
kubectl apply -f kubernetes/mysql-pvc.yaml
kubectl apply -f kubernetes/mysql-deployment.yaml
kubectl apply -f kubernetes/mysql-service.yaml
kubectl apply -f kubernetes/bookservice-configmap.yaml
kubectl apply -f kubernetes/bookservice-deployment.yaml
kubectl apply -f kubernetes/bookservice-service.yaml

# Port forward for access
kubectl port-forward -n bookservice service/bookservice 30080:8080 --address 0.0.0.0 &
# Access: http://localhost:30080/api/books
```

### Helm

```bash
helm install bookservice ./helm/bookservice-chart -n bookservice --create-namespace
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/books | Get all books (includes deployment type) |
| GET | /api/books/{id} | Get book by ID |
| GET | /api/books/isbn/{isbn} | Get book by ISBN |
| GET | /api/books/search/author?q= | Search by author |
| GET | /api/books/search/title?q= | Search by title |
| POST | /api/books | Create new book |
| PUT | /api/books/{id} | Update book |
| DELETE | /api/books/{id} | Delete book |
| GET | /api/books/count | Get book count |
| GET | /actuator/health | Health check |

### Sample Response

```json
{
  "deployment": "docker-compose",
  "books": [
    {
      "id": 1,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "isbn": "978-0132350884",
      "price": 34.99
    }
  ]
}
```

## Running All 3 in Parallel

Each orchestration tool uses a different port:

| Tool | Port |
|------|------|
| Docker Compose | 8080 |
| Docker Swarm | 8081 |
| Kubernetes | 30080 |

## ELK Stack

```bash
cd docker-compose
docker compose -f docker-compose-elk.yml up -d
# Kibana: http://localhost:5601
# Elasticsearch: http://localhost:9200
```

## Cleanup

```bash
# Docker Compose
docker compose -f docker-compose/docker-compose.yml down -v

# Docker Swarm
docker stack rm bookstack
docker swarm leave --force

# Kubernetes
kubectl delete namespace bookservice

# Helm
helm uninstall bookservice -n bookservice
```

## Generate PDF Report

```bash
cd report
python3 generate_report.py
```

## Author

Ahmed Wahba (A00336722) - Container Design & Deployment Module

## License

This project is for educational purposes.
