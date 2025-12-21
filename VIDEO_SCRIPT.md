# Video Script - CDD Project #2
## Ahmed Wahba (A00336722)

---

## DEMO LINKS (Use These During Recording)

| Tool | Health Check | Books API |
|------|--------------|-----------|
| **Docker Compose** | http://128.140.102.126:8080/actuator/health | http://128.140.102.126:8080/api/books |
| **Docker Swarm** | http://128.140.102.126:8081/actuator/health | http://128.140.102.126:8081/api/books |
| **Kubernetes** | http://128.140.102.126:30080/actuator/health | http://128.140.102.126:30080/api/books |

> Note: Each tool uses a different port so they can run in parallel:
> - Compose: 8080, Swarm: 8081, Kubernetes: 30080

---

## INTRO (0:00 - 0:30)

*[Show terminal with project open]*

"Hi, I'm Ahmed. In this demo, I show you my Book Management app. I built it with **Spring Boot 4.0.1** and **Java 25**, the latest LTS version. I deploy it three ways: Docker Compose, Docker Swarm, and Kubernetes. I also demonstrate **ELK stack** for logging and **Helm charts** for Kubernetes - these are **advanced features** mentioned in the assignment. Let me show you."

---

## PART 1: PROJECT OVERVIEW (0:30 - 1:00)

*[Show project structure]*

"Here's my project. The bookservice folder has the Java app. I use **Java 25**, the latest LTS version, **Spring Boot 4.0.1**, and **MySQL 8.4** - all latest stable versions."

*[Point to Dockerfile]*

"My Dockerfile has two stages. Stage one compiles the code. Stage two creates a small image for running. I also run the app as a non-root user - that's a security best practice."

*[Point to folders]*

"These folders have my config files: docker-compose, docker-swarm, and kubernetes."

---

## PART 2: DOCKER COMPOSE (1:00 - 3:30)

*[Go to docker-compose folder]*

"Let's start with Docker Compose. This is the simplest tool."

*[Run: cat docker-compose.yml]*

"I define two services here: MySQL for the database and bookservice for my app. The app waits for MySQL to start before connecting."

*[Run: docker compose up -d]*

"Now I start both containers with one command."

*[Run: docker compose ps]*

"Both containers run. MySQL started first. My app connected and created the database tables."

