import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_domainName():
    """
    Function for keys lookup.
        :param parameters:      Receive a Dictonary type.
        :return:                Return dictonary if real values
    """
    try:
        cd('/SelfTuning')
        domain_name = str(cmo.getSelfTuning())
        if '=' in domain_name:
            domain_name = domain_name.split("=", 1)[1]
            domain_name = domain_name.split(",", 1)[0]
            return domain_name
        else:
            return None
    except raiseWLSTException:
        raise

def get_clusters():
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        lista = []
        cd('/SelfTuning')
        clusters = cmo.getClusters()
        for cluster in clusters:
            a = str(cluster)
            a = a.split("=")
            a = a[1].split(",")
            lista.append(a[0])
        return lista
    except raiseWLSTException:
        raise


def get_workmanagerName(domain):
    try:
        cd('/SelfTuning/' + domain + '/WorkManagers')
        workmanager_name_list = cmo.getWorkManagers()
        lista = []
        for item in workmanager_name_list:
            work = str(item)
            work = work.split("=", 1)[1]
            work = work.split(",", 1)[0]
            lista.append(str(work))
        return lista
    except raiseWLSTException:
        raise

def convert_dict(lista):
    """
    Function to convert a List type into dictionary
        :param lista:           Receive a List type.
        :return:                Return a dictionary.
    """
    dic = {}
    lista = lista[0].split(",")
    for item in lista:
        dic[item.split(':',1)[0]] = item.split(':',1)[1]
    return dic

def get_worker(path):
    """ Function a little mess with strings
            :param path: Receive path of SelfTuning Ex. /SelfTuning/domain/WorkManagers....
            :return: Only type of workmanager
    """
    # Format path
    path = path.split("/")
    p = '/'.join(path[0:6])
    cd(p)

    # Get content from path
    redirect('/dev/null', 'false')
    l = ls(returnMap='True', returnType='c')
    redirect('/dev/null', 'true')

    # Check if there's any relevant value
    if l is None or l is [] or len(l) < 3:
        # Return nothing
        return None
    else:
        # Format and return value
        l = l.split()
        l = str(l[1])
        return l

def get_params(dic):
    try:
        for key in dic:
            for subkey in dic[key]:
                if subkey in ['target', 'targettype']:
                    dic[key][subkey] = str(get(dic[key][subkey])).split(" ")
                else:
                    dic[key][subkey] = get(dic[key][subkey])
                #
            #
        #
        return dic 
    except raiseWLSTException:
        raise

# Main
# Load credentials
username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Connect to a existing weblogic
connect(username, password, 't3://' + hostname + ':7001')

# Convert content received
data = convert_dict(contents)

# Get keys and return a dictionary
domain = get_domainName()
if domain is None:
    print '{}'
    sys.exit(0)
else:
    cluster = get_clusters()
    workers_list = get_workmanagerName(domain)

#
dic = {}

# Tuple of properties for workmanager default
tuple_values = ('defaultFairShareReqClass', 'defaultCapacityConstraint', 'defaultMaxThreadsConstraint', 'defaultMinThreadsConstraint')

for worker in workers_list:
    dic[worker] = {}
    # Replacements
    for key in data:
        value = data[key]
        value = value.replace('{DomainName}', domain)
        value = value.replace('{WorkManagerName}', worker)
        value = value.replace('{ClusterName}', cluster[0])

        # This is a hotfix for some WLS not having all workers configurated properly.
        if get_worker(value) is None or get_worker(value) is []:
            continue
        else:
            value = value.replace('{worker}', get_worker(value))
            dic[worker][key] = value


# Do the magic
gathered_information = get_params(dic)

# Print dictionary
print gathered_information
