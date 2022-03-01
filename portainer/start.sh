# Need to check that volume is present
#docker volume create portainer_data
docker run -d --net=host --name portainer     --restart=always     -v /var/run/docker.sock:/var/run/docker.sock     -v portainer_data:/data     cr.portainer.io/portainer/portainer-ce:2.11.1
