import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_jms_servers():
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        cd('/JMSServers')
        servers = cmo.getJMSServers()
        lista = []
        for server in servers:
            srv = str(server)
            srv = srv.split("=")
            srv = srv[1].split(",")
            lista.append(srv[0])
        return lista
    except raiseWLSTException:
        raise

def get_jms_servers_targets(server):
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        cd('/JMSServers/' + server + '/Targets')
        target_list = cmo.getTargets()
        lista = []
        for target in target_list:
            tgt = str(target)
            tgt = tgt.split("=")
            tgt = tgt[1].split(",")
            lista.append(tgt[0])
        return lista
    except raiseWLSTException:
        raise

def get_jms_servers_persistentStore(server):
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        cd('/JMSServers/' + server + '/PersistentStore')
        persist_store = str(cmo.getPersistentStore())
        persist_store = persist_store.split("=")
        persist_store = persist_store[1].split(",")
        persist_store = persist_store[0]

        return persist_store
    except raiseWLSTException:
        raise

def convert_dict(lista):
    """
    Function to convert a List type into dictionary
        :param lista:       Receive a List type.
        :return:            Return a dictionary.
    """
    dic = {}
    lista = lista[0].split(",")
    for item in lista:
        dic[item.split(':',1)[0]] = item.split(':',1)[1]
    return dic


def get_params(dicionario):
    """
        This function lookup the key values from certain dictionary
            :return: A dictionary with lookup key[jms_server] amd values
    """
    for jms_server in dicionario:
        for key in dicionario[jms_server]:
            if key == 'target':
                dicionario[jms_server][key] = str(get(dicionario[jms_server][key])).split(" ")
            else:
                dicionario[jms_server][key] = get(dicionario[jms_server][key])
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

# Get keys and return a dictionary
jms_server_list = get_jms_servers()

dic = {}
for jms_server in  jms_server_list:
    # Create master key
    dic[jms_server] = {}
    for key in data:
        # Populate master key with received keys
        # Get missing information.
        server_jms_name = jms_server
        server_target = get_jms_servers_targets(jms_server)
        server_stores = get_jms_servers_persistentStore(jms_server)
        server_name = server_target[0]

        # Mount value based on retrieve missing information
        value = data[key].replace('{jms_server}', server_jms_name)
        value = value.replace('{server_target}', str(server_name))
        value = value.replace('{server_stores}', server_stores)
        value = value.replace('{ServerName}', server_name)

        # Save to dictionary
        dic[jms_server][key] = value

gathered_information = get_params(dic)

# Print dictionary
print gathered_information

