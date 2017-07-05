import config

#
# for the 'tc' command 'iproute2' needs to be installed inside the container
# furthermore the container needs to be started with '--cap-add=NET_ADMIN'
#


def add(latency):
        return 'tc qdisc add dev eth0 root netem delay ' + str(latency) + 'ms'


def add_except_ip(latency, ip):
        return ['tc qdisc add dev eth0 root handle 1: prio',
                'tc filter add dev eth0 parent 1:0 protocol ip prio 1 u32 match ip dst ' + str(ip) + ' flowid 1:1',
                'tc filter add dev eth0 parent 1:0 protocol ip prio 1 u32 match ip dst ' + config.ip_range + ' flowid 1:2',
                'tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 0ms',
                'tc qdisc add dev eth0 parent 1:2 handle 20: netem delay ' + str(latency) + 'ms']
