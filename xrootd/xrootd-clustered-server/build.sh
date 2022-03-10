for did in `docker images | grep xrootd-clustered-server | awk '{print $3}' | uniq`;
do
  docker image rm $did --force;
done
docker build --no-cache -t xrootd-clustered-server .
