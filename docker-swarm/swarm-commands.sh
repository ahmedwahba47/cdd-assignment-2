#!/bin/bash

# ============================================
# Docker Swarm Commands Reference
# Book Service Deployment
# ============================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Docker Swarm Commands for Book Service${NC}"
echo "========================================"

# -------------------------------------------
# 1. INITIALIZE SWARM
# -------------------------------------------
echo -e "\n${YELLOW}1. Initialize Docker Swarm:${NC}"
echo "docker swarm init"
echo "# For multi-node: docker swarm init --advertise-addr <MANAGER-IP>"

# -------------------------------------------
# 2. DEPLOY STACK
# -------------------------------------------
echo -e "\n${YELLOW}2. Deploy the stack:${NC}"
echo "docker stack deploy -c docker-stack.yml bookservice-stack"

# -------------------------------------------
# 3. LIST SERVICES
# -------------------------------------------
echo -e "\n${YELLOW}3. List services:${NC}"
echo "docker stack services bookservice-stack"
echo "docker service ls"

# -------------------------------------------
# 4. SCALING
# -------------------------------------------
echo -e "\n${YELLOW}4. Scale services:${NC}"
echo "# Scale to 5 replicas"
echo "docker service scale bookservice-stack_bookservice=5"
echo ""
echo "# Scale down to 2 replicas"
echo "docker service scale bookservice-stack_bookservice=2"

# -------------------------------------------
# 5. UPDATE SERVICE (Rolling Update)
# -------------------------------------------
echo -e "\n${YELLOW}5. Update service (Rolling Update):${NC}"
echo "# Update to new image version"
echo "docker service update --image yourusername/bookservice:2.0.0 bookservice-stack_bookservice"
echo ""
echo "# Update with environment variable"
echo "docker service update --env-add NEW_VAR=value bookservice-stack_bookservice"

# -------------------------------------------
# 6. ROLLBACK
# -------------------------------------------
echo -e "\n${YELLOW}6. Rollback to previous version:${NC}"
echo "docker service rollback bookservice-stack_bookservice"

# -------------------------------------------
# 7. VIEW LOGS
# -------------------------------------------
echo -e "\n${YELLOW}7. View service logs:${NC}"
echo "docker service logs bookservice-stack_bookservice"
echo "docker service logs -f bookservice-stack_bookservice  # Follow logs"

# -------------------------------------------
# 8. INSPECT SERVICE
# -------------------------------------------
echo -e "\n${YELLOW}8. Inspect service details:${NC}"
echo "docker service inspect bookservice-stack_bookservice"
echo "docker service ps bookservice-stack_bookservice  # Show tasks"

# -------------------------------------------
# 9. REMOVE STACK
# -------------------------------------------
echo -e "\n${YELLOW}9. Remove stack:${NC}"
echo "docker stack rm bookservice-stack"

# -------------------------------------------
# 10. LEAVE SWARM
# -------------------------------------------
echo -e "\n${YELLOW}10. Leave Swarm:${NC}"
echo "docker swarm leave --force"

# -------------------------------------------
# 11. NODE MANAGEMENT
# -------------------------------------------
echo -e "\n${YELLOW}11. Node management:${NC}"
echo "docker node ls                    # List nodes"
echo "docker node inspect <node-id>     # Inspect node"
echo "docker node update --availability drain <node-id>  # Drain node"

echo -e "\n${GREEN}========================================${NC}"
