from pprint import pprint
import time, sys, redis, random

import monitoring, config.parameters as _params

from config.parameters import backend_experiment_db

print("I'm starting the Experiment Operations")
index=0
customer_services = {}

def add_experiment(experiment):
	print("experiment: " + str(experiment))
	return add(experiment['service_name'], experiment['params'])

def del_experiment(experiment):
	customer_service_name = experiment['service_name']
	if (backend_experiment_db.exists(customer_service_name)):
		backend_experiment_db.delete(customer_service_name)
		return "Customer Service " + customer_service_name + " has been removed from the queue" + "\n"
	return "Customer Service " + customer_service_name + " wasn't found in the queue" + "\n"

def add(customer_service_name, params):
	print("**************************************")
	if (backend_experiment_db.exists(customer_service_name)):
		result = "\n" + "Customer Service " + customer_service_name + " already registered" + "\n"
		return result
	exp_id = "exp_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	backend_experiment_db.set(customer_service_name, {'id':exp_id, 'params':params})
	result  = "\n" + "**************************************" + "\n"
	result += "A new experiment has just been added" + "\n"
	result += "ID: " + str(exp_id) + "\n" 
	result += "Service Name: " + str(customer_service_name) + "\n" 
	result += "Parameters: " + str(params) + "\n" 
	result += "**************************************" + "\n"
	return result
