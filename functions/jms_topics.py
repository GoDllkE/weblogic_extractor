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

def get_jms_topic(cluster, modules):
    """
        Must return a LIST
    """
    try:
        listas = [[],[]]
        dic_tp = {}
        cd('/JMSSystemResources/' + cluster + '/JMSResource/' + modules + '/' + 'Topics')
        jms_topic = list(cmo.getTopics())

        cd('/JMSSystemResources/' + cluster + '/JMSResource/' + modules + '/' + 'UniformDistributedTopics')
        jms_topic_udt = list(cmo.getUniformDistributedTopics())

        for jms_tp in jms_topic:
            jms_tp = str(jms_topic)
            jms_tp = jms_tp.split("=")
            jms_tp = jms_tp[1].split(",")
            listas[0].append(jms_tp[0])
        dic_tp['Topic'] = listas[0]

        for jms_tp_udt in jms_topic_udt:
            jms_tp_udt = str(jms_tp_udt)
            jms_tp_udt = jms_tp_udt.split("=")
            jms_tp_udt = jms_tp_udt[1].split(",")
            listas[1].append(jms_tp_udt[0])
        dic_tp['UniformDistributedTopics'] =  listas[1]

        return dic_tp
    except raiseWLSTException:
        raise

def get_jms_deliveryParamsOverrides(cluster, modules, topic_type, topic_name):
    """
        Must return a STR
    """
    try:
        cd('/JMSSystemResources/' + cluster +'/JMSResource/' + modules + '/' + topic_type + '/' + topic_name + '/DeliveryParamsOverrides')
        jms_module = str(cmo.getDeliveryParamsOverrides())
        jms_module = jms_module.split("=", 1)[1]
        jms_module = jms_module.split(",", 1)[0]
        return jms_module
    except raiseWLSTException:
        raise



# def get_jms_cf_transactionParams(cluster, module, connectionFactory):
#   """
#       Must return a STR
#   """
#   try:
#       cd('/JMSSystemResources/' + cluster + '/JMSResource/' + module + '/ConnectionFactories/' + connectionFactory + '/TransactionParams')
#       jms_tp = str(cmo.getTransactionParams())
#       jms_tp = jms_tp.split("=", 1)[1]
#       jms_tp = jms_tp.split(",")[0]
#       return jms_tp
#   except raiseWLSTException:
#       raise

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
    jms_topic = get_jms_topic(jms_cluster, jms_module)

    for topic in jms_topic:
        if len(jms_topic[topic]) != 0:
            for topic_name in jms_topic[topic]:
                # Master key
                master_key = jms_cluster + ':' + topic_name
                dic[master_key] = {}

                for key in data:
                    # Gather required values
                    delivery_params = get_jms_deliveryParamsOverrides(jms_module, jms_cluster, topic, topic_name)

                    # Distributed key chumb
                    if topic == "UniformDistributedTopics":
                        dic[master_key]['distributed'] = 1
                    else:
                        dic[master_key]['distributed'] = 0

                    # Update value
                    value = data[key]
                    value = value.replace("{jms_module}", jms_module)
                    value = value.replace("{ClusterJmsModule}", jms_cluster)
                    value = value.replace("{TopicType}", topic)
                    value = value.replace("{TopicName}", topic_name)
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

