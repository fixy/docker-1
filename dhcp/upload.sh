source ../environment
docker login $SWARM
dockerimageid=`docker images | grep dhcp-sdn | grep latest | awk '{print $3}'`
docker tag $dockerimageid $SWARM/dhcp-sdn:latest
docker push $SWARM/dhcp-sdn
