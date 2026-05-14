#!/bin/bash

# =================================================================
# Samsung Strategic Analysis: Unified Execution Script
# =================================================================

# Color codes for cleaner terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Samsung Strategic Market & Lifecycle Analysis Pipeline...${NC}"

# 1. Environment Setup
echo -e "${BLUE}[1/2] Installing dependencies...${NC}"
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Dependency installation failed.${NC}"
    exit 1
fi

# 2. Launch Dashboard
echo -e "${BLUE}[2/2] Launching Streamlit Dashboard...${NC}"
echo -e "${GREEN}Pipeline complete. Your browser will open shortly.${NC}"
python3 -m streamlit run app.py