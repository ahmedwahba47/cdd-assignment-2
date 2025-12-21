# Project Tracker - Container Design & Deployment Project #2

**Student:** Ahmed Wahba
**Student ID:** A00336722
**Assignment:** Container Design & Deployment Project #2 2025/26

---

## Requirements Checklist

### Part 1: Report (30%)

| Section | Requirement | Status | Notes |
|---------|-------------|--------|-------|
| **1. Introduction** | | | |
| | Explain microservices and containerisation | DONE | Section 1.1 |
| | Discuss role of container orchestration | DONE | Section 1.2 |
| | Describe logging/monitoring for reliability | DONE | Section 1.3 |
| **2. Docker Compose** | | | |
| | Describe Docker Compose and features | DONE | Section 2.1 |
| | Step-by-step deployment | DONE | Section 2.2-2.5 |
| | Create Dockerfile for service | DONE | Multi-stage Dockerfile |
| | Launch 2 containers (service + database) | DONE | bookservice + MySQL |
| | Test API with Postman | DONE | Screenshots needed |
| | Push image to Docker Hub | DONE | Commands shown |
| | Demonstrate management via Compose | DONE | Section 2.6 |
| | Integrate ELK stack | DONE | Section 2.7 |
| | Screenshots and code snippets | PARTIAL | Need actual screenshots |
| **3. Docker Swarm** | | | |
| | Explain Swarm and components | DONE | Section 3.1 |
| | Deploy microservice on Swarm | DONE | Section 3.3-3.4 |
| | Demonstrate scaling | DONE | Section 3.5 |
| | Demonstrate upgrades and rollback | DONE | Section 3.6 |
| | Discuss advantages/limitations | DONE | Section 3.7 |
| | Include Compose files, commands, screenshots | PARTIAL | Need actual screenshots |
| **4. Kubernetes** | | | |
| | Explain K8s and core components | DONE | Section 4.1-4.2 |
| | Deploy service using K8s | DONE | Section 4.4-4.5 |
| | Demonstrate scaling, upgrades, rollback | DONE | Section 4.6-4.7 |
| | Discuss features, scalability, learning curve | DONE | Section 4.9 |
| | Include YAML files and commands | DONE | Section 4.4 |
| | Explore Helm charts | DONE | Section 4.8 |
| **5. Evaluation** | | | |
| | Reflect on experience | DONE | Section 5.2 |
| | Evaluate ease of use, scalability, flexibility | DONE | Section 5.1 |
| | Identify what worked/didn't work | DONE | Section 5.2 |
| | Production recommendations | DONE | Section 5.3 |

### Report Quality Requirements (Marking Rubric)

| Criteria | Target | Status |
|----------|--------|--------|
| Logical structure | Clear sections following assignment | DONE |
| Consistent formatting | Professional appearance | IN PROGRESS |
| Valid references | Proper citations | DONE |
| Effective visuals (tables/diagrams) | Charts, tables, architecture diagrams | IN PROGRESS |
| Evidence of own work | Original code and configurations | DONE |
| ELK integration shown | Screenshots/explanation | DONE |
| Helm charts included | Chart structure and usage | DONE |
| Thoughtful evaluation | Trade-offs discussion | DONE |
| AI assistance acknowledged | Required citation at end | DONE |

---

## Identified Gaps & Fixes

### GAP 1: Java Version - RESOLVED
- **Previous:** Java 17 LTS
- **Updated to:** Java 25 LTS (latest LTS release)
- **Status:** DONE - pom.xml and Dockerfile updated to Java 25
- **Note:** Removed Lombok dependency (incompatible with Java 25) and added manual getters/setters.

### GAP 2: Report Format
- **Issue:** Current report is markdown, need PDF
- **Action:** Create Python script to generate professional PDF
- **Features needed:**
  - Cover page with student details
  - Table of contents
  - Professional formatting
  - Embedded tables and diagrams
  - Page numbers

### GAP 3: Visual Elements
- **Issue:** Need more charts/graphs, should look human-made
- **Action:** Add matplotlib-generated charts:
  - Orchestration comparison bar chart
  - Architecture diagrams (keep ASCII for human feel)
  - Feature comparison table with visual styling

### GAP 4: Screenshots Placeholders
- **Issue:** Report has placeholder text for screenshots
- **Action:** These will be actual screenshots from screencast demo

### GAP 5: Deployment Validation - IN PROGRESS
- **Issue:** Need to actually run and validate all 3 orchestration tools
- **Requirements:**
  - Docker and Docker Compose installed
  - Docker Swarm mode available
  - Minikube for Kubernetes testing
  - kubectl CLI tool
  - Helm 3.x installed
- **Status:** Running validation tests

---

## Environment Requirements

### Required Tools

