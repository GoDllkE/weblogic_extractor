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

def get_jms_queue(cluster, modules):
    """
        Must return a LIST
    """
    try:
        listas = [[],[]]
        dic_tp = {}
        cd('/JMSSystemResources/' + cluster + '/JMSResource/' + modules + '/' + 'Queues')
        jms_queue = list(cmo.getQueues())
        
        cd('/JMSSystemResources/' + cluster + '/JMSResource/' + modules + '/' + 'UniformDistributedQueues')
        jms_queue_udt = list(cmo.getUniformDistributedQueues())
        
        for jms_q in jms_queue:
            jms_q = str(jms_queue)
            jms_q = jms_q.split("=")
            jms_q = jms_q[1].split(",")
            listas[0].append(jms_q[0])
        dic_tp['Queue'] = listas[0]

        for jms_q_udt in jms_queue_udt:
            jms_q_udt = str(jms_q_udt)
            jms_q_udt = jms_q_udt.split("=")
            jms_q_udt = jms_q_udt[1].split(",")
            listas[1].append(jms_q_udt[0])
        dic_tp['UniformDistributedQueues'] =  listas[1]

        return dic_tp
    except raiseWLSTException:
        raise

def get_jms_deliveryParamsOverrides(cluster, modules, queue_type, queue_name):
    """
        Must return a STR
    """
    try:
        cd('/JMSSystemResources/' + cluster +'/JMSResource/' + modules + '/' + queue_type + '/' + queue_name + '/DeliveryParamsOverrides')
        jms_module = str(cmo.getDeliveryParamsOverrides())
        jms_module = jms_module.split("=", 1)[1]
        jms_module = jms_module.split(",", 1)[0]
        return jms_module
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
            if key != "distributed":
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
    jms_queue = get_jms_queue(jms_cluster, jms_module)

    for queue in jms_queue:
        if len(jms_queue[queue]) != 0:
            for queue_name in jms_queue[queue]:
                # Master key
                master_key = jms_cluster + ':' + queue_name
                dic[master_key] = {}

                for key in data:
                    # Gather required values
                    delivery_params = get_jms_deliveryParamsOverrides(jms_module, jms_cluster, queue, queue_name)
                    # Distributed key chumb
                    if queue == "UniformDistributedQueues":
                        dic[master_key]['distributed'] = 1
                    else:
                        dic[master_key]['distributed'] = 0


                    #Update value
                    value = data[key]
                    value = value.replace("{jms_module}", jms_module)
                    value = value.replace("{ClusterJmsModule}", jms_cluster)
                    value = value.replace("{QueueType}", queue)
                    value = value.replace("{QueueName}", queue_name)
                    value = value.replace("{DeliveryParams}", delivery_params)

                    # Save to dict
                    dic[master_key][key] = value
                    continue
                continue
        else:
            pass
        continue
    continue

# Do the magic
gathered_information = get_params(dic)

# Print dictionary
print gathered_information