*[Open browser or curl: http://128.140.102.126:8080/actuator/health]*

"Let me check the health endpoint... Status is UP. Everything works."

*[Open browser or curl: http://128.140.102.126:8080/api/books]*

"Here's the API. It returns book data from the database. Five books loaded automatically."

*[Run: docker compose logs bookservice --tail=5]*

"I can check logs too. Helpful for debugging."

*[Run: docker compose down -v]*

"That's Docker Compose. Simple and fast. Perfect for development."

---

## PART 3: DOCKER SWARM (3:30 - 6:00)

*[In terminal]*

"Now Docker Swarm. Swarm adds clustering and scaling."

*[Run: docker swarm init]*

"First I turn on Swarm mode. My machine becomes a manager node."

*[Run: cat docker-swarm/docker-stack.yml]*

"The stack file looks like Compose, but I add Swarm features. See this deploy section? I set 3 replicas, resource limits, and update rules."

*[Run: docker stack deploy -c docker-swarm/docker-stack.yml bookstack]*

"I deploy the stack."

*[Run: docker service ls]*

"MySQL runs with 1 replica. Bookservice runs with 3 replicas. Swarm balances traffic across all three."

*[Open browser or curl: http://128.140.102.126:8081/actuator/health]*

"The API works through Swarm's load balancer on port 8081."

*[Open browser or curl: http://128.140.102.126:8081/api/books]*

"Books API returns data. Swarm routes to one of the 3 replicas."

*[Run: docker service scale bookstack_bookservice=5]*

"Watch this. I scale to 5 replicas with one command."

*[Run: docker service ps bookstack_bookservice]*

"Now I have 5 replicas. Swarm creates the containers automatically."

*[Run: docker service rollback bookstack_bookservice]*

"If I push a bad update, I can rollback instantly."

*[Run: docker stack rm bookstack && docker swarm leave --force]*

"That's Swarm. Easy setup, good for simpler production systems."

---

## PART 4: KUBERNETES (6:00 - 9:00)

*[In terminal]*

"Now Kubernetes. The most powerful option."

*[Run: minikube status]*

"I use Minikube to run a local Kubernetes cluster."

*[Run: minikube image load bookservice:1.0.0]*

"I load my image into Minikube."

*[Run: cat kubernetes/bookservice-deployment.yaml]*

"Here's my deployment file. I define replicas, resource limits, and health checks. Kubernetes gives you fine control."

*[Run kubectl apply commands]*

"I apply all my YAML files: namespace, secrets, MySQL, and bookservice."

*[Run: kubectl get pods -n bookservice -w]*

"Let me watch the pods start... MySQL first, then bookservice pods. All running now."

*[Open browser or curl: http://128.140.102.126:30080/actuator/health]*

"Kubernetes uses NodePort 30080. Health check shows UP."

*[Open browser or curl: http://128.140.102.126:30080/api/books]*

"Books API works through the NodePort service."

*[Run: kubectl scale deployment bookservice -n bookservice --replicas=5]*

"I scale to 5 replicas."

*[Run: kubectl get pods -n bookservice]*

"Five pods run now."

*[Run: kubectl rollout undo deployment/bookservice -n bookservice]*

"For bad updates, I rollback with one command. Kubernetes starts new pods before stopping old ones - no downtime."

*[Run: helm install bookservice ./helm/bookservice-chart -n bookservice --dry-run]*

"I also have a **Helm chart** - another **advanced feature**. Helm packages Kubernetes configs so I can deploy with one command and pass different values for different environments. This simplifies production deployments significantly."

---

## PART 5: ELK STACK - ADVANCED FEATURE (9:00 - 10:00)

*[Show ELK config briefly]*

"For monitoring, I set up the **ELK stack** - **Elasticsearch 9.2.3**, **Logstash 9.2.3**, and **Kibana 9.2.3**. This is an **advanced feature** from the assignment that demonstrates observability in distributed systems."

*[Run: cat elk/logstash/logstash.conf]*

"Logstash parses my HTTP logs - it extracts the method, endpoint, status code, and response time."

*[Open browser: http://localhost:5601 - Kibana]*

"Here's Kibana. Let me show you the Discover page."

*[Navigate to Discover, select bookservice-logs-* index]*

"I can see all my API requests in real-time. Each log shows the HTTP method, endpoint, status code, and how long it took."

*[Click on a log entry to expand it]*

"I can drill into any request. This is invaluable for debugging production issues."

*[If you have a dashboard, show it briefly]*

"Kibana also lets me build dashboards to visualise trends - like requests per endpoint or error rates over time."

*[Speak to camera]*

"Let me share what I learned from this project.

**What worked well:** Docker Compose let me iterate fast during development. My multi-stage Dockerfile cut the image size in half. Health checks solved the MySQL timing problem - the app now waits for the database before starting.

**Challenges:** The biggest was Kubernetes networking. Understanding ClusterIP versus NodePort took practice. Also, Lombok didn't work with Java 25, so I had to write getters and setters manually.

**My recommendations:**

Docker Compose - use it for development. It's fast and simple. You can rebuild and test in seconds.

Docker Swarm - good for smaller teams. If you already know Docker, Swarm feels natural. Scaling is one command.

Kubernetes - the best for production. Yes, it's complex. But features like auto-scaling and zero-downtime updates are worth it.

For a real project, I'd use Compose for local development, then Kubernetes for production. I'd add a CI/CD pipeline to automate builds and deployments. Helm charts would handle different environments.

The key lesson: start simple and add complexity only when you need it."

---

## OUTRO (9:50 - 10:00)

"Thanks for watching. All my configuration files are in the project submission. I'm Ahmed Wahba, student ID A00336722. If you have questions, the code is well documented."

---

## Recording Tips

- **Talk naturally** - use this script as a guide, not word-for-word
- **Keep moving** - don't wait too long for commands
- **If something fails** - say "let me try that again" and continue
- **Big font** - make terminal text readable
- **Practice once** before recording
- **Stay under 10 minutes** - markers appreciate concise demos
