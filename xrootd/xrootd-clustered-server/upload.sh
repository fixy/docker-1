source ../../environment
docker login $SWARM
dockerimageid=`docker images | grep xrootd-clustered-server | grep latest | awk '{print $3}'`
docker tag $dockerimageid $SWARM/xrootd-clustered-server:latest
docker push $SWARM/xrootd-clustered-server
