from pprint import pprint
import shlex, subprocess, json

def create(image_url, service_name, replicas):
	output = ""
	try:
		output = subprocess.check_output(['docker','service', 'create', '--name', service_name,'--replicas', str(replicas), image_url])
	except Exception as e:
		output = "Error happened : " + str(e)
	return output

def scale(service_name, replicas):
	output = ""
	try:
		output = subprocess.check_output(['docker','service', 'scale', service_name + '=' + str(replicas)])
	except Exception as e:
		output = "Error happened : " + str(e)
	return output

def replicas():
	try:
		output = subprocess.check_output(['docker','service', 'ls', '-q'])
		replicas_list = {}
		services = str(output,'utf-8').splitlines()
		for service in services:
			output = subprocess.check_output(['docker','service', 'inspect', service])
			data_json = json.loads(str(output,'utf-8'))
			service_id = data_json[0]['ID']
			service_name = data_json[0]['Spec']['Name']
			replicas = data_json[0]['Spec']['Mode']['Replicated']['Replicas']
			replicas_list[service_name] = {'id': service_id, 'replicas':replicas}
			
	except Exception as e:
		pass
	return replicas_list

def replicas(service_name):
	result = {}
	try:
		output = subprocess.check_output(['docker','service', 'inspect', service_name])
		data_json = json.loads(str(output,'utf-8'))
		service_id = data_json[0]['ID']
		service_name = data_json[0]['Spec']['Name']
		replicas = data_json[0]['Spec']['Mode']['Replicated']['Replicas']
		result = {'id': service_id, 'service_name': service_name, 'replicas':replicas}		
	except Exception as e:
		pass

	return result

#create('osabuoun/python_echo_app', 'test_name' , 3)
#print(scale('test_name',6))
print(replicas('test_name1'))
