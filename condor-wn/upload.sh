source ../environment
docker login $SWARM
dockerimageid=`docker images | grep condor-wn | grep latest | awk '{print $3}'`
docker tag $dockerimageid $SWARM/condor-wn:latest
docker push $SWARM/condor-wn
