#!/bin/bash
set -e

# Upgrade pip
python -m pip install --upgrade pip

#!/bin/bash
# Update package lists
sudo apt-get update
pip install uvicorn

# Install missing Playwright dependencies
sudo apt-get install -y \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libavif15 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2

# Install Playwright browsers
playwright install


# Install dependencies
python -m pip install -r requirements.txt --no-cache-dir

# Install Playwright system dependencies and browsers
playwright install-deps
playwright install