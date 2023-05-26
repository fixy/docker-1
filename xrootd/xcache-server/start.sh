source ../../environment

if [[ "$HOSTNAME" =~ ^xrd-nvme- ]]; then
  python3 nodeScan.py --memory-percent=35
else
  python3 nodeScan.py
fi

docker-compose up --detach xcache-server
