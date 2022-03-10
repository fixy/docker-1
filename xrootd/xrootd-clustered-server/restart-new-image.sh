source ../../environment
for id in `docker ps -a | grep $SWARM/xrootd-clustered-server | awk '{print $1}'`;
do
  docker stop $id;
  docker rm $id;
done

docker image rm $SWARM/xrootd-clustered-server --force
./start.sh
