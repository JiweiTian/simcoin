import config
import bitcoindcmd
import tccmd


def run_node(node, cmd):
    return ('docker run'
            ' --cap-add=NET_ADMIN'  # for `tc`
            ' --detach=true'
            ' --net=isolated_network'
            ' --ip=' + str(node.ip) +
            ' --name=' + node.name +  # container name
            ' --hostname=' + node.name +
            ' --volume ' + config.host_dir(node) + ':' + bitcoindcmd.guest_dir +
            ' ' + config.node_image +  # image name # src: https://hub.docker.com/r/abrkn/bitcoind/
            ' bash -c "' + cmd + '" ')


def run_selfish_proxy(node, cmd):
        return (
                'docker run'
                ' --cap-add=NET_ADMIN'  # for `tc`
                ' --detach=true'
                ' --net=isolated_network'
                ' --ip=' + str(node.ip) +
                ' --name=' + node.name +
                ' --hostname=' + node.name +
                ' --rm'
                ' ' + config.selfish_node_image +
                ' bash -c "' + cmd + '"; ')


def exec_cmd(node, command):
        return ('docker exec '
                + node + ' '
                + command)


def create_network(ip_range):
        return ('docker network create'
                ' --subnet=' + ip_range +
                ' --driver bridge isolated_network')


def rm_network():
        return 'docker network rm isolated_network'


def fix_data_dirs_permissions():
        return ('docker run '
                ' --rm --volume ' + config.root_dir + ':/mnt' + ' ' + config.node_image + ' chmod a+rwx --recursive /mnt')


def rm_container(name):
        return 'docker rm --force ' + name
