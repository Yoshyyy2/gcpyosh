#!/bin/bash

# Inject UUID into xray config
sed -i "s|PLACEHOLDER_UUID|${UUID}|g" /etc/xray/config.json

# Start Xray in background
/usr/local/bin/xray run -c /etc/xray/config.json &

# Small delay so xray is up before nginx starts routing to it
sleep 1

# Start Nginx in foreground (keeps container alive)
nginx -g "daemon off;"
