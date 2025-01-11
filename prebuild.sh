#!/bin/bash
set -e

# Update and install system dependencies without sudo
apt-get update
apt-get install -y \
    libgstreamer-gl1.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libavif15 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt --no-cache-dir

# Install Playwright
python -m pip install playwright
playwright install-deps
playwright install