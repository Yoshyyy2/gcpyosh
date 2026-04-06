#!/usr/bin/env python3
import json, uuid

ACCOUNTS_FILE = "/etc/xray/accounts.txt"
CONFIG_FILE   = "/etc/xray/config.json"

def name_to_uuid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

users = []
with open(ACCOUNTS_FILE) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            users.append(line)

print(f"[*] Found {len(users)} account(s)")

with open(CONFIG_FILE) as f:
    cfg = json.load(f)

vless_clients  = [{"id": name_to_uuid(u), "level": 0, "email": u} for u in users]
vmess_clients  = [{"id": name_to_uuid(u), "alterId": 0, "email": u} for u in users]
trojan_clients = [{"password": u, "email": u} for u in users]

for inb in cfg.get("inbounds", []):
    proto = inb.get("protocol")
    if proto == "vless":
        inb["settings"]["clients"] = vless_clients
    elif proto == "vmess":
        inb["settings"]["clients"] = vmess_clients
    elif proto == "trojan":
        inb["settings"]["clients"] = trojan_clients

with open(CONFIG_FILE, "w") as f:
    json.dump(cfg, f, indent=2)

print("[✓] Config built!")
for u in users:
    print(f"  {u} → {name_to_uuid(u)}")
