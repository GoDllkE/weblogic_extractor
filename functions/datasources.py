import os
import re
import sys

import weblogic.security.internal.SerializedSystemIni
import weblogic.security.internal.encryption.ClearOrEncryptedService

sys.path.insert(0, 'functions/')
from extensions import convert_dict


def get_folders(location):
    # Return a list of folders
    try:
        cd(location)
        redirect('/dev/null', 'false')
        folders = list(ls(returnMap='true', returnType='c'))
        redirect('/dev/null', 'true')
        return folders
    except raiseWLSTException:
        raise

def get_domain():
    """
    Function for keys lookup.
        :param parameters:      Receive a Dictonary type.
        :return:                Return dictonary if real values
    """
    try:
        domain_name = get('Name')
        return domain_name
    except raiseWLSTException:
        raise

def get_clusters(key_path):
    """
        This function get clusters from a specified path
        :return: A list of clusters
    """
    path = ""
    path_list = key_path.split('/')[1:4]
    for item in path_list:
        path = path + '/' + item
    return get_folders(str(path))[0]

def get_jdbc_clusters():
    """
        This function get clusters through cmo method.
        :return: A list of clusters
    """
    try:
        return get_folders('/JDBCSystemResources')
    except raiseWLSTException:
        raise

def get_datasources_targets(data, cluster):
    try:
        lista = []
        cd(data[cluster]['target'])
        servers = cmo.getTargets()
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

def get_xml_list(domain_name):
    lista = []
    config_paths = [
        '/app/product/oracle/wlsdomains/{domainName}/config/jdbc/',
        '/app/oracle/admin/{domainName}/aserver/{domainName}/config/jdbc/'
    ]

    for item in config_paths:
        # Format path from list
        item = item.replace('{domainName}', domain_name)

        # Check if it exists and have some 'xml' file in.
        if os.path.isdir(item):
            files = os.listdir(item)
            for content in files:
                if content.endswith('.xml'):
                    # Append file to list
                    lista.append(item + content)
                    break
    return lista

def clear_tags(hashtag):
    # Format hash throughout regex
    regex = re.compile('<.*?>')
    textr = re.sub(regex, '', hashtag)
    return textr

def decrypt_password(hashtext, cluster_name):
    # Instance of some weblogic core modules to decrypt password
    service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(cluster_name)
    crypt = weblogic.security.internal.encryption.ClearOrEncryptedService(service)
    return crypt.decrypt(hashtext)

def return_password(lista_xml):
    # Linter troubleshooting
    domain = None
    content = None

    for item in lista_xml:
        # Load file content
        file_data = open(item, 'rt')
        content = file_data.read().split()
        # Check path to split and retrieve domain path
        if 'wlsdomains' in item:
            domain = item.split('/')[1:6]
        else:
            domain = item.split('/')[1:7]

    # Format domain path
    dom = ""
    for item in domain:
        dom = dom + '/' + item

    # Decrypt key
    hashtag = None
    for item in content:
        if 'password-encrypted' in item:
            hashtag = clear_tags(item)
    return decrypt_password(hashtag, dom)

def get_params(dicionario):
    """
        This function lookup the key values from certain dictionary
        :return: return a dictionary with lookup key[clusters] amd values
    """
    for cluster in dicionario:
        for key in dicionario[cluster]:
            if key in ['target']:
                dicionario[cluster][key] = get_datasources_targets(dicionario, cluster)
            elif key in ['jndinames']:
                dicionario[cluster][key] = str(get_jndinames(get(dicionario[cluster][key]))).split()
            elif key in ['usexa', 'testconnectionsonreserve']:
                dicionario[cluster][key] = str(get(dicionario[cluster][key]))
            elif key in ['password']:
                continue
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
domain_name = get_domain()
cluster_list = get_jdbc_clusters()

# Interactive array and replace variables with contains '{clusterName}' to another receive parameter
dicionario = {}
for jdbc_cluster in cluster_list:
    dicionario[jdbc_cluster] = {}

    for key in data:
        # Make substitutions
        dicionario[jdbc_cluster][key] = data[key].replace('{ClusterJDBC}', jdbc_cluster)

        # Only exception on datasources. Can change as no pattern is settled.
        if key in ['targettype']:
            # Get the ClusterName in specified path
            cluster_name = get_clusters(str(dicionario[jdbc_cluster][key]))

            # Make substitution
            dicionario[jdbc_cluster][key] = dicionario[jdbc_cluster][key].replace('{ClusterName}', str(cluster_name))

        # Ensure password configurations
        elif key in ['password']:
            lista_files_xml = get_xml_list(domain_name)
            dicionario[jdbc_cluster][key] = return_password(lista_files_xml)

    continue

#
data = get_params(dicionario)

for key in data:
    data[key]['ensure'] = "present"

print data

