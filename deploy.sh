#!/bin/bash

# Pull the latest code changes from the repository
echo "Pulling latest changes from Git..."
git pull || { echo "Git pull failed. Exiting."; exit 1; }

# Reload systemd daemon first
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload || { echo "Failed to reload daemon. Exiting."; exit 1; }

# Restart the alumni-portal service
echo "Restarting the alumni-portal service..."
sudo systemctl restart alumni-portal || { echo "Failed to restart alumni-portal. Exiting."; exit 1; }

# Restart the Nginx service
echo "Restarting Nginx..."
sudo systemctl restart nginx || { echo "Failed to restart Nginx. Exiting."; exit 1; }

echo "All services restarted successfully!"
