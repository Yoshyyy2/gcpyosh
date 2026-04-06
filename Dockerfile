FROM alpine:latest

# ══════════════════════════════════════════════
# CHANGE THIS UUID before building!
# ══════════════════════════════════════════════
ENV UUID=chad \
    PORT=8080

RUN apk add --no-cache curl unzip bash nginx && \
    curl -L -o /tmp/xray.zip \
      "https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip" && \
    unzip /tmp/xray.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip && \
    mkdir -p /etc/xray /run/nginx

COPY config.json /etc/xray/config.json
COPY nginx.conf /etc/nginx/http.d/default.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
