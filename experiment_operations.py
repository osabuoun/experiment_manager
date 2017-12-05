from pprint import pprint
import time, sys, redis, random, http.client, urllib.parse

import monitoring, config.parameters as _params

from config.parameters import backend_experiment_db

print("I'm starting the Experiment Operations")
index=0
customer_services = {}

def add_experiment(experiment):
	print("experiment: " + str(experiment))
	exp_id = "exp_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	experiment_service_name = experiment['service_name']
	experiment_params = experiment['params']  
	experiment_command = experiment['command']  
	output = add_service(exp_id, '', experiment_service_name, experiment_params )
	for job in experiment['jobs']:
		job_service_name = ""
		job_params = []
		try:
			job_service_name = job['service_name'] 
		except Exception as e:
			job_service_name = experiment_service_name
		try:
			job_params = job['params'] 
		except Exception as e:
			job_params = experiment_params
		output = output + add_service(exp_id, job['id'], job_service_name, job_params)
		output = output + add_job(job)
	return output

def del_experiment(experiment):
	customer_service_name = experiment['service_name']
	if (backend_experiment_db.exists(customer_service_name)):
		backend_experiment_db.delete(customer_service_name)
		return "Customer Service " + customer_service_name + " has been removed from the queue" + "\n"
	return "Customer Service " + customer_service_name + " wasn't found in the queue" + "\n"

def add_service(exp_id, job_id,  customer_service_name, params):
	print("**************************************")
	if (backend_experiment_db.exists(customer_service_name)):
		#result = "\n" + "Customer Service " + customer_service_name + " already registered" + "\n"
		return ""
	backend_experiment_db.set(customer_service_name, {'exp_id':exp_id, 'job_id':job_id, 'params':params})
	result  = "\n" + "**************************************" + "\n"
	result += "A new experiment has just been added" + "\n"
	result += "ID: " + str(exp_id) + "\n" 
	result += "Service Name: " + str(customer_service_name) + "\n" 
	result += "Parameters: " + str(params) + "\n" 
	result += "**************************************" + "\n"
	return result

def add_job(job):
	params = urllib.parse.urlencode(job)
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPConnection("localhost:8778")
	conn.request("POST", "", params, headers)
	response = conn.getresponse()
	data = response.read()
	output = "\n"
	output = output + "job_id:" + job['id']
	output = output + ", Status:" + response.status 
	output = output + ", Reason:" + response.reason 
	output = output + ", data:" + data 
	output = output + "\n"
	response = conn.getresponse()
	conn.close()
	return output