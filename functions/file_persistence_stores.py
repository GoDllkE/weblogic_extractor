import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_file_stores():
    """
        Function takes the name of the FileStores through the method cmo.getFileStores
        :return: A list of FileStores
    """
    try:
        file_stores = cmo.getFileStores()
        fs_array = []
        for file_store in file_stores:
           fs = str(file_store)
           fs = fs.split("=")
           fs = fs[1].split(",")
           fs_array.append(fs[0])
        return fs_array
    except raiseWLSTException:
        raise

def get_params(dic):
    try:
        for key in dic:
            for subkey in dic[key]:
                if subkey in ['target']:
                    dic[key][subkey] = str(dic[key][subkey]).split(" ")
                elif subkey in ['targettype']:
                    dic[key][subkey] = str(get(dic[key][subkey])).split(" ")
                else:
                    dic[key][subkey] = get(dic[key][subkey])
                #
            #
        #
        return dic
    except raiseWLSTException:
        raise

#def get_params(fs_hash):
#   """
#       Function lookup the key values from certain dictionary
#           :param machines_hash: Receives a dictionary that contains the name of
#            the machines
#           :return: Return a dictionary with lookup key[machines] amd values
#   """
#   for file_store in fs_hash:
#       for key in fs_hash[file_store]:
#           if key == 'target':
#               fs_hash[file_store][key] = '[\'' + fs_hash[file_store][key] + '\']'
#           elif key == 'directory':
#               fs_hash[file_store][key] = get(fs_hash[file_store][key])
#           elif key == 'targettype':
#               fs_hash[file_store][key] = '[\'' + get(fs_hash[file_store][key]) + '\']'
#   return fs_hash

def get_targets(file_store):
    """
    """
    try:
        cd('/FileStores/' + file_store + '/Targets')
        target_list = cmo.getTargets()
        lista = []
        for target in target_list:
            tgt = str(target)
            tgt = tgt.split("=")
            tgt = tgt[1].split(",")
            lista.append(tgt[0])
        return lista[0]
    except raiseWLSTException:
        raise

# Main

username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Connection string
connect(username, password, 't3://' + hostname + ':7001')

# Fuction for get array of file_stores
file_stores = get_file_stores()

# String to dictionary conversion
parameters = convert_dict(contents)
fs_hash = {}

# Interactive array and replace variables with contains '{sever} and {file_store}'
# to another receive parameter
for file_store in file_stores:
    fs_hash[file_store] = {}
    for parameter in parameters:
        fs_hash[file_store][parameter] = parameters[parameter].replace('{server}', get_targets(file_store))
        fs_hash[file_store][parameter] = fs_hash[file_store][parameter].replace('{file_store}', file_store)

# Relevant output
print get_params(fs_hash)
