#!/bin/bash
# Auto-generated installation script for Kali Linux

set -e

echo "========================================"
echo "Installing GitHub Tool on Kali Linux"
echo "========================================"

# Update system
echo "Updating system packages..."
sudo apt-get update

# Install system dependencies
echo 'Installing system dependencies...'
sudo apt-get install -y Install requests using pip: pip install requests Ensure that the user has ProxyChains installed by adding a check and prompt for installation: 'sudo apt-get install proxychains4'. Include in documentation that Git must be installed. Use 'apt-get install git' if not installed.

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
