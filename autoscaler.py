#from docker import types

class Autoscaler:
	def __init__(self):
		'''
		try:
			#self.client = docker.from_env()
		except Exception as e:
			raise e
		#print("Docker Client: " + str(client))
		'''


import docker, time
from pprint import pprint
from docker import types
import shlex, subprocess

client = docker.from_env()
index = 1

#subprocess.run(["ls", "-l", "/"], stdout=subprocess.PIPE)

env = ["SERVER=172.17.0.1", "PORT=8777" , "INSTANCE=123"]
mode = types.ServiceMode(mode='replicated', replicas= index)
service = client.services.create("python-webclient", command=None, env= env, mode= mode)
print(service.id)
print(service.name)
print(service.tasks)

#client1.update_service(client1.services()[0]["ID"], version=client1.services()[0]["Version"]["Index"], task_template=task_template, name=client.services()[0]["Spec"]["Name"], labels=client.services()[0]["Spec"]["Labels"], mode=mode, update_config=update_config, networks=networks, endpoint_spec=endpoint_spec)

while True:
	pprint(vars(service))
	index += 5	
	output = subprocess.check_output(['docker','service', 'update', '--replicas', str(index), service.id ])
	#print(output)
	#print(service.tasks)
	print("--------------------------------------------")
	#mode = types.ServiceMode(mode='replicated', replicas= index)
	#print(mode)
	#service.update(name=service.name, env= env, mode=mode)
	time.sleep(15)
#service.remove()
