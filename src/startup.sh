!/bin/bash

# convert Markdown to HTML (used to be done only at startup, now done at build time as well)
python -c 'import src.server;src.server.conv(src.server.mdfiles, verbose=True)'

# Start Gunicorn im Hintergrund
gunicorn -b 0.0.0.0:8000 src.server:app &

# Start Caddy (im Vordergrund)
caddy run --config src/Caddyfile --adapter caddyfile

