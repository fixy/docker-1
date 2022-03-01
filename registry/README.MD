docker volume create registry


htpasswd -B auth/registry.password <USERNAME>

cp /etc/letsencrypt/live/swarm-01.ultralight.org/fullchain.pem certs/fullchain.pem
cp /etc/letsencrypt/live/swarm-01.ultralight.org/privkey.pem certs/privkey.pem

