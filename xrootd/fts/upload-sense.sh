source ../../environment
docker login
dockerimageid=`docker images | grep sense-fts3 | grep latest | awk '{print $3}'`
docker tag $dockerimageid sdnsense/sense-fts3:latest
docker push sdnsense/sense-fts3
