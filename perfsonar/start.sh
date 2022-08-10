source ../environment
docker-compose up --detach

echo "Container started, waiting 10s before adding remote archive"
sleep 10
dockerid=`docker ps | grep 'perfsonar/testpoint:latest' | awk '{print $1}'`
docker exec -it $dockerid psconfig remote add --configure-archives http://monipe-central.rnp.br:8000/pub/config/autogole
