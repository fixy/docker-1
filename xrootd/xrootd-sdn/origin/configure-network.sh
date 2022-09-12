
# Disable autoconf.
sysctl -w net.ipv6.conf.default.autoconf=0

export MAIN_INTF=enp49s0f0.43

export ID=0
export END=2
# echo /etc/iproute2/rt_tables new macvlan….
ip link del macvlan$ID
ip link add link macvlan$ID link $MAIN_INTF type macvlan mode bridge
ip link set macvlan$ID up
ip -6 addr add 2605:d9c0:2:fff$ID::$END/64 dev macvlan$ID
ip -6 r add 2605:d9c0:2:fff$ID::$END dev macvlan$ID table macvlan$ID
ip -6 route add default via 2605:d9c0:2:fff$ID::1 dev macvlan$ID table macvlan$ID
ip -6 rule add from 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
ip -6 rule add to 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
while true; do ping6 -c2 2605:d9c0:2:fff$ID::1 -I macvlan$ID > /dev/null && break; done

export ID=1
export END=2
# echo /etc/iproute2/rt_tables new macvlan….
ip link del macvlan$ID
ip link add link macvlan$ID link $MAIN_INTF type macvlan mode bridge
ip link set macvlan$ID up
ip -6 addr add 2605:d9c0:2:fff$ID::$END/64 dev macvlan$ID
ip -6 r add 2605:d9c0:2:fff$ID::$END dev macvlan$ID table macvlan$ID
ip -6 route add default via 2605:d9c0:2:fff$ID::1 dev macvlan$ID table macvlan$ID
ip -6 rule add from 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
ip -6 rule add to 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
while true; do ping6 -c2 2605:d9c0:2:fff$ID::1 -I macvlan$ID > /dev/null && break; done


export ID=2
export END=2
# echo /etc/iproute2/rt_tables new macvlan….
ip link del macvlan$ID
ip link add link macvlan$ID link $MAIN_INTF type macvlan mode bridge
ip link set macvlan$ID up
ip -6 addr add 2605:d9c0:2:fff$ID::$END/64 dev macvlan$ID
ip -6 r add 2605:d9c0:2:fff$ID::$END dev macvlan$ID table macvlan$ID
ip -6 route add default via 2605:d9c0:2:fff$ID::1 dev macvlan$ID table macvlan$ID
ip -6 rule add from 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
ip -6 rule add to 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
while true; do ping6 -c2 2605:d9c0:2:fff$ID::1 -I macvlan$ID > /dev/null && break; done


export ID=3
export END=2
# echo /etc/iproute2/rt_tables new macvlan….
ip link del macvlan$ID
ip link add link macvlan$ID link $MAIN_INTF type macvlan mode bridge
ip link set macvlan$ID up
ip -6 addr add 2605:d9c0:2:fff$ID::$END/64 dev macvlan$ID
ip -6 r add 2605:d9c0:2:fff$ID::$END dev macvlan$ID table macvlan$ID
ip -6 route add default via 2605:d9c0:2:fff$ID::1 dev macvlan$ID table macvlan$ID
ip -6 rule add from 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
ip -6 rule add to 2605:d9c0:2:fff$ID::$END/128 table macvlan$ID
while true; do ping6 -c2 2605:d9c0:2:fff$ID::1 -I macvlan$ID > /dev/null && break; done
