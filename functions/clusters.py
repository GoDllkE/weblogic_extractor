import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_clusters():
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        clusters = cmo.getClusters()
        lista = []
        for cluster in clusters:
           a = str(cluster)
           a = a.split("=")
           a = a[1].split(",")
           lista.append(a[0])
        return lista
    except raiseWLSTException:
        raise

def get_clusters_servers(data, cluster):
    try:
        cd(data[cluster]['servers'])
        servers = cmo.getServers()
        lista = []
        for server in servers:
            srv = str(server)
            srv = srv.split("=")
            srv = srv[1].split(",")
            lista.append(srv[0])
        return lista
    except raiseWLSTException:
        raise

def get_params(dicionario):
    """
        This function lookup the key values from certain dictionary
        :return: return a dictionary with lookup key[clusters] amd values
    """
    for cluster in dicionario:
        for key in dicionario[cluster]:
            if key == 'servers':
                dicionario[cluster][key] = get_clusters_servers(dicionario, cluster)
            else:
                var = dicionario[cluster][key]
                dicionario[cluster][key] = get(var)
    return dicionario


# Main
# Load credentials
username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Connect to a existing weblogic
connect(username, password, 't3://' + hostname + ':7001')

# Convert contents into dictionary
data = convert_dict(contents)

# Lookup for base cluster keys and save into a list
cluster_list = get_clusters()

# Interactive array and replace variables with contains '{clusterName}' to another receive parameter
dicionario = {}
for cluster in cluster_list:
    dicionario[cluster] = {}
    for key in data:
        dicionario[cluster][key] = data[key].replace('{ClusterName}', cluster)
    continue

#
print get_params(dicionario)

