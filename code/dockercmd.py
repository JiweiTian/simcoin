import plan
import bitcoindcmd


def run_bootstrap_node(node, cmd, latency):
    return ('docker run '
            ' --detach=true '
            ' --net=isolated_network '
            ' --ip=' + node.ip + ' '
            ' --name=' + node.name +   # container name
            ' ' + plan.node_image + ' '      # image name # src: https://hub.docker.com/r/abrkn/bitcoind/
            '   bash -c "' + slow_network(latency) + cmd + '" ')


def run_node(node, cmd, latency):
    return ('docker run '
            ' --cap-add=NET_ADMIN '  # for `tc`
            ' --detach=true '
            ' --net=isolated_network '
            ' --ip=' + str(node.ip) +
            ' --name=' + node.name + ' '   # container name
            ' --hostname=' + node.name + ' '
            ' --volume ' + plan.host_dir(node.name) + ':' + bitcoindcmd.guest_dir + ' '
            ' ' + plan.node_image + ' '      # image name # src: https://hub.docker.com/r/abrkn/bitcoind/
            ' bash -c "' + slow_network(latency) + cmd + '" ')


def run_selfish_node(node, cmd):
    public_ips = [str(ip) for ip in node.public_ips]
    args = ' {}'.format(node.args) if node.args else ''
    return (
            #
            # public node
            'docker run'
            ' --detach=true'
            ' --net=isolated_network'
            ' --ip=' + str(node.ip) +
            ' --name=' + node.name + '_proxy'
            ' --hostname=' + node.name + '_proxy'
            ' --rm'
            ' ' + plan.selfish_node_image +
            args +
            ' --ips-public ' + ' '.join(public_ips) + '; '
            #
            # private node
            'docker run'
            ' --detach=true'
            ' --net=isolated_network'
            ' --ip=' + str(node.private_ip) +
            ' --name=' + node.name +
            ' ' + plan.node_image +
            ' bash -c "' + cmd + '"')


def rm_node(node):
    return 'docker rm --force ' + node.name


def exec_bash(node, command):
        return ('docker exec '
                + node.name +
                ' /bin/sh -c "'
                + command + '"')


def create_network(ip_range):
        return ('docker network create'
                ' --subnet=' + ip_range +
                ' --driver bridge isolated_network')


def rm_network():
        return 'docker network rm isolated_network'


def fix_data_dirs_permissions():
        return ('docker run '
                ' --rm --volume ' + plan.root_dir + ':/mnt' + ' ' + plan.node_image + ' chmod a+rwx --recursive /mnt')


def slow_network(latency):
        # needed for this cmd: apt install iproute2 and --cap-add=NET_ADMIN
        return "tc qdisc replace dev eth0 root netem delay " + str(latency) + "ms; "
