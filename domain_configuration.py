import os
import sys

def domain_configuration(parameters):
    try:
        domain_name =get('Name')
        for key in parameters:
            var = parameters[key].replace('{DomainName}', domain_name)
            parameters[key] = get(var)
        return parameters
    except raiseWLSTException:
        raise

def convert_dict(lista):
    dic = {}
    lista = lista[0].split(",")
    for item in lista:
        dic[item.split(':',1)[0]] = item.split(':',1)[1]
    return dic


# Main
username = 'weblogic'
password = 'Livelo@@15'
admin = 'vbntst803liv'

connect(username, password, 't3://' + admin + ':7001')

ret = domain_configuration(convert_dict(sys.argv[1:]))
print ret
