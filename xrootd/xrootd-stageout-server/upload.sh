source ../../environment
docker login --username $USERNAME
dockerimageid=`docker images | grep xrootd-stageout-server | grep latest | awk '{print $3}'`
docker tag $dockerimageid $USERNAME/xrootd-stageout-server:latest
docker push $USERNAME/xrootd-stageout-server
