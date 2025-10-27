!/bin/bash
# Start Gunicorn im Hintergrund
gunicorn -b 0.0.0.0:8000 src.server:app &

# Start Caddy (im Vordergrund)
caddy run --config src/Caddyfile --adapter caddyfile

