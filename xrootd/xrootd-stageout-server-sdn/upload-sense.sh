source ../../environment
docker login
dockerimageid=`docker images | grep xrootd-stageout-server-sdn | grep latest | awk '{print $3}'`
docker tag $dockerimageid sdnsense/xrootd-stageout-server-sdn:latest
docker push sdnsense/xrootd-stageout-server-sdn
