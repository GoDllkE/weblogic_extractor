import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_jms_cluster():
    """
        Must return a STR
    """
    try:
        cd('/JMSSystemResources')
        jms_cluster = cmo.getJMSSystemResources()
        lista = []
        for cluster in jms_cluster:
            clr = str(cluster)
            clr = clr.split("=")
            clr = clr[1].split(",")
            lista.append(clr[0])
        return lista
    except raiseWLSTException:
        raise


def get_jms_cluster_modules(cluster):
    """
        Must return a STR
    """
    try:
        cd('/JMSSystemResources/' + cluster + '/JMSResource')
        jms_module = str(cmo.getJMSResource())
        jms_module = jms_module.split("=", 1)[1]
        jms_module = jms_module.split(",", 1)[0]
        return jms_module
    except raiseWLSTException:
        raise

def get_jms_connectionFactories(cluster, modules):
    """
        Must return a LIST
    """
    try:
        cd('/JMSSystemResources/' + cluster + '/JMSResource/' + modules + '/ConnectionFactories')
        jms_cf = cmo.getConnectionFactories()
        lista = []
        for connfact in jms_cf:
            cf = str(connfact)
            cf = cf.split("=")
            cf = cf[1].split(",")
            lista.append(cf[0])
        return lista
    except raiseWLSTException:
        raise

def get_jms_cf_transactionParams(cluster, module, connectionFactory):
    """
        Must return a STR
    """
    try:
        cd('/JMSSystemResources/' + cluster + '/JMSResource/' + module + '/ConnectionFactories/' + connectionFactory + '/TransactionParams')
        jms_tp = str(cmo.getTransactionParams())
        jms_tp = jms_tp.split("=", 1)[1]
        jms_tp = jms_tp.split(",")[0]
        return jms_tp
    except raiseWLSTException:
        raise

def convert_dict(lista):
    """
    Function to convert a List type into dictionary
        :param lista:         Receive a List type.
        :return:                Return a dictionary.
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
            if key == 'jmsmodule':
                dicionario[jms_server][key] = dicionario[jms_server][key].split('/')[-1]
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

# Convert received content into a dic
data = convert_dict(contents)

# Get missing information
jms_cluster_list = get_jms_cluster()

# Prepare dic
dic = {}

# Loop into missin_data to fill dic
for jms_cluster in  jms_cluster_list:
    # Collect remaining keys
    jms_module = get_jms_cluster_modules(jms_cluster)

    # Collect remaining keys
    jms_cf = get_jms_connectionFactories(jms_cluster, jms_module)

    for confact in jms_cf:
        # Create master key
        master_key = jms_module + ':' + confact
        dic[master_key] = {}

        for key in data:
            # Get missing information
            jms_tf = get_jms_cf_transactionParams(jms_cluster, jms_module, confact)

            # Populate master key with received keys...
            value = data[key].replace('{ClusterJmsModule}', jms_module)
            value = value.replace('{ClusterJmsCf}', confact)
            value = value.replace('{ClusterJmsTp', jms_tf)

            # Save to dictionary
            dic[master_key][key] = value
            continue
        continue
    continue

# Do the magic
gathered_information = get_params(dic)

# Print dictionary
print gathered_information


