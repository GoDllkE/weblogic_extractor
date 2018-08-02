import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_servers():
    """
        Function to get all servers included AdminServer
            :result: Return array of servers
                Ex.: ['AdminServer', 'ms1', 'ms2']
    """
    try:
        servers =  cmo.getServers()
        servers_array = []
        for server in servers:
           server = str(server)
           server = server.split("=")
           server  = server[1].split(",")
           servers_array.append(server[0])
        return servers_array
    except raiseWLSTException:
        raise

def get_params(dic):
    """
        Function to get all parameters recived in the keys of dictionary
            :param dic: Dictionary that contain all parameters that to owe checked
                Ex.: {'arguments':'/Servers/ms1/ServerStart/ms1/Arguments'}
            :result dic: Return dictionary with values substituted per new values collected
                Ex.:
    """
    for server in dic:
        for key in dic[server]:
            if key in ['custom_identity']:
                dic[server][key] = get_custom_identity(dic[server][key])
            elif key in ['timeout']:
                dic[server][key] = '60'
            elif key in ['listenport']:
                dic[server][key] = get(dic[server][key])
                # Hotfix for Nonetype
                if dic[server][key] is None or dic[server][key] == 'None':
                    dic[server][key] = 0
                # Hotfix for stringtype
                if type(dic[server][key]) is not int:
                    dic[server][key] = int(dic[server][key])
            else:
                dic[server][key] = get(dic[server][key])
    return dic

def get_machine(server):
    """
        Function that takes the machines corresponding to the managed servers
        :param server: Name of managed server Ex. ms1
        :result: Name of machine correspondig to the managed server
    """
    cd('/Servers/' + server + '/Machine')
    machine = cmo.getMachine()
    machine = str(machine)
    machine = machine.split("=")
    machine = machine[1].split(",")
    machine = machine[0]
    return machine


def get_custom_identity(mbean):
    """
        Function to set custom_identity, according with o return the mbean /Servers/ms1/KeyStore
        :param mbean: /Servers/ms1/KeyStore
        :result: 0 or 1 according with return /Servers/ms1/KeyStore
    """
    bean = get(mbean)
    if bean == "DemoIdentityAndDemoTrust":
        return 0
    else:
        return 1

# Main
username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
content_srv = sys.argv[4]
content_adm = sys.argv[5]

# Connection string
connect(username, password, 't3://' + hostname + ':7001')

# Fuction for get array of servers
servers = get_servers()

# Create a bucket of arrays
bucket = []
bucket.append(content_srv)
bucket.append(content_adm)

# Create hash of servers
servers_hash = {}
for server in servers:
   servers_hash[server] = {}


# Interactive array and replace variables with contains '{server}' to another receive parameter
for server in servers_hash:
    if server == 'AdminServer':
        servers_hash[server] = convert_dict(bucket[0].replace("{MachineName}", get_machine(server)))
    else:
        var = bucket[1].replace("{server}", server)
        var = var.replace("{MachineName}", get_machine(server))
        servers_hash[server] = convert_dict(var)


# Relevant output
result = get_params(servers_hash)
print result

