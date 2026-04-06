#!/bin/bash

echo "=============================="
echo "  GCPYosh - Starting up..."
echo "=============================="

# Build xray config from accounts.txt
python3 /etc/xray/build_config.py

# Start Xray in background
/usr/local/bin/xray run -c /etc/xray/config.json &

# Wait for xray to be ready
sleep 1

# Start Nginx in foreground
echo "[✓] Starting Nginx on port 8080..."
nginx -g "daemon off;"
