#!/bin/bash

# Activate the virtual environment
source /home/ubuntu/betface_core/venv/bin/activate

# Run your make commands
cd /home/ubuntu/betface_core
make odds
make scrape