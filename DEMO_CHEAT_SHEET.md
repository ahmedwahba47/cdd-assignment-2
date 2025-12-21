# Demo Cheat Sheet - 10 Minute Screencast

**Student:** Ahmed Wahba (A00336722)
**Total Time:** 10 minutes MAX
**Public IP:** 128.140.102.126

---

## DEMO LINKS (Test These Before Recording)

| Tool | Health Check | Books API |
|------|--------------|-----------|
| **Docker Compose** | http://128.140.102.126:8080/actuator/health | http://128.140.102.126:8080/api/books |
| **Docker Swarm** | http://128.140.102.126:8081/actuator/health | http://128.140.102.126:8081/api/books |
| **Kubernetes** | http://128.140.102.126:30080/actuator/health | http://128.140.102.126:30080/api/books |

> **All 3 can run in parallel!** Each uses a different port: Compose (8080), Swarm (8081), K8s (30080)

---

## PRE-DEMO SETUP (Do Before Recording)

```bash
# Clean up any previous runs
cd /home/ahmed/ws/cdd2
docker compose -f docker-compose/docker-compose.yml down -v 2>/dev/null
docker swarm leave --force 2>/dev/null
kubectl delete namespace bookservice 2>/dev/null

# Pre-pull images (saves time during demo)
docker pull mysql:8.4
docker pull eclipse-temurin:25-jre-alpine

# Build the image
cd bookservice && docker build -t bookservice:1.0.0 . && cd ..

# Start minikube and load image
minikube start --driver=docker
minikube image load bookservice:1.0.0
```

---

## DEMO FLOW (Follow This Exactly)

### PART 1: INTRO (1 minute)

**What to say:**
> "Hi, I'm Ahmed Wahba. This demo shows deploying a Book Management microservice using three orchestration tools: Docker Compose, Docker Swarm, and Kubernetes."

**Show on screen:**
- Open VS Code with project folder
- Quickly show the folder structure

**Commands to show structure:**
```bash
ls -la
ls bookservice/src/main/java/com/cdd/bookservice/
```

---

### PART 2: DOCKER COMPOSE (2.5 minutes)

**What to say:**
> "First, Docker Compose. It's the simplest tool - great for development. Let me show the config file."

**Step 1 - Show config:**
```bash
cat docker-compose/docker-compose.yml
```
Point out: service names, ports, depends_on, volumes

**Step 2 - Start services:**
```bash
cd docker-compose
docker compose up -d
```

**Step 3 - Check status:**
```bash
docker compose ps
```
Wait for both containers to show "healthy"

**Step 4 - Test API (use public IP in browser):**
```bash
curl http://128.140.102.126:8080/actuator/health
curl http://128.140.102.126:8080/api/books
```

**Step 5 - Show logs:**
```bash
docker compose logs bookservice --tail=10
```

**Step 6 - Stop (for next section):**
```bash
docker compose down -v
cd ..
```

---

### PART 3: DOCKER SWARM (2.5 minutes)

**What to say:**
> "Now Docker Swarm. It adds clustering and scaling. Same containers, but now I can run multiple replicas."

**Step 1 - Initialize Swarm:**
```bash
docker swarm init
```

**Step 2 - Show stack file:**
```bash
cat docker-swarm/docker-stack.yml
```
Point out: deploy section, replicas, update_config

**Step 3 - Deploy stack:**
```bash
docker stack deploy -c docker-swarm/docker-stack.yml bookstack
```

**Step 4 - Wait and check services:**
```bash
sleep 45  # Wait for MySQL to be ready
docker service ls
docker service ps bookstack_bookservice
```

**Step 5 - Test API (use public IP in browser):**
```bash
curl http://128.140.102.126:8081/actuator/health
curl http://128.140.102.126:8081/api/books
```

**Step 6 - SCALE (Important!):**
```bash
docker service scale bookstack_bookservice=5
docker service ps bookstack_bookservice
```
> "See how Swarm spreads replicas automatically"

**Step 7 - Show rollback capability:**
```bash
docker service rollback bookstack_bookservice
```

**Step 8 - Cleanup:**
```bash
docker stack rm bookstack
docker swarm leave --force
```

