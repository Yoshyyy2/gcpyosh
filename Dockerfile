FROM alpine:latest

ENV PORT=8080

RUN apk add --no-cache curl unzip bash nginx python3 && \
    curl -L -o /tmp/xray.zip \
      "https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip" && \
    unzip /tmp/xray.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip && \
    mkdir -p /etc/xray /run/nginx

# ══════════════════════════════════════════════
# accounts.txt — add your usernames here
# one username per line = one VPN account
# ══════════════════════════════════════════════
COPY accounts.txt /etc/xray/accounts.txt
COPY config.json /etc/xray/config.json
COPY nginx.conf /etc/nginx/http.d/default.conf
COPY build_config.py /etc/xray/build_config.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