| Tool | Minimum Version | Purpose | Install Command |
|------|-----------------|---------|-----------------|
| Docker | 24.x+ | Container runtime | `sudo apt install docker.io` |
| Docker Compose | 2.x+ | Multi-container orchestration | Included with Docker |
| Minikube | 1.32+ | Local Kubernetes cluster | `curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && sudo install minikube-linux-amd64 /usr/local/bin/minikube` |
| kubectl | 1.28+ | Kubernetes CLI | `sudo snap install kubectl --classic` |
| Helm | 3.13+ | Kubernetes package manager | `sudo snap install helm --classic` |
| Maven | 3.9+ | Java build tool | `sudo apt install maven` |
| Java | 25 | JDK for building | Eclipse Temurin 25 |

### Validation Status

| Orchestration Tool | Status | Notes |
|--------------------|--------|-------|
| Docker Compose | VALIDATED | 2 containers running, API tested |
| Docker Swarm | VALIDATED | Stack deployed, scaled to 5 replicas |
| Kubernetes (Minikube) | VALIDATED | Deployed, scaled, tested API |
| ELK Stack | PENDING | Logging integration |
| Helm Chart | PENDING | Chart installation |

---

## File Structure

```
cdd2/
├── bookservice/               # Java Spring Boot microservice
│   ├── Dockerfile             # Multi-stage build
│   ├── pom.xml               # Maven config (Java 17)
│   └── src/                  # Source code
├── docker-compose/           # Compose configs
│   ├── docker-compose.yml    # Main compose file
│   └── docker-compose-elk.yml # With ELK stack
├── docker-swarm/             # Swarm stack
│   └── docker-stack.yml      # Stack deployment
├── kubernetes/               # K8s manifests
│   ├── namespace.yaml
│   ├── mysql-*.yaml          # Database resources
│   ├── bookservice-*.yaml    # Service resources
│   └── kustomization.yaml
├── helm/                     # Helm chart
│   └── bookservice-chart/
├── elk/                      # ELK configs
│   └── logstash/
├── report/                   # NEW: Report generation
│   └── generate_report.py    # PDF generator
├── REPORT.md                 # Source content
├── PROJECT_TRACKER.md        # This file
└── Assignment_2_25_PT.pdf    # Assignment spec
```

---

## PDF Report Specifications

**Filename:** `AhmedWahba_A00336722_CDD_Project2.pdf`

**Cover Page:**
- Assignment: Container Design & Deployment Project #2 2025/26
- Student Name: Ahmed Wahba
- Student ID: A00336722
- Module: Container Design & Deployment
- Date: January 2026

**Structure:**
1. Cover Page
2. Table of Contents
3. Introduction (1.5 pages)
4. Docker Compose Deployment (3 pages)
5. Docker Swarm Deployment (2.5 pages)
6. Kubernetes Deployment (3 pages)
7. Evaluation & Conclusion (2 pages)
8. References
9. AI Acknowledgment

**Design Guidelines:**
- Clean, professional look
- Tables with subtle borders (not overly styled)
- Simple bar charts (not complex infographics)
- Consistent headings
- Code blocks with light background
- Page numbers in footer

---

## Next Steps

1. [x] Review all requirements from assignment PDF
2. [x] Create project tracker
3. [x] Create Python PDF generator
4. [x] Generate professional PDF with charts
5. [x] Final review of content accuracy
6. [x] Test PDF regeneration

---

## Generated Files

| File | Description |
|------|-------------|
| `AhmedWahba_A00336722_CDD_Project2.pdf` | Final report (14 pages) |
| `report/generate_report.py` | Python script to regenerate PDF |
| `PROJECT_TRACKER.md` | This tracking document |

## How to Regenerate PDF

```bash
cd /home/ahmed/ws/cdd2
python3 report/generate_report.py
```

The PDF will be generated at: `AhmedWahba_A00336722_CDD_Project2.pdf`

---

## Testing Requirements

### Automated Tests (run before submission)

| Test | Command | Expected |
|------|---------|----------|
| Build JAR | `cd bookservice && mvn clean package` | BUILD SUCCESS |
| Docker Build | `docker build -t bookservice:test ./bookservice` | Image created |
| Compose Up | `cd docker-compose && docker-compose up -d` | 2 containers running |
| API Health | `curl http://localhost:8080/actuator/health` | {"status":"UP"} |
| API Books | `curl http://localhost:8080/api/books` | JSON array |
| Compose Down | `docker-compose down -v` | Clean shutdown |

### Manual Verification (for screencast)

- [ ] Docker Compose: Services start, API responds
- [ ] Docker Swarm: Init, deploy stack, scale, rollback
- [ ] Kubernetes: Apply manifests, scale, update, rollback
- [ ] ELK Stack: Kibana accessible, logs visible
- [ ] Helm: Install chart, upgrade, rollback

### Run Test Script

```bash
./scripts/test_deployment.sh
```

---

*Last Updated: December 2025*
