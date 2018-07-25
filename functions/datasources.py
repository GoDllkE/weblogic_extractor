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
        cd('/JDBCSystemResources')
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

def get_jdbc_clusters():
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        cd('/JDBCSystemResources')
        clusters = cmo.getJDBCSystemResources()
        lista = []
        for cluster in clusters:
            a = str(cluster)
            a = a.split("=")
            a = a[1].split(",")
            lista.append(a[0])
        return lista
    except raiseWLSTException:
        raise

def get_datasources_targets(data, cluster):
    try:
        cd(data[cluster]['target'])
        servers = cmo.getTargets()
        lista = []
        for server in servers:
            srv = str(server).split("=")[1]
            srv = srv.split(",")[0]
            lista.append(srv)
        return lista
    except raiseWLSTException:
        raise

def get_jndinames(value):
    try:
        value = str(value)
        value = value.split(",", 1)[1]
        value = value.replace(")","")
        value = value.replace("[","")
        value = value.replace("]","")
        value = value.replace("'","")
        return str(value)
    except raiseWLSTException:
        raise

def get_params(dicionario):
    """
        This function lookup the key values from certain dictionary
        :return: return a dictionary with lookup key[clusters] amd values
    """
    for cluster in dicionario:
        for key in dicionario[cluster]:
            if key == 'target':
                dicionario[cluster][key] = get_datasources_targets(dicionario, cluster)
            elif key == 'jndinames':
                dicionario[cluster][key] = str(get_jndinames(get(dicionario[cluster][key]))).split()
            elif key in ['usexa', 'testconnectionsonreserve']:
                dicionario[cluster][key] = str(get(dicionario[cluster][key]))
            else:
                dicionario[cluster][key] = get(dicionario[cluster][key])
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
cluster_list = get_jdbc_clusters()

# Interactive array and replace variables with contains '{clusterName}' to another receive parameter
dicionario = {}
for jdbc_cluster in cluster_list:
    dicionario[jdbc_cluster] = {}
    for key in data:
        cluster_name = get_clusters()[0]
        dicionario[jdbc_cluster][key] = data[key].replace('{ClusterJDBC}', jdbc_cluster)
        dicionario[jdbc_cluster][key] = dicionario[jdbc_cluster][key].replace('{ClusterName}', str(cluster_name))
    continue

#
data = get_params(dicionario)

for key in data:
    data[key]['password'] = ""
    data[key]['ensure'] = "present"

print data

