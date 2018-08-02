import os
import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_folders(location):
    try:
        cd(location)
        redirect('/dev/null', 'false')
        folders = list(ls(returnMap='true', returnType='c'))
        redirect('/dev/null', 'true')

        # Return a list of folders
        return folders
    except raiseWLSTException:
        raise

def get_domainName():
    try:
        domain = get_folders('/SelfTuning')
        if len(domain) < 2:
            return str(domain[0])
        else:
            return domain
    except raiseWLSTException:
        raise

def get_workerstype(domain):

    try:
        workerstype = get_folders('/SelfTuning/' + domain)

        # Exceptions list
        for item in workerstype:
            if item not in ['FairShareRequestClasses', 'MinThreadsConstraints', 'MaxThreadsConstraints', 'Capacities']:
                workerstype.remove(item)

        # Dont know why dont del this one
        workerstype.remove('WorkManagers')

        return workerstype
    except raiseWLSTException:
        raise

def get_workmanagerName(domain_name, folder):
    try:
        workersname = get_folders('/SelfTuning/'+domain+'/'+folder)
        return workersname
    except raiseWLSTException:
        raise

def get_clusterName(domain, folder, worker):
    try:
        clustername = get_folders('/SelfTuning/'+domain+'/'+folder+'/'+worker+'/Targets')
        if len(clustername) < 2:
            return str(clustername[0])
        else:
            return str(clustername)
    except raiseWLSTException:
        raise

def get_params(dic):
    try:
        for key in dic:
            for subkey in dic[key]:
                if subkey in ['target', 'targettype']:
                    dic[key][subkey] = str(get(dic[key][subkey])).split(" ")
                elif subkey in ['constrainttype']:
                    dic[key][subkey] = str(get(dic[key][subkey])).replace('FairShareRequestClass','FairShareRequestClasses')
                else:
                    dic[key][subkey] = get(dic[key][subkey])
                #
            #
        #
        return dic
    except raiseWLSTException:
        raise

# ---------------------------------------------------------------------------- #
# Script
username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Weblogic connection
connect(username, password, 't3://'+hostname+':7001')

# Contents convertion
data = convert_dict(contents)

# Required information
domain = get_domainName()
folder_list = get_workerstype(domain)

#
dic = {}

#
for folder in folder_list:
    # Get more of missing information
    workers_list = get_workmanagerName(domain, folder)


    for worker in workers_list:
        # Get more of missing information
        cluster = get_clusterName(domain, folder, worker)

        #
        dic[worker] = {}

        for key in data:
            #
            value = data[key]

            value = value.replace('{DomainName}', domain)
            value = value.replace('{FolderName}', folder)
            value = value.replace('{WorkManagerName}', worker)
            value = value.replace('{ClusterName}', cluster)

            # Change property name based on constraint category
            if folder == 'FairShareRequestClasses':
                value = value.replace('{Property}', 'FairShare')
            else:
                value = value.replace('{Property}', 'Count')

            # Save to dic
            dic[worker][key] = value
        #
    #
#
gathered_values = get_params(dic)

#
print gathered_values
