# Container Design & Deployment Project Report

## Book Management Microservice

**Module:** Container Design & Deployment
**Assignment:** Project #2 2025/26 – Springboard
**Student:** Ahmed Wahba
**Date:** January 2026
**GitHub Repository:** https://github.com/ahmedwahba47/cdd-assignment-2

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Docker Compose Deployment](#2-docker-compose-deployment)
3. [Docker Swarm Deployment](#3-docker-swarm-deployment)
4. [Kubernetes Deployment](#4-kubernetes-deployment)
5. [Evaluation & Conclusion](#5-evaluation--conclusion)
6. [References](#6-references)

---

## 1. Introduction

### 1.1 Microservices and Containerisation

**Microservices architecture** is a software design approach where applications are structured as a collection of loosely coupled, independently deployable services. Each service:

- **Handles a specific business capability** - Single responsibility principle
- **Is independently deployable** - Can be updated without affecting other services
- **Is technology agnostic** - Different services can use different languages/databases
- **Is independently scalable** - Scale only what needs scaling

**Containerisation** packages applications and their dependencies into isolated, portable units called containers. Key benefits include:

| Benefit | Description |
|---------|-------------|
| **Consistency** | Same environment from development to production |
| **Isolation** | Applications run in isolated environments without conflicts |
| **Portability** | Containers run on any platform supporting the container runtime |
| **Efficiency** | Lightweight compared to virtual machines (shared OS kernel) |
| **Rapid deployment** | Containers start in seconds, not minutes |

In this project, I developed a **Book Management Microservice** using **Java 25** with **Spring Boot 4.0.1** that provides RESTful APIs for CRUD operations on a book inventory, backed by a **MySQL 8.4** database.

### 1.2 The Role of Container Orchestration

Container orchestration automates the deployment, management, scaling, and networking of containers in distributed environments. As microservice architectures grow, manual container management becomes impractical. Orchestration provides:

| Function | Description |
|----------|-------------|
| **Scheduling** | Deciding which nodes run which containers based on resources |
| **Service Discovery** | Enabling containers to find and communicate with each other dynamically |
| **Load Balancing** | Distributing traffic across container instances for reliability |
| **Scaling** | Adjusting container count based on demand (manual or automatic) |
| **Self-healing** | Automatically replacing failed containers to maintain desired state |
| **Rolling Updates** | Deploying updates without downtime using gradual replacement |
| **Configuration Management** | Centralised management of environment variables and secrets |

This project explores three orchestration tools with increasing complexity:
1. **Docker Compose** - Single-host multi-container orchestration
2. **Docker Swarm** - Native Docker clustering and orchestration
3. **Kubernetes** - Industry-standard production orchestration

### 1.3 Logging and Monitoring in Distributed Systems

Observability is critical in distributed microservice systems because:

- **Distributed debugging** - Requests span multiple services, making traditional debugging insufficient
- **Performance monitoring** - Identifying bottlenecks across service boundaries
- **Compliance and audit** - Maintaining logs for regulatory requirements
- **Proactive alerting** - Detecting issues before they impact users
- **Root cause analysis** - Understanding cascading failures

The **ELK Stack** (Elasticsearch, Logstash, Kibana) provides comprehensive observability:

| Component | Role |
|-----------|------|
| **Elasticsearch** | Distributed search and analytics engine for storing and querying logs |
| **Logstash** | Log pipeline for collecting, parsing, transforming, and forwarding logs |
| **Kibana** | Visualisation dashboard for exploring, analysing, and creating dashboards |

By integrating ELK, we achieve centralised logging across all microservice instances, enabling real-time monitoring and historical analysis.

---

## 2. Docker Compose Deployment

### 2.1 What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications using a declarative YAML configuration file. Main features include:

- **Declarative configuration** - Define services, networks, and volumes in a single YAML file
- **Single-host orchestration** - Manage multiple containers on one machine
- **Environment management** - Easy configuration via environment variables and `.env` files
- **Dependency management** - Control service startup order with `depends_on`
- **Volume persistence** - Maintain data across container restarts
- **Network isolation** - Containers communicate via user-defined networks

### 2.2 Microservice Architecture

The Book Management application consists of two containers:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│  ┌─────────────────┐         ┌─────────────────┐        │
│  │   BookService   │   ───►  │     MySQL       │        │
│  │   (Port 8080)   │         │   (Port 3306)   │        │
│  │                 │         │                 │        │
│  │  Spring Boot    │         │   bookdb        │        │
│  │  Java 25        │         │   mysql:8.4     │        │
│  └─────────────────┘         └─────────────────┘        │
│           │                          │                   │
│           ▼                          ▼                   │
│     app_logs volume           mysql_data volume          │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Dockerfile (Multi-stage Build)

I created a multi-stage Dockerfile for optimised image builds:

```dockerfile
# Stage 1: Build Stage
FROM maven:3.9-eclipse-temurin-25 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime Stage
FROM eclipse-temurin:25-jre-alpine
LABEL maintainer="CDD Assignment"
LABEL version="1.0.0"
LABEL description="Book Management Microservice"

# Security: Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
RUN mkdir -p /app/logs && chown -R appuser:appgroup /app
COPY --from=builder /app/target/*.jar app.jar
RUN chown appuser:appgroup app.jar
USER appuser
EXPOSE 8080

# Health check for orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget -q --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Key Design Decisions:**
- **Multi-stage build** - Separates build dependencies from runtime, reducing image from ~400MB to ~180MB
- **Non-root user** - Security best practice to limit container privileges
- **Health check** - Enables orchestrators to monitor container health
- **Alpine base** - Minimal image size while maintaining compatibility

### 2.4 Docker Compose Configuration

```yaml
version: '3.8'

services:
  # MySQL Database Service
  mysql:
    image: mysql:8.4
    container_name: bookdb
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: bookdb
      MYSQL_USER: bookuser
      MYSQL_PASSWORD: bookpass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - bookservice-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-prootpassword"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    restart: unless-stopped

  # Book Microservice
  bookservice:
    build:
      context: ../bookservice
      dockerfile: Dockerfile
    image: bookservice:1.0.0
    container_name: bookservice
    environment:
      MYSQL_HOST: mysql
      MYSQL_PORT: 3306
      MYSQL_DATABASE: bookdb
      MYSQL_USER: bookuser
      MYSQL_PASSWORD: bookpass
    ports:
      - "8080:8080"
    volumes:
      - app_logs:/app/logs
    networks:
      - bookservice-network
    depends_on:
      mysql:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: unless-stopped

networks:
  bookservice-network:
    driver: bridge
    name: bookservice-network

volumes:
  mysql_data:
    name: bookservice-mysql-data
  app_logs:
    name: bookservice-logs
```

### 2.5 Step-by-Step Deployment

**Step 1: Build and Start Services**
```bash
cd docker-compose
docker-compose up -d --build
```

**Step 2: Verify Containers Running**
```bash
docker-compose ps
docker-compose logs -f bookservice
```

*[Screenshot: Terminal showing both containers running with healthy status]*

**Step 3: Test API with Postman**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/books | Get all books |
| GET | /api/books/{id} | Get book by ID |
| GET | /api/books/isbn/{isbn} | Get book by ISBN |
| POST | /api/books | Create new book |
| PUT | /api/books/{id} | Update book |
| DELETE | /api/books/{id} | Delete book |
| GET | /api/books/health | Health check |
| GET | /actuator/health | Spring Actuator health |

**Sample POST Request:**
```json
{
    "title": "Docker Deep Dive",
    "author": "Nigel Poulton",
    "isbn": "978-1916585256",
    "price": 29.99,
    "description": "Zero to Docker in a single book",
    "publishedYear": 2023,
    "quantity": 25
}
```

*[Screenshot: Postman showing successful POST request creating a new book]*

*[Screenshot: Postman showing GET request returning list of books]*

**Step 4: Push Image to Docker Hub**
```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag bookservice:1.0.0 ahmedwahba/bookservice:1.0.0

# Push to Docker Hub
docker push ahmedwahba/bookservice:1.0.0
```

*[Screenshot: Docker Hub showing pushed bookservice image]*

### 2.6 Docker Compose Management Commands

```bash
# View running services
docker-compose ps

# View logs (follow mode)
docker-compose logs -f bookservice

# Stop services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# Restart specific service
docker-compose restart bookservice

# View resource usage
docker-compose top
```

### 2.7 ELK Stack Integration (Advanced Feature)

> **Note:** ELK stack integration is an **advanced/optional feature** that demonstrates observability best practices for distributed systems, as highlighted in the assignment objectives.

The application writes HTTP request logs to `/app/logs/test.log` which are processed by the ELK stack (**Elasticsearch 9.2.3**, **Logstash 9.2.3**, **Kibana 9.2.3**).

**Application Logging Filter (Java):**
```java
@Component
public class LoggingFilter implements Filter {
    private static final String LOG_FILE_PATH = "/app/logs/test.log";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        long startTime = System.currentTimeMillis();
        chain.doFilter(request, response);
        long duration = System.currentTimeMillis() - startTime;

        String logEntry = String.format("%s | %s | %s %s | Status: %d | Duration: %dms | IP: %s",
                LocalDateTime.now().format(formatter),
                httpRequest.getProtocol(),
                httpRequest.getMethod(),
                httpRequest.getRequestURI(),
                httpResponse.getStatus(),
                duration,
                httpRequest.getRemoteAddr());

        writeToLogFile(logEntry);
    }
}
```

**Logstash Configuration:**
```conf
input {
  file {
    path => "/app/logs/test.log"
    start_position => "beginning"
    type => "bookservice-http"
  }
}

filter {
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} \| %{DATA:protocol} \| %{WORD:method} %{URIPATH:endpoint} \| Status: %{NUMBER:status_code:int} \| Duration: %{NUMBER:duration:int}ms \| IP: %{IP:client_ip}"
    }
  }
  date {
    match => ["timestamp", "yyyy-MM-dd HH:mm:ss"]
    target => "@timestamp"
  }
  mutate {
    add_field => { "service" => "bookservice" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "bookservice-logs-%{+YYYY.MM.dd}"
  }
}
```

**Start ELK Stack:**
```bash
docker-compose -f docker-compose-elk.yml up -d
```

**Access Kibana:** `http://localhost:5601`

*[Screenshot: Kibana Discover page showing parsed HTTP request logs with method, endpoint, status_code, and duration fields]*

*[Screenshot: Kibana Dashboard with visualisations showing request counts by endpoint and average response times]*

---

## 3. Docker Swarm Deployment

### 3.1 What is Docker Swarm?

Docker Swarm is Docker's native container orchestration tool that enables clustering of Docker hosts into a single virtual host. Core components include:

| Component | Description |
|-----------|-------------|
| **Manager Nodes** | Control cluster state, schedule services, serve Swarm API. Maintain consensus using Raft. |
| **Worker Nodes** | Execute container tasks assigned by managers. Report status back to managers. |
| **Services** | Declarative definition of desired state (image, replicas, ports, etc.) |
| **Tasks** | Individual container instances scheduled on nodes |
| **Overlay Network** | Multi-host networking enabling container communication across nodes |
| **Ingress Network** | Built-in load balancing for routing external traffic to services |

### 3.2 Swarm Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Swarm Cluster                  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Manager    │  │   Worker 1   │  │   Worker 2   │   │
│  │              │  │              │  │              │   │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │   │
│  │ │bookservice│ │  │ │bookservice│ │  │ │bookservice│ │   │
│  │ │ replica 1│ │  │ │ replica 2│ │  │ │ replica 3│ │   │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │   │
│  │              │  │              │  │              │   │
│  │ ┌──────────┐ │  │              │  │              │   │
│  │ │  MySQL   │ │  │              │  │              │   │
│  │ └──────────┘ │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                          │
│           ◄─────── Overlay Network ───────►              │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Ingress Load Balancer                │   │
│  │                   (Port 8080)                     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Docker Stack Configuration

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: bookdb
      MYSQL_USER: bookuser
      MYSQL_PASSWORD: bookpass
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - bookservice-network
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  bookservice:
    image: ahmedwahba/bookservice:1.0.0
    environment:
      MYSQL_HOST: mysql
      MYSQL_PORT: 3306
      MYSQL_DATABASE: bookdb
      MYSQL_USER: bookuser
      MYSQL_PASSWORD: bookpass
    ports:
      - "8080:8080"
    volumes:
      - app_logs:/app/logs
    networks:
      - bookservice-network
    deploy:
      mode: replicated
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        monitor: 60s
        order: start-first
      rollback_config:
        parallelism: 1
        delay: 10s
        failure_action: pause
        order: stop-first
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

networks:
  bookservice-network:
    driver: overlay
    attachable: true

volumes:
  mysql_data:
  app_logs:
```

### 3.4 Deployment Steps

**Step 1: Initialize Docker Swarm**
```bash
docker swarm init
# Output: Swarm initialized: current node (xxx) is now a manager.
```

**Step 2: Deploy the Stack**
```bash
docker stack deploy -c docker-stack.yml bookservice-stack
```

**Step 3: Verify Deployment**
```bash
docker stack services bookservice-stack
docker service ps bookservice-stack_bookservice
```

*[Screenshot: Terminal showing stack services with 3/3 replicas running]*

### 3.5 Scaling Demonstration

```bash
# Scale to 5 replicas
docker service scale bookservice-stack_bookservice=5

# Verify scaling
docker service ls

# Watch tasks distributing
docker service ps bookservice-stack_bookservice
```

*[Screenshot: Service scaled to 5/5 replicas across nodes]*

```bash
# Scale down to 2 replicas
docker service scale bookservice-stack_bookservice=2
```

### 3.6 Rolling Updates and Rollback

**Perform Rolling Update:**
```bash
# Update to new image version
docker service update --image ahmedwahba/bookservice:2.0.0 bookservice-stack_bookservice

# Watch update progress
docker service ps bookservice-stack_bookservice
```

*[Screenshot: Rolling update in progress showing old and new task versions]*

**Rollback to Previous Version:**
```bash
# Rollback command
docker service rollback bookservice-stack_bookservice

# Verify rollback
docker service ps bookservice-stack_bookservice
```

*[Screenshot: Service rolled back to previous version]*

### 3.7 Advantages and Limitations of Docker Swarm

| Advantages | Limitations |
|------------|-------------|
| **Native Docker integration** - No additional tools needed | **Limited ecosystem** - Fewer add-ons compared to Kubernetes |
| **Simple setup** - Single command to initialise | **Fewer advanced features** - No native auto-scaling |
| **Low learning curve** - Familiar Docker Compose syntax | **Smaller community** - Less support and resources |
| **Built-in load balancing** - Ingress routing mesh | **Less flexible networking** - Simpler but limited options |
| **Rolling updates/rollbacks** - Built-in deployment strategies | **Limited storage options** - Basic volume support |
| **Service discovery** - Automatic DNS-based discovery | **No built-in monitoring** - Requires external tools |

---

## 4. Kubernetes Deployment

### 4.1 What is Kubernetes?

Kubernetes (K8s) is an open-source container orchestration platform originally developed by Google and now maintained by the Cloud Native Computing Foundation (CNCF). Key capabilities:

- **Automated rollouts and rollbacks** - Declarative updates with automatic failure handling
- **Service discovery and load balancing** - Built-in DNS and traffic distribution
- **Storage orchestration** - Automatic mounting of storage systems
- **Self-healing** - Restarts failed containers, replaces unresponsive nodes
- **Secret and configuration management** - Secure storage and injection of sensitive data
- **Horizontal scaling** - Manual and automatic scaling based on metrics

### 4.2 Core Components

| Component | Description |
|-----------|-------------|
| **Pod** | Smallest deployable unit; one or more containers sharing network/storage |
| **Deployment** | Manages ReplicaSets and provides declarative updates to Pods |
| **Service** | Stable network endpoint abstracting Pod IP addresses |
| **ConfigMap** | Non-sensitive configuration data as key-value pairs |
| **Secret** | Sensitive data (passwords, tokens) stored securely |
| **PersistentVolumeClaim** | Request for storage resources |
| **Namespace** | Virtual cluster for resource isolation and organisation |
| **HorizontalPodAutoscaler** | Automatic scaling based on CPU/memory metrics |

### 4.3 Kubernetes Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    Namespace: bookservice               │ │
│  │                                                         │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │ │
│  │  │  ConfigMap  │    │   Secret    │    │     PVC     │ │ │
│  │  │bookservice- │    │mysql-secret │    │  mysql-pvc  │ │ │
│  │  │   config    │    │             │    │             │ │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘ │ │
│  │         │                  │                  │        │ │
│  │         ▼                  ▼                  ▼        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │              MySQL Deployment (1 replica)         │ │ │
│  │  │  ┌─────────┐                                     │ │ │
│  │  │  │   Pod   │◄────── MySQL Service (ClusterIP)   │ │ │
│  │  │  │ mysql:8 │        mysql:3306                   │ │ │
│  │  │  └─────────┘                                     │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                          │                             │ │
│  │                          ▼                             │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │        BookService Deployment (3 replicas)        │ │ │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐          │ │ │
│  │  │  │  Pod 1  │  │  Pod 2  │  │  Pod 3  │          │ │ │
│  │  │  │bookserv │  │bookserv │  │bookserv │          │ │ │
│  │  │  └─────────┘  └─────────┘  └─────────┘          │ │ │
│  │  │                     │                            │ │ │
│  │  │      BookService Service (NodePort:30080)       │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                                                         │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │     HorizontalPodAutoscaler (min:2, max:10)      │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Key YAML Configuration Files

**Namespace:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: bookservice
  labels:
    app: bookservice
```

**ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: bookservice-config
  namespace: bookservice
data:
  MYSQL_HOST: "mysql"
  MYSQL_PORT: "3306"
  MYSQL_DATABASE: "bookdb"
  MYSQL_USER: "bookuser"
```

**Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: bookservice
type: Opaque
data:
  mysql-root-password: cm9vdHBhc3N3b3Jk  # base64: rootpassword
  mysql-password: Ym9va3Bhc3M=            # base64: bookpass
```

**PersistentVolumeClaim:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: bookservice
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

**BookService Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bookservice
  namespace: bookservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bookservice
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: bookservice
    spec:
      containers:
        - name: bookservice
          image: ahmedwahba/bookservice:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: MYSQL_HOST
              valueFrom:
                configMapKeyRef:
                  name: bookservice-config
                  key: MYSQL_HOST
            - name: MYSQL_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: mysql-password
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 5
```

**Service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: bookservice
  namespace: bookservice
spec:
  type: NodePort
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30080
  selector:
    app: bookservice
```

**HorizontalPodAutoscaler:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bookservice-hpa
  namespace: bookservice
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bookservice
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### 4.5 Deployment Steps

**Step 1: Apply All Manifests**
```bash
cd kubernetes
kubectl apply -k .
```

**Step 2: Verify Deployment**
```bash
kubectl get all -n bookservice
kubectl get pods -n bookservice -w
```

*[Screenshot: kubectl get all showing running pods, services, and deployments]*

### 4.6 Scaling Demonstration

**Manual Scaling:**
```bash
# Scale to 5 replicas
kubectl scale deployment bookservice -n bookservice --replicas=5

# Verify
kubectl get pods -n bookservice
```

*[Screenshot: 5 pods running after manual scaling]*

**Automatic Scaling with HPA:**
```bash
# View HPA status
kubectl get hpa -n bookservice

# Describe HPA for details
kubectl describe hpa bookservice-hpa -n bookservice
```

### 4.7 Rolling Updates and Rollback

**Perform Rolling Update:**
```bash
# Update image
kubectl set image deployment/bookservice bookservice=ahmedwahba/bookservice:2.0.0 -n bookservice

# Watch rollout
kubectl rollout status deployment/bookservice -n bookservice
```

*[Screenshot: Rolling update in progress showing pod replacements]*

**View Rollout History:**
```bash
kubectl rollout history deployment/bookservice -n bookservice
```

**Rollback:**
```bash
# Rollback to previous revision
kubectl rollout undo deployment/bookservice -n bookservice

# Or to specific revision
kubectl rollout undo deployment/bookservice -n bookservice --to-revision=1
```

*[Screenshot: Successful rollback showing previous version restored]*

### 4.8 Helm Charts for Simplified Deployment (Advanced Feature)

> **Note:** Helm chart implementation is an **advanced/optional feature** that demonstrates deployment simplification and infrastructure-as-code best practices.

Helm is the package manager for Kubernetes, providing templated, reusable deployments.

**Chart Structure:**
```
bookservice-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
└── templates/
    ├── _helpers.tpl    # Template helpers
    ├── deployment.yaml # Templated deployment
    ├── service.yaml    # Templated service
    ├── configmap.yaml  # Templated configmap
    ├── secret.yaml     # Templated secret
    └── hpa.yaml        # Templated HPA
```

**Install with Helm:**
```bash
helm install bookservice ./bookservice-chart -n bookservice --create-namespace
```

**Upgrade with Custom Values:**
```bash
helm upgrade bookservice ./bookservice-chart -n bookservice --set replicaCount=5
```

**Rollback with Helm:**
```bash
# View history
helm history bookservice -n bookservice

# Rollback
helm rollback bookservice -n bookservice
```

**Benefits of Helm:**
- **Templating** - Parameterised configurations for different environments
- **Versioning** - Track and manage deployment versions
- **Dependencies** - Manage chart dependencies (e.g., MySQL chart)
- **Rollbacks** - Easy rollback to any previous release
- **Sharing** - Package and share charts via repositories

### 4.9 Kubernetes Features, Scalability, and Learning Curve

| Aspect | Assessment |
|--------|------------|
| **Scalability** | Excellent - handles thousands of nodes and tens of thousands of pods |
| **High Availability** | Built-in with multi-replica deployments and pod anti-affinity |
| **Feature Richness** | Comprehensive - covers all orchestration needs |
| **Ecosystem** | Vast - extensive tools (Istio, Prometheus, ArgoCD, etc.) |
| **Community** | Very large and active, strong enterprise backing |
| **Learning Curve** | Steep - many concepts (pods, services, deployments, ingress, CRDs) |
| **Operational Complexity** | High - requires dedicated expertise for production |

---

## 5. Evaluation & Conclusion

### 5.1 Comparative Analysis

| Feature | Docker Compose | Docker Swarm | Kubernetes |
|---------|---------------|--------------|------------|
| **Setup Complexity** | Low | Medium | High |
| **Learning Curve** | Easy | Moderate | Steep |
| **Scalability** | Single host only | Good (multi-host) | Excellent (thousands of nodes) |
| **High Availability** | No | Yes | Yes |
| **Rolling Updates** | Basic | Yes | Advanced |
| **Auto-scaling** | No | No (manual only) | Yes (HPA) |
| **Service Discovery** | DNS | DNS | DNS + Ingress + Service Mesh |
| **Load Balancing** | Basic | Built-in (ingress mesh) | Advanced (multiple options) |
| **Configuration** | Environment files | Configs/Secrets | ConfigMaps/Secrets |
| **Storage** | Local volumes | Volume plugins | PV/PVC + StorageClasses |
| **Networking** | Bridge networks | Overlay networks | CNI plugins (Calico, Flannel) |
| **Community** | Large | Moderate | Very Large |
| **Best Use Case** | Development | Small-medium production | Enterprise production |

### 5.2 Reflection on Experience

**What Worked Well:**

1. **Docker Compose** provided an excellent local development environment with quick iteration cycles
2. **Multi-stage Dockerfile** reduced image size significantly (~180MB vs ~400MB)
3. **Health checks** across all platforms ensured reliable service discovery
4. **Docker Swarm's simplicity** made the transition from Compose seamless
5. **Kubernetes ConfigMaps and Secrets** cleanly separated configuration from code
6. **Helm charts** dramatically simplified repeated deployments and upgrades
7. **ELK integration** provided valuable insights into application behaviour

**Challenges Encountered:**

1. **MySQL connection timing** - Initial failures due to database not being ready; solved with proper health checks and `depends_on` conditions
2. **Kubernetes networking** - Understanding Services, ClusterIP vs NodePort vs LoadBalancer took time
3. **Secret management** - Base64 encoding is not encryption; would need Sealed Secrets or Vault for production
4. **ELK resource requirements** - Elasticsearch required significant memory; needed to tune JVM heap settings
5. **Helm templating** - Go template syntax has a learning curve

**Key Learnings:**

1. **Start simple, scale complexity** - Begin with Compose for development, graduate to orchestration as needed
2. **Health checks are essential** - They enable orchestrators to make intelligent decisions
3. **Configuration externalisation** - Environment variables and ConfigMaps enable environment-specific deployments
4. **Observability from day one** - Logging and monitoring should be built into the architecture, not added later
5. **Infrastructure as Code** - All configurations should be version controlled and declarative

### 5.3 Production Recommendations

For production-level orchestration, I would recommend:

1. **Use managed Kubernetes** (EKS, GKE, AKS) - Reduces operational overhead of managing control plane
2. **Implement GitOps** with ArgoCD or Flux - Declarative, auditable deployments from Git
3. **Add service mesh** (Istio or Linkerd) - For mTLS, traffic management, and observability
4. **Enhanced monitoring** - Prometheus for metrics, Grafana for dashboards, alongside ELK for logs
5. **Proper secrets management** - HashiCorp Vault or cloud-native solutions (AWS Secrets Manager)
6. **Network policies** - Restrict pod-to-pod communication for security
7. **Pod Disruption Budgets** - Ensure availability during maintenance
8. **Resource quotas** - Prevent runaway resource consumption

### 5.4 Conclusion

This project demonstrated the progression from simple container deployment to enterprise-grade orchestration. Each tool serves a distinct purpose:

- **Docker Compose** excels in development and simple single-host deployments where quick iteration matters
- **Docker Swarm** provides a gentle introduction to multi-host orchestration with familiar Docker concepts
- **Kubernetes** offers the comprehensive feature set required for large-scale, production workloads

The integration of the **ELK stack** highlighted the importance of observability in distributed systems, while **Helm charts** demonstrated how deployment automation can reduce complexity and human error.

The choice of orchestration tool should be driven by team expertise, scale requirements, and operational maturity. For most new projects, I would recommend starting with Docker Compose for development, with a clear path to Kubernetes for production as requirements grow.

---

## 6. References

1. Docker Documentation. (2025). *Docker Compose Overview*. https://docs.docker.com/compose/
2. Docker Documentation. (2025). *Swarm Mode Overview*. https://docs.docker.com/engine/swarm/
3. Kubernetes Documentation. (2025). *Kubernetes Basics*. https://kubernetes.io/docs/tutorials/kubernetes-basics/
4. Elastic. (2025). *Getting Started with the Elastic Stack*. https://www.elastic.co/guide/
5. Helm Documentation. (2025). *Helm - The Package Manager for Kubernetes*. https://helm.sh/docs/
6. Poulton, N. (2023). *Docker Deep Dive*. Nigel Poulton.
7. Luksa, M. (2018). *Kubernetes in Action*. Manning Publications.
8. Burns, B., Beda, J., & Hightower, K. (2019). *Kubernetes: Up and Running*. O'Reilly Media.

---

**AI Assistance Acknowledgment:**

Claude (Anthropic, 2025). Assistance with Docker Compose configuration structure, Kubernetes manifest templates, Helm chart scaffolding, and ELK stack Logstash grok patterns.

---

*Report prepared by Ahmed Wahba for Container Design & Deployment Module - Project #2 2025/26*
