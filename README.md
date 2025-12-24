# Container Design & Deployment - Project #2

## Book Management Microservice

**Student:** Ahmed Wahba (A00336722)
**Module:** Container Design & Deployment
**Date:** December 2025

**Docker Hub:** [wahba87/bookservice](https://hub.docker.com/r/wahba87/bookservice)

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
- Kubernetes (k3s - lightweight Kubernetes distribution)
- Helm 3
- Java 25 (for local development)
- Maven (for local development)

> **Note:** This project uses k3s instead of Minikube. Minikube was causing system freezes on VPS environments due to disk I/O issues ([GitHub #11124](https://github.com/kubernetes/minikube/issues/11124)). k3s runs natively without virtualisation overhead.

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

### Kubernetes with k3s (Port 30080)

```bash
# Install k3s (one-time setup)
curl -sfL https://get.k3s.io | sh -

# Configure kubectl
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config

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

# Access directly via NodePort (no port-forward needed with k3s)
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
# Kibana: http://localhost:47601 (random port for security)
```

> **Security Note:** Elasticsearch and Logstash ports are not exposed publicly. Only Kibana is accessible on a non-standard port to avoid automated scanners.

## Cleanup

```bash
# Docker Compose
docker compose -f docker-compose/docker-compose.yml down -v

# Docker Swarm
docker stack rm bookstack
docker swarm leave --force

# Kubernetes (k3s)
kubectl delete namespace bookservice

# Helm
helm uninstall bookservice -n bookservice

# Uninstall k3s completely (if needed)
/usr/local/bin/k3s-uninstall.sh
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
