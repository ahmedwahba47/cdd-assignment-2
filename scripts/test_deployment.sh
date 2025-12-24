#!/bin/bash
# Test script for Container Design & Deployment Project #2
# Student: Ahmed Wahba (A00336722)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=========================================="
echo "CDD Project #2 - Deployment Test Suite"
echo "=========================================="
echo ""

TESTS_PASSED=0
TESTS_FAILED=0

pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++)) || true
}

fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++)) || true
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

info() {
    echo -e "[INFO] $1"
}

# Test 1: Check required files exist
echo "--- Test 1: Required Files ---"
FILES=(
    "bookservice/Dockerfile"
    "bookservice/pom.xml"
    "docker-compose/docker-compose.yml"
    "docker-compose/docker-compose-elk.yml"
    "docker-swarm/docker-stack.yml"
    "kubernetes/bookservice-deployment.yaml"
    "helm/bookservice-chart/Chart.yaml"
)

for file in "${FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        pass "$file exists"
    else
        fail "$file missing"
    fi
done

# Test 2: Check Java version in pom.xml
echo ""
echo "--- Test 2: Java Version ---"
JAVA_VERSION=$(grep -o '<java.version>[0-9]*</java.version>' "$PROJECT_ROOT/bookservice/pom.xml" | grep -o '[0-9]*')
if [ "$JAVA_VERSION" = "25" ]; then
    pass "Java version is 25 (LTS)"
else
    fail "Java version is $JAVA_VERSION (expected 25)"
fi

# Test 3: Check MySQL version in compose files
echo ""
echo "--- Test 3: MySQL Version ---"
MYSQL_VERSION=$(grep 'image: mysql:' "$PROJECT_ROOT/docker-compose/docker-compose.yml" | grep -o 'mysql:[0-9.]*' | head -1)
if [[ "$MYSQL_VERSION" == "mysql:8.4" ]]; then
    pass "MySQL version is 8.4 (LTS)"
else
    warn "MySQL version is $MYSQL_VERSION (recommended: 8.4)"
fi

# Test 4: Check ELK versions
echo ""
echo "--- Test 4: ELK Stack Versions ---"
ELK_VERSION=$(grep 'image: elasticsearch:' "$PROJECT_ROOT/docker-compose/docker-compose-elk.yml" | grep -o 'elasticsearch:[0-9.]*' | head -1)
if [[ "$ELK_VERSION" == *"9.2"* ]] || [[ "$ELK_VERSION" == *"9."* ]]; then
    pass "Elasticsearch version: $ELK_VERSION"
else
    warn "Elasticsearch version: $ELK_VERSION (consider updating to 9.x)"
fi

# Test 5: Check Dockerfile uses Java 25
echo ""
echo "--- Test 5: Dockerfile Java Version ---"
if grep -q "eclipse-temurin:25" "$PROJECT_ROOT/bookservice/Dockerfile"; then
    pass "Dockerfile uses Java 25"
else
    fail "Dockerfile not using Java 25"
fi

# Test 6: Check multi-stage build
echo ""
echo "--- Test 6: Dockerfile Best Practices ---"
if grep -q "AS builder" "$PROJECT_ROOT/bookservice/Dockerfile"; then
    pass "Multi-stage build configured"
else
    fail "Multi-stage build not found"
fi

if grep -q "USER appuser" "$PROJECT_ROOT/bookservice/Dockerfile"; then
    pass "Non-root user configured"
else
    warn "Consider adding non-root user"
fi

if grep -q "HEALTHCHECK" "$PROJECT_ROOT/bookservice/Dockerfile"; then
    pass "Health check configured"
else
    warn "Consider adding health check"
fi

# Test 7: Validate YAML syntax
echo ""
echo "--- Test 7: YAML Syntax Validation ---"
if command -v python3 &> /dev/null; then
    for yaml in docker-compose/docker-compose.yml docker-swarm/docker-stack.yml; do
        if python3 -c "import yaml; yaml.safe_load(open('$PROJECT_ROOT/$yaml'))" 2>/dev/null; then
            pass "$yaml is valid YAML"
        else
            fail "$yaml has invalid YAML syntax"
        fi
    done
