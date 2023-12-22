source ../../environment
docker login -u $USERNAME
dockerimageid=`docker images | grep xcache-server | grep latest | awk '{print $3}'`
docker tag $dockerimageid $USERNAME/xcache-server:latest
docker push $USERNAME/xcache-server
