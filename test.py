import requests
import json
from topology import topology

controller = '192.168.31.128:8181'
url_topology = 'http://{}/restconf/operational/network-topology:network-topology/topology/example-linkstate-topology'.format(controller)
headers={'Authorization': 'admin:<admin>'}
r = requests.get(url_topology,auth = ('admin','admin'))
j = r.text
msg = json.loads(j)

topo = topology(msg)
d = topo.get_topology()
d_json = topo.topology_jscript

# link_list = topo.get_links()
# node_list = topo.get_nodes()
# topologyData = {}
# json_links_list = json.dumps(links_list, indent = 2)
# print(json_links_list)
f = open('data4.js', 'w+')
f.write(d_json)
