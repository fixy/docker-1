for did in `docker images | grep xrootd-stageout-server-sdn | awk '{print $3}' | uniq`;
do
  docker image rm $did --force;
done
docker build --no-cache -t xrootd-stageout-server-sdn .
