#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if it's not already installed
if ! command -v nginx &>/dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file for testing Nginx configuration
echo "<html><head></head><body>Test Page</body></html>" > /data/web_static/releases/test/index.html

# Create symbolic link /data/web_static/current
if [[ -L /data/web_static/current ]]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sed -i '/^server {/a \
    location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }\
' "$config_file"

# Restart Nginx
service nginx restart
