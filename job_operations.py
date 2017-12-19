from __future__ import absolute_import, unicode_literals
import time, shlex, subprocess, random

from jqueuing_worker import job_app
import jqueuing_worker as jqw
import monitoring
import celery

print("Job Operations - Started")

class MyTask(celery.Task):
	def on_failure(self, exc, task_id, args, kwargs, einfo):
		print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
		print('{0!r} failed: {1!r}'.format(task_id, exc))
		print("/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")

def process_list(exp_id, job_queue_id, job):
	for task in job['tasks']:
		output = ""
		myfile.write("-------------------------------------\n")
		myfile.write("Task: " + str(task) + "\n")
		try:
			task_command = task['command'] 
		except Exception as e:
			task['command'] = job['command']
		try:
			task_data = task['data'] 
		except Exception as e:
			tasks['data'] = job['data']
		
		task_start_time = time.time()
		monitoring.run_task(node_id, exp_id,service_name, worker_id, job_queue_id, task["id"])
		try:
			command = ['docker','exec', container_id] + task_command + [str(task["data"])]
			output = subprocess.check_output(command)
		except Exception as e:
			monitoring.task_failed(node_id, exp_id, service_name, worker_id, job_queue_id, task["id"], task_start_time)
			print("/////////////////////////////////////////////////////")
			print(str(e))
			print("/////////////////////////////////////////////////////")
			raise KeyError()
		finally:
			monitoring.terminate_task(node_id, exp_id, service_name, worker_id, job_queue_id, task["id"], task_start_time)

		myfile.write("output: " + str(output) + "\n")
		return output

def process_array(exp_id, job_queue_id, job):
	tasks = job['tasks']
	try:
		task_command = tasks['command'] 
	except Exception as e:
		tasks['command'] = job['command']
	try:
		task_data = tasks['data'] 
	except Exception as e:
		tasks['data'] = job['data']

	myfile.write("Task: " + str(tasks) + "\n")
	for x in range(0,tasks['count']):
		myfile.write("-------------------------------------\n")
		task_start_time = time.time()
		task_id = tasks["id"] + "_" + str(x)
		monitoring.run_task(node_id, exp_id, service_name, worker_id, job_queue_id, task_id)
		command = ['docker','exec', container_id] + tasks['command'] + [str(tasks["data"])]
		print(worker_id + " - Running Task : " + str(command))
		output = subprocess.check_output(command)
		monitoring.terminate_task(node_id, exp_id, service_name, worker_id, job_queue_id, task_id , task_start_time)
		myfile.write("output: " + str(output) + "\n")
		print(worker_id + " - Output: " + str(output))

@job_app.task(bind=True, base=MyTask)
def add(self, exp_id, job_queue_id, job):
	job_params  = job['params']
	job_command 	= job['command']
	job_start_time = time.time()
	output = ""

	worker_id = self.request.hostname.split("@")[1]
	node_id, service_name, container_id  = worker_id.split("##")

	monitoring.run_job(node_id, exp_id,service_name, worker_id, job_queue_id)

	#log_file =  "./log/" + self.request.hostname + ".log"
	log_file =  "./" + worker_id + ".log"

	with open(log_file, "a") as myfile:
		myfile.write("node_id: " + jqw.node_id + "\n") 
		myfile.write("worker_id: " + worker_id + "\n") 
		myfile.write("New Queue Job: " + job_queue_id + "\n") 
		myfile.write("Command: " + str(job['command']) + "\n")
		myfile.write("Parameters: " + str(len(job_params)) + "\n")

		if (isinstance(job['tasks'], list)):
			print("Tasks : There is a List of " + str(len(job['tasks'])))
			output = process_list()
		else:
			output = process_array()
			print("Tasks : There is an array of " + str(tasks['count']))

		print("......................................................")
		print(worker_id + " has finished the job " + job_queue_id + " - " + exp_id)

		monitoring.terminate_job(node_id, exp_id, service_name, worker_id, job_queue_id, job_start_time)
		return output
