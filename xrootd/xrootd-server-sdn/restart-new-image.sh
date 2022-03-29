source ../../environment
for id in `docker ps -a | grep $SWARM/xrootd-stageout-server | awk '{print $1}'`;
do
  docker stop $id;
  docker rm $id;
done

docker image rm $SWARM/xrootd-stageout-server --force
./start.sh
