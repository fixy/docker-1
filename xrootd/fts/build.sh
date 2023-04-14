for did in `docker images | grep sense-fts3 | awk '{print $3}' | uniq`;
do
  docker image rm $did --force;
done
docker build --no-cache -t sense-fts3 .
