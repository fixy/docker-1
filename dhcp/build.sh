for did in `docker images | grep dhcp-sdn | awk '{print $3}' | uniq`;
do
  docker image rm $did --force;
done
docker build --no-cache -t dhcp-sdn .
