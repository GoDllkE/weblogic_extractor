# Funcao primo

def convert_dict(params):
	dic = {}
	if type(params) == list:
		params = params[0].split(",")
	else:
		params = params.split(",")

	for item in params:
		dic[item.split(':',1)[0]] = item.split(':',1)[1]
	return dic
