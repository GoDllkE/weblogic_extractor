import sys

sys.path.insert(0, 'functions/')
from extensions import convert_dict

def get_machines():
    """
        This function get machines throughout method cmo.getMachines
        :return: A list of machines
    """
    try:
        machines = cmo.getMachines()
        lista = []
        for x in machines:
           a = str(x)
           a = a.split("=")
           a = a[1].split(",")
           lista.append(a[0])
        return lista
    except raiseWLSTException:
        raise


def get_params(machine_hash):
    """
        This function lookup the key values from certain dictionary
        :param 
        :return: return a dictionary with lookup key[machines] amd values
    """
    for machine in machine_hash:
        for key in machine_hash[machine]:
            machine_hash[machine][key] = get(machine_hash[machine][key])
    return machine_hash


# Main

username = sys.argv[1]
password = sys.argv[2]
hostname = sys.argv[3]
contents = sys.argv[4:]

# Connection string
connect(username, password, 't3://' + hostname + ':7001')

# Fuction for get array of machines
machines = get_machines()

# Function to create a dictionary
parameters = convert_dict(contents)
machine_hash = {}

# Interactive array and replace variables with contains '{MachineName}' to another receive parameter
for machine in machines:
   machine_hash[machine] = {}
   for parameter in parameters:
       machine_hash[machine][parameter] = parameters[parameter].replace('{MachineName}', machine)

# Relevant output
print get_params(machine_hash)
