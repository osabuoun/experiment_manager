from pprint import pprint
import time, sys, redis, random, http.client, urllib.parse
from celery import subtask

import monitoring, job_operations
from parameters import backend_experiment_db, JOB_QUEUE_PREFIX

from experiment import Experiment
print("I'm starting the Experiment Operations")
index=0
customer_services = {}

def add_experiment(experiment_json):
	output = "experiment_json: " + str(experiment_json)
	private_id = str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	service_name = experiment_json['image_url'] + "__" + private_id
	exp_id = "exp_" + private_id

	experiment = Experiment(exp_id, service_name)
	try:
		experiment.update('image_name', experiment_json['image_name'])
	except Exception as e:
		experiment.update('image_name', "")
	try:
		experiment.update('image_name', experiment_json['image_name'])
	except Exception as e:
		experiment.update('image_name', "")
		
	output += add_service(exp_id, service_name , experiment_json['params'] )
	if (isinstance(experiment_json['jobs'], list)):
		output += process_job_list(exp_id, experiment_json)
	else:
		output += process_job_array(exp_id,experiment_json)
	print(output)
	return output

def get_task_count(tasks):
	count = 0
	try:
		if (isinstance(tasks, list)):
			count = len(tasks)
		else:
			count = tasks['count']
	except Exception as e:
		count = 0
	return count 

def process_job_list(exp_id, experiment):
	print("There is a list of " + str(len(experiment['jobs'])))
	output = ""
	for job in experiment['jobs']:
		try:
			job_service_name = job['service_name'] 
		except Exception as e:
			job['service_name'] = experiment['service_name']
		try:
			job_params = job['params'] 
		except Exception as e:
			job['params'] = experiment['params'] 
		try:
			job_command = job['command'] 
		except Exception as e:
			job['command'] = experiment['command']

		output += add_service(exp_id, job['service_name'], job['params'], job['id'])
		output += add_job(exp_id, job)
	return output

def process_job_array(exp_id, experiment):
	output = ""
	jobs = experiment['jobs']
	print("There is an array of " + str(jobs['count']))
	try:
		job_service_name = jobs['service_name'] 
	except Exception as e:
		jobs['service_name'] = experiment['service_name']
	try:
		job_params = jobs['params'] 
	except Exception as e:
		jobs['params'] = experiment['params'] 
	try:
		job_command = jobs['command'] 
	except Exception as e:
		jobs['command'] = experiment['command']
	output += add_service(exp_id, jobs['service_name'], jobs['params'], jobs['id'])
	for x in range(0,jobs['count']):
		job_id = jobs['id'] + "_" + str(x)
		output += add_job(exp_id, jobs)
	return output

def del_experiment(experiment):
	customer_service_name = experiment['service_name']
	if (backend_experiment_db.exists(customer_service_name)):
		backend_experiment_db.delete(customer_service_name)
		return "Customer Service " + customer_service_name + " has been removed from the queue" + "\n"
	return "Customer Service " + customer_service_name + " wasn't found in the queue" + "\n"

def add_service(exp_id, service_name, parameters, job_id = ""):
	result  = "\n" + "**************************************" + "\n"
	if (backend_experiment_db.exists(service_name)):
		return ""
	backend_experiment_db.set(service_name, {'exp_id':exp_id, 'job_id':job_id, 'params':parameters})
	result += "A new service has just been added" + "\n"
	result += "Exp_ID: " + str(exp_id) + "\n" 
	result += "Service Name: " + str(service_name) + "\n" 
	result += "Parameters: " + str(parameters) + "\n" 
	result += "**************************************" + "\n"
	return result

def add_job(exp_id, job):
	job_queue_id = "j_" + job['service_name'] +"_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	output = "job_queue_id:" + job_queue_id
	output += "JOB_QUEUE_PREFIX:" + JOB_QUEUE_PREFIX
	output += "service_name:" + job['service_name']
	chain = subtask('job_operations.add', queue = JOB_QUEUE_PREFIX + job['service_name'])
	chain.delay(exp_id, job_queue_id, job)
	monitoring.add_job(exp_id, job['service_name'], job_queue_id)
	output += "\n" + "------------------------------------" + "\n"
	output += "The job " + str(job['id']) + " has just been added" + "\n"
	task_count = get_task_count(job['tasks'])
	monitoring.add_task(exp_id, job['service_name'], job_queue_id, task_count)
	output += "The job " + str(job['id']) + " has " + str(task_count) + " tasks, they have just been added" + "\n"
	output += "------------------------------------" + "\n"
	return output
