#!/usr/bin/env python3
# build_config.py
# Reads accounts.txt and injects all users into xray config.json

import json

ACCOUNTS_FILE = "/etc/xray/accounts.txt"
CONFIG_FILE   = "/etc/xray/config.json"

# Read usernames from accounts.txt
users = []
with open(ACCOUNTS_FILE) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            users.append(line)

print(f"[*] Found {len(users)} account(s): {users}")

# Load base config
with open(CONFIG_FILE) as f:
    cfg = json.load(f)

# Build client lists
vless_clients  = [{"id": u, "level": 0, "email": u} for u in users]
vmess_clients  = [{"id": u, "alterId": 0, "email": u} for u in users]
trojan_clients = [{"password": u, "email": u} for u in users]

# Inject into inbounds
for inb in cfg.get("inbounds", []):
    proto = inb.get("protocol")
    if proto == "vless":
        inb["settings"]["clients"] = vless_clients
        print(f"[✓] Injected {len(vless_clients)} VLESS user(s)")
    elif proto == "vmess":
        inb["settings"]["clients"] = vmess_clients
        print(f"[✓] Injected {len(vmess_clients)} VMess user(s)")
    elif proto == "trojan":
        inb["settings"]["clients"] = trojan_clients
        print(f"[✓] Injected {len(trojan_clients)} Trojan user(s)")

# Save updated config
with open(CONFIG_FILE, "w") as f:
    json.dump(cfg, f, indent=2)

print("[✓] Config built successfully!")
print("")
print("=== ACCOUNTS READY ===")
for u in users:
    print(f"  Username/UUID: {u}")
print("======================")
