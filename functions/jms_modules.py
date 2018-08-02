import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_jms_modules():
    """
        Function takes the name of the FileStores through the method cmo.getFileStores
        :return: A list of FileStores
    """
    try:
        jms_modules = cmo.getJMSSystemResources()
        jm_array = []
        for jms_module in jms_modules:
           jm = str(jms_module)
           jm = jm.split("=")
           jm = jm[1].split(",")
           jm_array.append(jm[0])
        return jm_array
    except raiseWLSTException:
        raise


def get_params(jms_module_hash):
    """
        Function lookup the key values from certain dictionary
            :param jms_module_hash: Receives a dictionary that contains the name of
             the modules of jms
            :return: Return a dictionary with lookup key[jms_module] and values
    """
    for jms_module in jms_module_hash:
        for key in jms_module_hash[jms_module]:
            if key in ['target', 'targettype']:
                jms_module_hash[jms_module][key] = str(get(jms_module_hash[jms_module][key])).split(" ")
            else:
                jms_module_hash[jms_module][key] = get(jms_module_hash[jms_module][key])
    return jms_module_hash

def get_clusters():
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        cd('/JMSSystemResources')
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

# Main

username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Connection string
connect(username, password, 't3://' + hostname + ':7001')

# Fuction for get array of jms_modules
jms_modules = get_jms_modules()

# String to dictionary conversion
parameters = convert_dict(contents)

clusters = get_clusters()

jms_modules_hash = {}
# Interactive array and replace variables with contains '{sever} and {jms_module}'
# to another receive parameter
for jms_module in jms_modules:
    jms_modules_hash[jms_module] = {}
    for cluster in clusters:
        for parameter in parameters:
            jms_modules_hash[jms_module][parameter] = parameters[parameter].replace('{jms_module}', jms_module)
            jms_modules_hash[jms_module][parameter] = jms_modules_hash[jms_module][parameter].replace('{ClusterName}', cluster)

# Relevant output
print get_params(jms_modules_hash)

