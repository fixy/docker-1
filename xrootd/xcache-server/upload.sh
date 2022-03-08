source ../../environment
docker login $SWARM
dockerimageid=`docker images | grep xcache-server | grep latest | awk '{print $3}'`
docker tag $dockerimageid $SWARM/xcache-server:latest
docker push $SWARM/xcache-server
