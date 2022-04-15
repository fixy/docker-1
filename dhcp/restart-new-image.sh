source ../environment
for id in `docker ps -a | grep $SWARM/dhcp-sdn | awk '{print $1}'`;
do
  docker stop $id;
  docker rm $id;
done

docker image rm $SWARM/dhcp-sdn --force
./start.sh
