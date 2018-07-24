import os
import sys
import ast
import yaml
import fnmatch
import subprocess as sub


def gen_find(filepat, topdir):
    """
    Function to find file recursively.
        :param filepat:     File name
        :param topdir:      Top dir name
        :return:            Full path of file
    """
    for path, dirlist, filelist in os.walk(topdir):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

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
    functionalities.
        :param credentials:     Receive a list with all credentials to an
        Weblogic server.
        :param event_name:      Receive the name of the function/script to call
        for it.
        :param content:         Receive the content to pass to the children
        (list/string).
        :return:                Return the raw output from WLST subprocess.
    """
    # Static definitions
    username = credentials[0]
    password = credentials[1]
    hostname = credentials[2]
    event_path = './functions/{0}.py'.format(event_name)

    wlst_path = gen_find("wlst.sh", "/app")
    for item in wlst_path:
        wlst_path = item
        break

    # Ensure wlst exists to call it
    if not os.path.isfile(wlst_path):
        print "Error: 'Weblogic Script Tool' not found."
        exit(1)

    # Ensure event_path exists to call it
    if not os.path.isfile(event_path):
        print "Event: {0} not found, skipping...".format(event_path)
        return None

    # Execute process
    if type(content) == list:
        ps = sub.Popen((wlst_path, event_path, username, password, hostname, str(content[0]), str(content[1])), stdout = sub.PIPE)
    else:
        ps = sub.Popen((wlst_path, event_path, username, password, hostname, str(content)), stdout = sub.PIPE)
    ps.wait()

    # Get ouput and return it
    output, errors = ps.communicate()
    output = output.splitlines()
    return output

# -------------------------------------------------------------------------- #
# Script session
# Main
# Set debug option, useful when developing some feature
debug = True

# Load template
data = {}
hiera_file = [
    "teste.yaml",
    "template-teste.yaml",
    "template.yaml"
]

for template_file in hiera_file:
    if os.path.isfile(template_file):
        data = data_load(template_file)
        break
    else:
        continue

# Get access credentials to weblogic server
credentials = [
    '{0}'.format(data['profile_weblogic::single_domain::weblogic_user']),
    '{0}'.format(data['profile_weblogic::single_domain::weblogic_password']),
    '{0}'.format(data['profile_weblogic::single_domain::adminserver']),
]

# Trigger all events on template
for index, key in enumerate(data):
    # Avoid using first 3 keys (credentials)
    if data[key] in credentials:
        continue

    # Get event name (last valid word on key)
    event = key.split(":")
    event = event[-1]

    # Ignore key
    if event in ['livelo_custom_directories', 'source_scripts']:
        continue

    # DEBUG feature.
    # enable otion to run only in one key
    if len(sys.argv) > 1:
        if sys.argv[1] != event:
            # Go to next iteration
            print "Skipping event: " + event
            continue
        else:
            print "Triggering event: " + event


    # Check if there's keys inside the gathered key that works as
    #  a template or for some static usage.
    if key_is_template(data[key]):
        # Create list of contents
        contents = []
        for subkey in data[key]:
            # Get contents (list type)
            contents.append(convert_dic_to_string(data[key][subkey]))
    else:
        # Get contents (string type)
        contents = convert_dic_to_string(data[key])

    # Call functions
    print "Retrieving: " + event
    if debug == True:
        print "Contents: " + str(contents)
    status = call_children(credentials, event, contents)

    # Get only valid outputs from all of it
    if status is not None:
        result = content_filter(status)
    else:
        result = None

    # Collect data gathered and update json
    if result is not None:
        data[key] = yaml.load(result)

    # end of loop
    if debug is True:
      print "-----------------------------------------------------------"
      print "DEBUG: Showing data gathered at instance:"
      print "Event: {0}".format(event)

      print "Raw output:"
      for line in status:
        print "\t" + line
      print "\n"

      print "Relevant output"
      print result
      print "\n"

      print "End of DEBUG mode"
      print "-----------------------------------------------------------"

    #
    continue
#
## Print transformed yaml-template
if debug is False:
    with open ('gathered-data.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style = False)
    print "Done!"

