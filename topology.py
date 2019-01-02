import re
import json

class topology():
    def __init__(self, msg):
        self.msg = msg
        self.link_list = msg['topology'][0]['link']
        self.node_list = msg['topology'][0]['node']
        self.id_dict = {}
    def get_links(self):
        links_list = []
        repeat_dict = {}
        if len(self.id_dict) == 0:
            return 'Es necesario ejecutar primero get_nodes()'
        n = 1
        for i in self.link_list:
            links_dict = {}
            link_id = i['link-id']
            source_node_id = re.findall('local-router=([0-9].+)\&remote-as',link_id)
            target_node_id = re.findall('remote-router=([0-9].+)\&ipv4-iface',link_id)
            source_ip = re.findall('ipv4-iface=(.+)\&ipv4-neigh',link_id)
            destination_ip = re.findall('ipv4-neigh=(.+)',link_id)

            if source_ip and destination_ip:
                tup1 = (source_ip[0], destination_ip[0])
                tup2 = (destination_ip[0], source_ip[0])
                if (tup1 and tup2) not in repeat_dict:
                    repeat_dict[tup1] = n
                    repeat_dict[tup2] = n
                else:
                    repeat_dict[tup1] += 1
                    repeat_dict[tup2] += 1

            else:
                print('Hay un problema para agregar source ip y destination ip en el link {}'.format(link_id))
                continue


            if (repeat_dict[tup1] or repeat_dict[tup2]) > 1:
                continue

            if source_node_id and target_node_id:
                links_dict['source'] = self.id_dict[source_node_id[0]]
                links_dict['target'] = self.id_dict[target_node_id[0]]
            else:
                print('Hay un problema para agregar source y target en el link {}'.format(link_id))
                continue

            links_dict['source_ip'] = source_ip[0]
            links_dict['destination_ip'] = destination_ip[0]
            links_list.append(links_dict)
        print(repeat_dict)
        return links_list

    def get_nodes(self):
        node_list = []
        id_count = 0
        for i in self.node_list:
            node_dict = {}
            temp = i['node-id']
            node_id = re.findall('router=(.+)',temp)
            try:
                router_id= i['l3-unicast-igp-topology:igp-node-attributes']['router-id'][0]
            except:
                print('no existe router_id para {}'.format(temp))
                router_id = ''
            if node_id:
                node_dict['id'] = id_count
                self.id_dict[node_id[0]] = id_count
                id_count += 1
            else:
                print('no existe node_id para {}'.format(temp))
                node_dict['id'] = ''
            node_dict['name'] = router_id
            node_dict['x'] = 100
            node_dict['y'] = 100
            node_list.append(node_dict)
        return node_list

    def get_topology(self):
        topologyData = {}
        node_list = self.get_nodes()
        link_list = self.get_links()
        json_node_list = json.dumps(node_list, indent = 1)
        json_link_list = json.dumps(link_list, indent = 1)

        topologyData['nodes'] = node_list
        topologyData['links'] = link_list
        self.topology_jscript = '''var topologyData = {{
    nodes: {nodes},
    links: {links}
    }};'''.format(nodes = json_node_list, links = json_link_list)
        return topologyData
