import os
import yaml
import json
import subprocess as sub 
import ast


def data_load(file_input):
    """
    :param file_input:
    :return:
    """
    try:
        with open(file_input, "r") as stream:
            data = yaml.load(stream)
            return data

    except IOError as e:
        return e


def convert_dic_to_string(hash_input):
    str1 = ""
    for x in hash_input:
        if x == hash_input.keys()[-1]:
            str1 = str1 + "{0}:{1}".format(x, hash_input[x])
        else:
            str1 = str1 + "{0}:{1},".format(x, hash_input[x])
    return str1


def convert_string_to_dict(string_input):
    return ast.literal_eval(string_input)


def domain_configuration(data):
    """
    :param data:
    :return:
    """
    data = data["profile_weblogic::single_domain::adminserver::domain_configuration"]
    data = convert_dic_to_string(data)
    ps = sub.Popen(('/app/product/oracle/fmw/oracle_common/common/bin/wlst.sh', '/root/filho.py', str(data)), stdout = sub.PIPE)
    ps.wait()
    output, errors = ps.communicate()
    output = output.splitlines()
    for i,x in enumerate(output):
       if i < 13:
           pass
       else:
           return x

# Main

data = data_load("template.yaml")
data["profile_weblogic::single_domain::adminserver::domain_configuration"] = convert_string_to_dict(domain_configuration(data))
print yaml.dump(data, default_flow_style = False)




# How to mount example: 
#data = "log_number_of_files_limited:/Log/{DomainName}/NumberOfFilesLimited,security_crossdomain:/SecurityConfiguration/{DomainName}/CrossDomainSecurityEnabled,log_rotate_logon_startup:/Log/{DomainName}/RotateLogOnStartup,jta_transaction_timeout:/JTA/{DomainName}/TimeoutSeconds,log_filename:/Log/{DomainName}/FileName,log_rotationtype:/Log/{DomainName}/RotationType,log_file_min_size:/Log/{DomainName}/FileMinSize,jta_max_transactions:/JTA/{DomainName}/MaxTransactions,log_filecount:/Log/{DomainName}/FileCount"

