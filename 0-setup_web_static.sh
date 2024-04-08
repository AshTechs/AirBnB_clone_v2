#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if it's not already installed
if ! command -v nginx &>/dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file for testing Nginx configuration
echo "<html><head></head><body>Test Page</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create symbolic link /data/web_static/current
if [[ -L /data/web_static/current ]]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i '/^server {/a \    location /hbnb_static/ {\        alias /data/web_static/current/;\    }\ ' "$config_file"

# Restart Nginx
sudo service nginx restart