else
    warn "Python3 not available for YAML validation"
fi

# Test 8: Check report generator
echo ""
echo "--- Test 8: Report Generator ---"
if [ -f "$PROJECT_ROOT/report/generate_report.py" ]; then
    pass "Report generator exists"
    if python3 -c "from reportlab.lib import colors" 2>/dev/null; then
        pass "reportlab library installed"
    else
        warn "reportlab not installed (run: pip install reportlab)"
    fi
else
    fail "Report generator missing"
fi

# Test 9: Check Kubernetes manifests
echo ""
echo "--- Test 9: Kubernetes Manifests ---"
K8S_FILES=(
    "namespace.yaml"
    "mysql-deployment.yaml"
    "bookservice-deployment.yaml"
    "bookservice-service.yaml"
)
for file in "${K8S_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/kubernetes/$file" ]; then
        pass "kubernetes/$file exists"
    else
        fail "kubernetes/$file missing"
    fi
done

# Test 9b: Check k3s installation
echo ""
echo "--- Test 9b: k3s Installation ---"
if command -v k3s &> /dev/null || [ -f "/usr/local/bin/k3s" ]; then
    pass "k3s is installed"
    if systemctl is-active --quiet k3s 2>/dev/null; then
        pass "k3s service is running"
    else
        warn "k3s service not running (start with: sudo systemctl start k3s)"
    fi
else
    warn "k3s not installed (install with: curl -sfL https://get.k3s.io | sh -)"
fi

# Test 10: Check Helm chart
echo ""
echo "--- Test 10: Helm Chart ---"
if [ -f "$PROJECT_ROOT/helm/bookservice-chart/Chart.yaml" ]; then
    pass "Helm Chart.yaml exists"
fi
if [ -f "$PROJECT_ROOT/helm/bookservice-chart/values.yaml" ]; then
    pass "Helm values.yaml exists"
fi
if [ -d "$PROJECT_ROOT/helm/bookservice-chart/templates" ]; then
    pass "Helm templates directory exists"
else
    fail "Helm templates directory missing"
fi

# Test 11: Deployment Type Environment Variable
echo ""
echo "--- Test 11: Deployment Type Configuration ---"

# Check DEPLOYMENT_TYPE is set in docker-compose.yml
if grep -q "DEPLOYMENT_TYPE: docker-compose" "$PROJECT_ROOT/docker-compose/docker-compose.yml"; then
    pass "DEPLOYMENT_TYPE set in docker-compose.yml"
else
    fail "DEPLOYMENT_TYPE missing in docker-compose.yml"
fi

# Check DEPLOYMENT_TYPE is set in docker-stack.yml
if grep -q "DEPLOYMENT_TYPE: docker-swarm" "$PROJECT_ROOT/docker-swarm/docker-stack.yml"; then
    pass "DEPLOYMENT_TYPE set in docker-stack.yml"
else
    fail "DEPLOYMENT_TYPE missing in docker-stack.yml"
fi

# Check DEPLOYMENT_TYPE is set in kubernetes configmap
if grep -q 'DEPLOYMENT_TYPE.*kubernetes' "$PROJECT_ROOT/kubernetes/bookservice-configmap.yaml"; then
    pass "DEPLOYMENT_TYPE set in kubernetes configmap"
else
    fail "DEPLOYMENT_TYPE missing in kubernetes configmap"
fi

# Test 12: APP_VERSION Configuration
echo ""
echo "--- Test 12: APP_VERSION Configuration ---"

# Check APP_VERSION is set in all config files
if grep -q 'APP_VERSION.*1.0.0' "$PROJECT_ROOT/docker-compose/docker-compose.yml"; then
    pass "APP_VERSION set in docker-compose.yml"
