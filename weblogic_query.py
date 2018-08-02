import os
import sys
import ast
import yaml
import getopt
import subprocess as sub


def data_load(file_input):
    """
    Function to open a file and return the content.
        :param file_input:      File path.
        :return:                File content.
    """
    try:
        with open(file_input, "r") as stream:
            data = yaml.load(stream)
            return data

    except IOError as e:
        return e


def convert_dic_to_string(dictionary):
    """
    Function to convert Dict type into string type.
        :param dictionary:      Receive dict type.
        :return:                Return string type.
    """
    string = ""
    for key in dictionary:
        if key == list(dictionary.keys())[-1]:
            string = string + "{0}:{1}".format(key, dictionary[key])
        else:
            string = string + "{0}:{1},".format(key, dictionary[key])
    return string


def convert_string_to_dict(string):
    """
    Function to convert string type into dict.
        :param string:          Receive a string type.
        :return:                Return a dict type.
    """
    return ast.literal_eval(string)


def key_is_template(content):
    """
    Function to check if key has template-keys inside of it.
        :param content:         Receive a dict type.
        :return:                Return True/False to a key in reserved list.
    """
    list_protected_keys = ["AdminServer", "Server"]
    for key in list_protected_keys:
        for info in content:
            if key in info:
                # Key matches the reserved template-key
                return True
            continue
        continue
    # Any of those keys matched the reserver template-key
    return False


def content_filter(content):
    """
    Function to filter content received from a certain WLST subprocess.
        :param content:         Receive a WLST subprocess output.
        :return:                Return a refined WLST subprocess output.
    """
    # Jump to the line with desired content
    if content is None:
        print "No valid content found."
        return None
    else:
        return content[-1]


def call_children(credentials, event_name, content):
    """
    Function to call children functions to work with pre-historic WLST
    functionality.
        :param credentials:     Receive a list with all credentials to an
        Weblogic server.
        :param event_name:      Receive the name of the function/script to call
        for it.
        :param content:         Receive the content to pass to the children
        (list/string).
        :return:                Return the raw output from WLST subprocess.
    """
    # Static definitions
    wlst_path = None
    username = credentials[0]
    password = credentials[1]
    hostname = credentials[2]
    event_path = 'functions/{0}.py'.format(event_name)

    # List of possible locations for WLST
    wlst_path_list = [
        '/app/product/oracle/oracle_common/common/bin/wlst.sh',
        '/app/oracle/product/fmw/oracle_common/common/bin/wlst.sh',
        '/app/product/oracle/fmw/oracle_common/common/bin/wlst.sh'
    ]

    for path in wlst_path_list:
        if os.path.isfile(path):
            wlst_path = path

    if wlst_path is None:
        print 'Error: No WLST found!'
        sys.exit(0)

    # Ensure event_path exists to call it
    if not os.path.isfile(event_path):
        print "Event: {0} not found, skipping...".format(event_path)
        return None

    # Execute process
    if type(content) == list:
        ps = sub.Popen((wlst_path, event_path, username, password, hostname, str(content[0]), str(content[1])), stdout=sub.PIPE)
    else:
        ps = sub.Popen((wlst_path, event_path, username, password, hostname, str(content)), stdout=sub.PIPE)
    ps.wait()

    # Get output and return it
    output, errors = ps.communicate()
    output = output.splitlines()
    return output


# -------------------------------------------------------------------------- #
# Script session
# Main
# Set debug option, useful when developing some feature
debug = False
verbose = False
skip_event = False

# Load template.
# Change it as your necessity demands
data = {}
hiera_file = [
    "resources/teste.yaml",
    "resources/template-teste.yaml",
    "resources/template.yaml"
]

# List of empty keys founded on runtime.
remove_keys_list = []

# Template loading hierarchy
for template_file in hiera_file:
    if os.path.isfile(template_file):
        data = data_load(template_file)
        break
    else:
        continue

# Check credentials
# If they where default values... then update they and update template file.
# For username
if data['profile_weblogic::single_domain::weblogic_username'] == '<some-username>':
    data['profile_weblogic::single_domain::weblogic_username'] = raw_input("Insert the WLST username (default: weblogic): ")
    if len(data['profile_weblogic::single_domain::weblogic_username']) < 3:
        data['profile_weblogic::single_domain::weblogic_username'] = 'weblogic'

