import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def domain_configuration(parameters):
    """
    Function for keys lookup.
        :param parameters:      Receive a Dictonary type.
        :return:                Return dictonary if real values
    """
    try:
        domain_name = get('Name')
        for key in parameters:
            var = parameters[key].replace('{DomainName}', domain_name)
            parameters[key] = get(var)
        return parameters
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


# Main
# Load credentials
username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Connect to a existing weblogic
connect(username, password, 't3://' + hostname + ':7001')

# Get keys and return a dictionary
ret = domain_configuration(convert_dict(contents))

# Print dictionary
print ret
