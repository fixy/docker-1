source ../../environment
for id in `docker ps -a | grep $USERNAME/xrootd-stageout-server-sdn | awk '{print $1}'`;
do
  docker stop $id;
  docker rm $id;
done

docker image rm $USERNAME/xrootd-stageout-server-sdn --force
./start.sh
