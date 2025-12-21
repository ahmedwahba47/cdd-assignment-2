#!/bin/bash

# ============================================
# Helm Commands Reference
# Book Service Deployment
# ============================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Helm Commands for Book Service${NC}"
echo "========================================"

# -------------------------------------------
# 1. INSTALL CHART
# -------------------------------------------
echo -e "\n${YELLOW}1. Install Helm chart:${NC}"
echo "helm install bookservice ./bookservice-chart -n bookservice --create-namespace"
echo ""
echo "# Install with custom values"
echo "helm install bookservice ./bookservice-chart -n bookservice --create-namespace -f custom-values.yaml"

# -------------------------------------------
# 2. LIST RELEASES
# -------------------------------------------
echo -e "\n${YELLOW}2. List Helm releases:${NC}"
echo "helm list -n bookservice"
echo "helm list -A  # All namespaces"

# -------------------------------------------
# 3. CHECK STATUS
# -------------------------------------------
echo -e "\n${YELLOW}3. Check release status:${NC}"
echo "helm status bookservice -n bookservice"

# -------------------------------------------
# 4. UPGRADE RELEASE
# -------------------------------------------
echo -e "\n${YELLOW}4. Upgrade release:${NC}"
echo "# Upgrade with new image tag"
echo "helm upgrade bookservice ./bookservice-chart -n bookservice --set image.tag=2.0.0"
echo ""
echo "# Upgrade with new replica count"
echo "helm upgrade bookservice ./bookservice-chart -n bookservice --set replicaCount=5"

# -------------------------------------------
# 5. ROLLBACK
# -------------------------------------------
echo -e "\n${YELLOW}5. Rollback to previous version:${NC}"
echo "# View history"
echo "helm history bookservice -n bookservice"
echo ""
echo "# Rollback to previous revision"
echo "helm rollback bookservice -n bookservice"
echo ""
echo "# Rollback to specific revision"
echo "helm rollback bookservice 1 -n bookservice"

# -------------------------------------------
# 6. TEMPLATE (DRY RUN)
# -------------------------------------------
echo -e "\n${YELLOW}6. Template (preview manifests):${NC}"
echo "helm template bookservice ./bookservice-chart -n bookservice"
echo ""
echo "# Debug with dry run"
echo "helm install bookservice ./bookservice-chart -n bookservice --dry-run --debug"

# -------------------------------------------
# 7. GET VALUES
# -------------------------------------------
echo -e "\n${YELLOW}7. Get release values:${NC}"
echo "helm get values bookservice -n bookservice"
echo "helm get values bookservice -n bookservice -a  # All values"

# -------------------------------------------
# 8. UNINSTALL
# -------------------------------------------
echo -e "\n${YELLOW}8. Uninstall release:${NC}"
echo "helm uninstall bookservice -n bookservice"

# -------------------------------------------
# 9. ADD BITNAMI REPO (for MySQL dependency)
# -------------------------------------------
echo -e "\n${YELLOW}9. Add Bitnami repo:${NC}"
echo "helm repo add bitnami https://charts.bitnami.com/bitnami"
echo "helm repo update"

# -------------------------------------------
# 10. BUILD DEPENDENCIES
# -------------------------------------------
echo -e "\n${YELLOW}10. Build chart dependencies:${NC}"
echo "helm dependency build ./bookservice-chart"
echo "helm dependency update ./bookservice-chart"

echo -e "\n${GREEN}========================================${NC}"
