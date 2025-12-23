#!/bin/bash

# ============================================
# Kubernetes Commands Reference (k3s)
# Book Service Deployment
# ============================================
#
# NOTE: This project uses k3s instead of minikube.
# k3s is a lightweight, production-ready Kubernetes distribution.
#
# Install k3s: curl -sfL https://get.k3s.io | sh -
# Configure kubectl:
#   mkdir -p ~/.kube
#   sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
#   sudo chown $(id -u):$(id -g) ~/.kube/config
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Kubernetes Commands for Book Service${NC}"
echo "========================================"

# -------------------------------------------
# 1. APPLY ALL MANIFESTS
# -------------------------------------------
echo -e "\n${YELLOW}1. Deploy all resources:${NC}"
echo "kubectl apply -k ."
echo "# Or apply individual files:"
echo "kubectl apply -f namespace.yaml"
echo "kubectl apply -f mysql-secret.yaml"
echo "kubectl apply -f mysql-configmap.yaml"
echo "kubectl apply -f mysql-pvc.yaml"
echo "kubectl apply -f mysql-deployment.yaml"
echo "kubectl apply -f mysql-service.yaml"
echo "kubectl apply -f bookservice-configmap.yaml"
echo "kubectl apply -f bookservice-deployment.yaml"
echo "kubectl apply -f bookservice-service.yaml"

# -------------------------------------------
# 2. CHECK STATUS
# -------------------------------------------
echo -e "\n${YELLOW}2. Check deployment status:${NC}"
echo "kubectl get all -n bookservice"
echo "kubectl get pods -n bookservice -w  # Watch pods"
echo "kubectl get deployments -n bookservice"
echo "kubectl get services -n bookservice"

# -------------------------------------------
# 3. SCALING
# -------------------------------------------
echo -e "\n${YELLOW}3. Scale deployment:${NC}"
echo "# Scale to 5 replicas"
echo "kubectl scale deployment bookservice -n bookservice --replicas=5"
echo ""
echo "# Scale down to 2 replicas"
echo "kubectl scale deployment bookservice -n bookservice --replicas=2"

# -------------------------------------------
# 4. ROLLING UPDATE
# -------------------------------------------
echo -e "\n${YELLOW}4. Perform rolling update:${NC}"
echo "# Update config (triggers rolling restart)"
echo "kubectl apply -f bookservice-configmap-v1.0.1.yaml"
echo ""
echo "# Or update image directly"
echo "kubectl set image deployment/bookservice bookservice=wahba87/bookservice:1.0.0 -n bookservice"
echo ""
echo "# Check rollout status"
echo "kubectl rollout status deployment/bookservice -n bookservice"

# -------------------------------------------
# 5. ROLLBACK
# -------------------------------------------
echo -e "\n${YELLOW}5. Rollback deployment:${NC}"
echo "# View rollout history"
echo "kubectl rollout history deployment/bookservice -n bookservice"
echo ""
echo "# Rollback to previous version"
echo "kubectl rollout undo deployment/bookservice -n bookservice"
echo ""
echo "# Rollback to specific revision"
echo "kubectl rollout undo deployment/bookservice -n bookservice --to-revision=1"

# -------------------------------------------
# 6. VIEW LOGS
# -------------------------------------------
echo -e "\n${YELLOW}6. View logs:${NC}"
echo "kubectl logs -l app=bookservice -n bookservice"
echo "kubectl logs -l app=bookservice -n bookservice -f  # Follow logs"
echo "kubectl logs <pod-name> -n bookservice"

# -------------------------------------------
# 7. EXEC INTO POD
# -------------------------------------------
echo -e "\n${YELLOW}7. Execute commands in pod:${NC}"
echo "kubectl exec -it <pod-name> -n bookservice -- /bin/sh"

# -------------------------------------------
# 8. DESCRIBE RESOURCES
# -------------------------------------------
echo -e "\n${YELLOW}8. Describe resources:${NC}"
echo "kubectl describe deployment bookservice -n bookservice"
echo "kubectl describe pod <pod-name> -n bookservice"
echo "kubectl describe service bookservice -n bookservice"

# -------------------------------------------
# 9. PORT FORWARD
# -------------------------------------------
echo -e "\n${YELLOW}9. Port forwarding:${NC}"
echo "kubectl port-forward service/bookservice 8080:8080 -n bookservice"

# -------------------------------------------
# 10. DELETE RESOURCES
# -------------------------------------------
echo -e "\n${YELLOW}10. Delete resources:${NC}"
echo "kubectl delete -k ."
echo "# Or delete namespace (removes everything)"
echo "kubectl delete namespace bookservice"

# -------------------------------------------
# 11. CONFIGMAP AND SECRET MANAGEMENT
# -------------------------------------------
echo -e "\n${YELLOW}11. ConfigMap and Secret management:${NC}"
echo "kubectl get configmaps -n bookservice"
echo "kubectl get secrets -n bookservice"
echo "kubectl describe configmap bookservice-config -n bookservice"

echo -e "\n${GREEN}========================================${NC}"