else
    fail "APP_VERSION missing in docker-compose.yml"
fi

if grep -q 'APP_VERSION.*1.0.0' "$PROJECT_ROOT/docker-swarm/docker-stack.yml"; then
    pass "APP_VERSION set in docker-stack.yml"
else
    fail "APP_VERSION missing in docker-stack.yml"
fi

if grep -q 'APP_VERSION.*1.0.0' "$PROJECT_ROOT/kubernetes/bookservice-configmap.yaml"; then
    pass "APP_VERSION set in kubernetes configmap"
else
    fail "APP_VERSION missing in kubernetes configmap"
fi

# Check upgrade files exist
if [ -f "$PROJECT_ROOT/docker-swarm/docker-stack-v1.0.1.yml" ]; then
    pass "Swarm upgrade file (v1.0.1) exists"
else
    fail "Swarm upgrade file missing"
fi

if [ -f "$PROJECT_ROOT/kubernetes/bookservice-configmap-v1.0.1.yaml" ]; then
    pass "K8s upgrade configmap (v1.0.1) exists"
else
    fail "K8s upgrade configmap missing"
fi

# Test 13: Docker Images
echo ""
echo "--- Test 13: Docker Images ---"

# Check if bookservice images exist
if docker image inspect bookservice:1.0.0 &>/dev/null; then
    pass "bookservice:1.0.0 image exists"
else
    warn "bookservice:1.0.0 image not found (build with: cd bookservice && docker build -t bookservice:1.0.0 .)"
fi

if docker image inspect bookservice:1.0.1 &>/dev/null; then
    pass "bookservice:1.0.1 image exists"
else
    warn "bookservice:1.0.1 image not found (create with: docker tag bookservice:1.0.0 bookservice:1.0.1)"
fi

# Test 14: ELK Stack Files
echo ""
echo "--- Test 14: ELK Stack Files ---"

if [ -f "$PROJECT_ROOT/elk/logstash/logstash.conf" ]; then
    pass "Logstash config exists"
else
    fail "Logstash config missing"
fi

if [ -d "$PROJECT_ROOT/elk/logstash" ]; then
    pass "ELK logstash directory exists"
else
    fail "ELK logstash directory missing"
fi

# Validate ELK compose file
if python3 -c "import yaml; yaml.safe_load(open('$PROJECT_ROOT/docker-compose/docker-compose-elk.yml'))" 2>/dev/null; then
    pass "docker-compose-elk.yml is valid YAML"
else
    fail "docker-compose-elk.yml has invalid YAML syntax"
fi

# Test 14b: Port Security Check
echo ""
echo "--- Test 14b: Port Security Check ---"

PUBLIC_IP="128.140.102.126"

# Check Elasticsearch port 9200 is NOT publicly accessible
if curl -s --connect-timeout 2 "http://${PUBLIC_IP}:9200" &>/dev/null; then
    fail "SECURITY RISK: Elasticsearch port 9200 is publicly accessible!"
else
    pass "Elasticsearch port 9200 is not publicly accessible"
fi

# Check Elasticsearch port 9300 is NOT publicly accessible
if curl -s --connect-timeout 2 "http://${PUBLIC_IP}:9300" &>/dev/null; then
    fail "SECURITY RISK: Elasticsearch port 9300 is publicly accessible!"
else
    pass "Elasticsearch port 9300 is not publicly accessible"
fi

# Check Logstash port 5044 is NOT publicly accessible
if curl -s --connect-timeout 2 "http://${PUBLIC_IP}:5044" &>/dev/null; then
    fail "SECURITY RISK: Logstash port 5044 is publicly accessible!"
else
    pass "Logstash port 5044 is not publicly accessible"
fi

# Check Kibana is localhost-only (should fail from public IP)
if curl -s --connect-timeout 2 "http://${PUBLIC_IP}:5601" &>/dev/null; then
    warn "Kibana port 5601 is publicly accessible (consider SSH tunnel access only)"
else
    pass "Kibana port 5601 is not publicly accessible (localhost only)"
