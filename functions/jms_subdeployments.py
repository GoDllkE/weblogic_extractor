import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_jms_modules():
    """
        This function get jms_servers through cmo method.
        :return:        A list of jms_servers
    """
    try:
        cd('/JMSSystemResources/')
        jms_modules = str(cmo.getJMSSystemResources())
        if '=' in jms_modules:
            jms_modules = jms_modules.split("=", 1)[1]
            jms_modules = jms_modules.split(",", 1)[0]
            return jms_modules
        else:
            return None
    except raiseWLSTException:
        raise


def get_jms_subdeployments(jms_module_name):
    """
        This function get jms_servers through cmo method.
        :return:        A list of jms_servers
    """
    try:
        cd('/JMSSystemResources/' + jms_module_name + '/SubDeployments')
        jms_subdeployment_list =list(cmo.getSubDeployments())
        lista = []
        for subdeployment in jms_subdeployment_list:
            subdep = str(subdeployment)
            subdep = subdep.split("=")[2]
            subdep = subdep.split(",")[0]
            lista.append(subdep)
        return lista
    except raiseWLSTException:
        raise

def get_jms_targets(jms_module_name, jms_subdeployment):
    """
        This function get jms_servers through cmo method.
        :return:        A list of jms_servers
    """
    try:
        cd('/JMSSystemResources/' + jms_module_name  + '/SubDeployments/' + jms_subdeployment + '/Targets')
        jms_target_list = cmo.getTargets()
        lista = []
        for target in jms_target_list:
            tgt = str(target)
            tgt = tgt.split("=")
            tgt = tgt[1].split(",")
            tgt = str(tgt[0])
        return str(tgt)
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
            if key in ['target', 'targettype']:
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
jms_module = get_jms_modules()

#
if jms_module is None:
    print '{}'
    sys.exit(0)
else:
    jms_subdeployment_list = get_jms_subdeployments(jms_module)

# Create dict
dic = {}

for subdeployment in jms_subdeployment_list:
    # Create master key
    master_key = jms_module + ':' + subdeployment
    dic[master_key] = {}
    for key in data:
        # Get missing content
        jms_cluster_targets = get_jms_targets(jms_module, subdeployment)

        # Mount value based on the missing gotten information
        value = data[key].replace('{JmsModule}', str(jms_module))
        value = value.replace('{ClusterJmsSubdept}', subdeployment)
        value = value.replace('{JmsTargets}', jms_cluster_targets)

        # Save to dictionary
        dic[master_key][key] = value

# Do the magic
gathered_information = get_params(dic)

# Print dictionary
print gathered_information