---

### PART 4: KUBERNETES (3 minutes)

**What to say:**
> "Finally Kubernetes - the most powerful but also most complex. It has more features like auto-scaling and declarative configs."

**Step 1 - Check minikube:**
```bash
minikube status
```

**Step 2 - Show manifest:**
```bash
cat kubernetes/bookservice-deployment.yaml
```
Point out: replicas, resources, livenessProbe

**Step 3 - Deploy all resources:**
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/mysql-secret.yaml
kubectl apply -f kubernetes/mysql-configmap.yaml
kubectl apply -f kubernetes/mysql-pvc.yaml
kubectl apply -f kubernetes/mysql-deployment.yaml
kubectl apply -f kubernetes/mysql-service.yaml
kubectl apply -f kubernetes/bookservice-configmap.yaml
kubectl apply -f kubernetes/bookservice-deployment.yaml
kubectl apply -f kubernetes/bookservice-service.yaml
```

**Step 4 - Check pods:**
```bash
kubectl get pods -n bookservice -w
```
Wait for pods to be Running (press Ctrl+C when ready)

**Step 5 - Expose via port-forward (run in background):**
```bash
kubectl port-forward -n bookservice service/bookservice 30080:8080 --address 0.0.0.0 &
```

**Step 6 - Test API (use public IP in browser):**
```bash
curl http://128.140.102.126:30080/actuator/health
curl http://128.140.102.126:30080/api/books
```

**Step 7 - SCALE:**
```bash
kubectl scale deployment bookservice -n bookservice --replicas=5
kubectl get pods -n bookservice
```

**Step 8 - Show rollback:**
```bash
kubectl rollout undo deployment/bookservice -n bookservice
```

**Step 9 - Show Helm (ADVANCED FEATURE - important!):**
```bash
ls helm/bookservice-chart/
cat helm/bookservice-chart/values.yaml
helm install bookservice ./helm/bookservice-chart -n bookservice --dry-run
```
> Say: "**Helm charts** are an **advanced feature**. They template Kubernetes configs for easy deployment across environments."

---

### PART 5: ELK STACK - ADVANCED FEATURE (1 minute)

**What to say:**
> "For monitoring, I integrated the **ELK stack** using **Elasticsearch 9.2.3**, **Logstash 9.2.3**, and **Kibana 9.2.3**. This is an **advanced feature** for the assignment."

**PRE-REQUISITE - Start ELK before recording (takes ~2 min to initialise):**
```bash
# Start main app first (if not already running)
cd /home/ahmed/ws/cdd2
docker compose -f docker-compose/docker-compose.yml up -d

# Start ELK stack
docker compose -f docker-compose/docker-compose-elk.yml up -d

# Wait for Elasticsearch to be healthy (~60 seconds)
docker compose -f docker-compose/docker-compose-elk.yml ps

# Generate some logs by hitting the API
curl http://localhost:8080/api/books
curl http://localhost:8080/api/books/1
curl http://localhost:8080/api/books/count
curl http://localhost:8080/api/books/search/author?q=Martin
```

**Step 1 - Show Logstash config:**
```bash
cat elk/logstash/logstash.conf
```

> "Logstash parses my HTTP logs - extracts method, endpoint, status code, and response time."

**Step 2 - Open Kibana in browser:**
- URL: `http://localhost:5601` (or `http://128.140.102.126:5601` if remote)
- Wait for Kibana to load (may take 30 seconds on first access)

**Step 3 - Create Index Pattern (first time only):**
- Click hamburger menu (☰) → **Stack Management** → **Data Views**
- Click **Create data view**
- Name: `bookservice-logs-*`
- Index pattern: `bookservice-logs-*`
- Timestamp field: `@timestamp`
- Click **Save data view to Kibana**

**Step 4 - Navigate to Discover:**
- Click hamburger menu (☰) → **Analytics** → **Discover**
- Select `bookservice-logs-*` from the dropdown (top left)
- Set time range to "Last 15 minutes" (top right)

**Step 5 - Explore logs:**
- Show the log entries in the table
- Click on one entry to expand it
- Point out fields: `method`, `endpoint`, `status_code`, `duration_ms`, `client_ip`
- Say: "I can see all API requests in real-time. Each log shows HTTP method, endpoint, status, and response time."