# For password
if data['profile_weblogic::single_domain::weblogic_password'] == '<some-password>':
    data['profile_weblogic::single_domain::weblogic_password'] = raw_input("Insert the WLST password: ")

# For hostname
if data['profile_weblogic::single_domain::weblogic_hostname'] == '<some-hostname>':
    data['profile_weblogic::single_domain::weblogic_hostname'] = raw_input("Insert the WLST hostname (default: "+os.uname()[1]+"): ")
    if len(data['profile_weblogic::single_domain::weblogic_hostname']) < 3:
        data['profile_weblogic::single_domain::weblogic_hostname'] = os.uname()[1]

# Get access credentials to weblogic server
credentials = [
    '{0}'.format(data['profile_weblogic::single_domain::weblogic_username']),
    '{0}'.format(data['profile_weblogic::single_domain::weblogic_password']),
    '{0}'.format(data['profile_weblogic::single_domain::weblogic_hostname']),
]

# Update template for future runtime
for template_file in hiera_file:
    if os.path.isfile(template_file):
        with open(template_file, "w") as temp_file:
            yaml.dump(data, temp_file, default_flow_style=False)
        break
    else:
        continue

# Remove specified key if not CLM technologies
for item in ['clm', 'tst']:
    if item in credentials[2]:
        if 'profile_weblogic::single_domain::livelo_custom_directories' in remove_keys_list:
            remove_keys_list.remove('profile_weblogic::single_domain::livelo_custom_directories')
        break
    else:
        if 'profile_weblogic::single_domain::livelo_custom_directories' not in remove_keys_list:
            remove_keys_list.append('profile_weblogic::single_domain::livelo_custom_directories')
        continue

# Trigger all events on template
for index, key in enumerate(data):
    # Avoid using first 3 keys (credentials)
    if data[key] in credentials:
        continue

    # Get event name (last valid word on key)
    event = key.split(":")
    event = event[-1]

    # Ignore keys
    if event in ['livelo_custom_directories', 'source_scripts']:
        continue

    # Retrieve options and arguments
    opts, args = getopt.getopt(sys.argv[1:], "dv", ['debug', 'verbose'])

    # Check if DEBUG option is enabled
    for option, value in opts:
        if option in ('-d', '--debug'):
            debug = True
        elif option in ('-v', '--verbose'):
            verbose = True
        else:
            debug = False
            continue
    #

    # Retrieve arguments
    if len(args) > 0:
        for arg_name in args:
            if arg_name != event:
                skip_event = True
            else:
                print "Triggering specified event: " + event
                skip_event = False
                break

    # Skip event
    if skip_event:
        remove_keys_list.append(key)
        skip_event = False
        continue

    # Check if there's keys inside the gathered key that works as a template or for some static usage.
    if key_is_template(data[key]):
        # Create list of contents
        contents = []
        for subkey in data[key]:
            # Get contents (list type)
            contents.append(convert_dic_to_string(data[key][subkey]))
    else:
        # Get contents (string type)
        contents = convert_dic_to_string(data[key])

    if debug:
        print "-----------------------------------------------------------"
        print "DEBUG: Showing data gathered at instance:"

    # Call functions
    if verbose or debug:
        print "Retrieving: " + event
    status = call_children(credentials, event, contents)

    # Get only valid outputs from all of it
    result = content_filter(status)

    if yaml.load(result) == {}:
        if verbose:
            print "Info: no content found at event '" + event + "'."
        remove_keys_list.append(str(key))
        continue
    else:
        # Collect data gathered and update json
        data[key] = yaml.load(result)

    # end of loop
    if debug:
        print "Raw output:"
        for line in status:
            print "\t" + line
        print "\n"
        print "Relevant output"
        print result
        print "\n"
        print "End of DEBUG for event " + event
    #
    continue
#
if verbose:
    print "Info: Removing empty content..."

# Remove empty keys
for item in remove_keys_list:
    data.pop(item)

if verbose:
    print "Info: Generating file..."

# Print transformed yaml-template
with open(credentials[2].split('.')[0].lower() + '.yaml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

# End of run
print "Extractor process complete!"