fi

# Test 15: Live Deployment Type Verification (if services are running)
echo ""
echo "--- Test 15: Live Deployment Type Verification ---"

PUBLIC_IP="128.140.102.126"

# Test Docker Compose (port 8080)
COMPOSE_RESPONSE=$(curl -s "http://${PUBLIC_IP}:8080/api/books" 2>/dev/null || echo "")
if [[ "$COMPOSE_RESPONSE" == *'"deployment":"docker-compose"'* ]]; then
    pass "Docker Compose returns deployment: docker-compose"
    # Check version
    if [[ "$COMPOSE_RESPONSE" == *'"version":"1.0.'* ]]; then
        VERSION=$(echo "$COMPOSE_RESPONSE" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        pass "Docker Compose returns version: $VERSION"
    else
        warn "Docker Compose version field not found"
    fi
elif [[ "$COMPOSE_RESPONSE" == *'"deployment"'* ]]; then
    DEPLOY_TYPE=$(echo "$COMPOSE_RESPONSE" | grep -o '"deployment":"[^"]*"' | cut -d'"' -f4)
    fail "Docker Compose returns wrong deployment type: $DEPLOY_TYPE (expected: docker-compose)"
elif [ -z "$COMPOSE_RESPONSE" ]; then
    warn "Docker Compose not running on port 8080 (skipped)"
else
    warn "Could not parse Docker Compose response"
fi

# Test Docker Swarm (port 8081)
SWARM_RESPONSE=$(curl -s "http://${PUBLIC_IP}:8081/api/books" 2>/dev/null || echo "")
if [[ "$SWARM_RESPONSE" == *'"deployment":"docker-swarm"'* ]]; then
    pass "Docker Swarm returns deployment: docker-swarm"
    # Check version
    if [[ "$SWARM_RESPONSE" == *'"version":"1.0.'* ]]; then
        VERSION=$(echo "$SWARM_RESPONSE" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        pass "Docker Swarm returns version: $VERSION"
    else
        warn "Docker Swarm version field not found"
    fi
elif [[ "$SWARM_RESPONSE" == *'"deployment"'* ]]; then
    DEPLOY_TYPE=$(echo "$SWARM_RESPONSE" | grep -o '"deployment":"[^"]*"' | cut -d'"' -f4)
    fail "Docker Swarm returns wrong deployment type: $DEPLOY_TYPE (expected: docker-swarm)"
elif [ -z "$SWARM_RESPONSE" ]; then
    warn "Docker Swarm not running on port 8081 (skipped)"
else
    warn "Could not parse Docker Swarm response"
fi

# Test Kubernetes (port 30080)
K8S_RESPONSE=$(curl -s "http://${PUBLIC_IP}:30080/api/books" 2>/dev/null || echo "")
if [[ "$K8S_RESPONSE" == *'"deployment":"kubernetes"'* ]]; then
    pass "Kubernetes returns deployment: kubernetes"
    # Check version
    if [[ "$K8S_RESPONSE" == *'"version":"1.0.'* ]]; then
        VERSION=$(echo "$K8S_RESPONSE" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        pass "Kubernetes returns version: $VERSION"
    else
        warn "Kubernetes version field not found"
    fi
elif [[ "$K8S_RESPONSE" == *'"deployment"'* ]]; then
    DEPLOY_TYPE=$(echo "$K8S_RESPONSE" | grep -o '"deployment":"[^"]*"' | cut -d'"' -f4)
    fail "Kubernetes returns wrong deployment type: $DEPLOY_TYPE (expected: kubernetes)"
elif [ -z "$K8S_RESPONSE" ]; then
    warn "Kubernetes not running on port 30080 (skipped)"
else
    warn "Could not parse Kubernetes response"
fi

# Summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC} $TESTS_PASSED"
echo -e "${RED}Failed:${NC} $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! Ready for deployment testing.${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please fix before submission.${NC}"
    exit 1
fi