**Step 6 - (Optional) Add columns to view:**
- Click **+ Add column** and add: `method`, `endpoint`, `status_code`, `duration_ms`
- Shows a cleaner table view

**Step 7 - (Optional) Show Dashboard:**
- If you created a dashboard, navigate to **Analytics** → **Dashboard**
- Say: "Kibana lets me build dashboards to visualise trends - requests per endpoint, error rates over time."

> "This is invaluable for debugging production issues."

**Cleanup after demo:**
```bash
docker compose -f docker-compose/docker-compose-elk.yml down -v
docker compose -f docker-compose/docker-compose.yml down -v
```

---

### PART 6: CONCLUSION (30 seconds)

**What to say:**
> "To summarize: Docker Compose is best for development - simple and fast. Docker Swarm adds multi-node scaling with minimal learning curve. Kubernetes is most powerful but takes more effort to learn. For production, I'd recommend Kubernetes for its auto-scaling and self-healing capabilities. Thanks for watching."

---

## QUICK REFERENCE - Key Commands

| Tool | Start | Scale | Stop |
|------|-------|-------|------|
| Compose | `docker compose up -d` | N/A (dev only) | `docker compose down` |
| Swarm | `docker stack deploy -c file.yml name` | `docker service scale name=5` | `docker stack rm name` |
| K8s | `kubectl apply -f .` | `kubectl scale deployment name --replicas=5` | `kubectl delete -f .` |

---

## IF SOMETHING GOES WRONG

**Compose won't start:**
```bash
docker compose down -v
docker compose up -d --build
```

**Swarm service stuck:**
```bash
docker service rm bookstack_bookservice
docker stack deploy -c docker-swarm/docker-stack.yml bookstack
```

**K8s pods not starting:**
```bash
kubectl describe pod -n bookservice
kubectl logs <pod-name> -n bookservice
```

**Port-forward not working:**
```bash
# Kill existing port-forward
pkill -f "port-forward"
# Start again
kubectl port-forward -n bookservice service/bookservice 30080:8080 --address 0.0.0.0 &
```

**Minikube issues:**
```bash
minikube delete
minikube start --driver=docker
minikube image load bookservice:1.0.0
```

**ELK stack not starting:**
```bash
# Check status
docker compose -f docker-compose/docker-compose-elk.yml ps

# Check Elasticsearch logs (usually the bottleneck)
docker compose -f docker-compose/docker-compose-elk.yml logs elasticsearch

# Restart ELK stack
docker compose -f docker-compose/docker-compose-elk.yml down -v
docker compose -f docker-compose/docker-compose-elk.yml up -d
```

**Kibana shows "Kibana server is not ready yet":**
- Wait 60-90 seconds for Elasticsearch to fully initialise
- Check Elasticsearch is healthy: `curl http://localhost:9200/_cluster/health`

**No logs appearing in Kibana Discover:**
```bash
# Check if logs exist
docker compose -f docker-compose/docker-compose.yml logs bookservice --tail=20

# Check Logstash is processing
docker compose -f docker-compose/docker-compose-elk.yml logs logstash --tail=20

# Generate fresh logs
curl http://localhost:8080/api/books

# Check Elasticsearch has data
curl http://localhost:9200/bookservice-logs-*/_count
```

**Index pattern not found:**
- Make sure you've generated some API requests first
- Wait 10-15 seconds for Logstash to process and send to Elasticsearch
- Refresh the Data Views page in Kibana

---

## TIMING CHECKPOINTS

| Time | Section |
|------|---------|
| 0:00 | Start intro |
| 1:00 | Start Docker Compose |
| 3:30 | Start Docker Swarm |
| 6:00 | Start Kubernetes |
| 9:00 | Start ELK/Conclusion |
| 10:00 | END |

**TIPS:**
- Don't read from script, speak naturally
- If a command fails, stay calm, explain what happened
- Focus on SCALING - that's what markers want to see
- Keep terminal font large so it's readable
- Record in a quiet place with good audio
- Open browser tabs with the URLs ready before recording
