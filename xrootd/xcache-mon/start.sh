source ../../environment

HOST=`hostname -s`
FILE=config/$HOST/etc/t2_maitenance.conf
if [ ! -f "$FILE" ]; then
   echo "========================================================="
   echo " CONFIGURATION FAILURE!!!"
   echo "========================================================="
   echo "Prepare monitoring configuration file:"
   echo "1. cp config/default/etc/t2_maitenance.conf $FILE"
   echo "2. edit $FILE and update IPs and or other parameters as needed"
   echo "========================================================="
   exit 1
fi

docker-compose up --detach
