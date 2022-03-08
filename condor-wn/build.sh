for did in `docker images | grep condor-wn | awk '{print $3}' | uniq`;
do
  docker image rm $did --force;
done
docker build --no-cache -t condor-wn .
