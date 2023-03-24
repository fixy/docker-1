source ../../environment

HTTP_SECRET_FILE=/etc/xrootd/xrd_http_secret_key
if [ ! -f "$HTTP_SECRET_FILE" ]; then
    echo "$HTTP_SECRET_FILE does not exist."
    exit 1
fi
HTTP_SECRET=`cat $HTTP_SECRET_FILE`

sed -i "s/AAAASTART_REPLACE_ME_HTTP_KEYAAAA/$HTTP_SECRET/" docker-compose.yml

docker-compose up --detach
