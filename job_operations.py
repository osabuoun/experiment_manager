from __future__ import absolute_import, unicode_literals
import time, shlex, subprocess, random

from jqueuing_worker import job_app
import jqueuing_worker as jqw
import monitoring

print("Job Operations - Started")

@job_app.task(bind=True)
def add(self, job_id, job):
	job_params  = job['params']
	job_command 	= job['command']
	job_start_time = time.time()

	worker_id = self.request.hostname.split("@")[1]
	node_id, service_name, container_id  = worker_id.split("##")

	monitoring.run_job(node_id, service_name, worker_id, job_id)

	log_file =  "./log/" + self.request.hostname + ".log"

	with open(log_file, "a") as myfile:
		myfile.write("node_id: " + jqw.node_id + "\n") 
		myfile.write("worker_id: " + worker_id + "\n") 
		myfile.write("New Job: " + job_id + "\n") 
		myfile.write("Command: " + str(job['command']) + "\n")
		myfile.write("Parameters: " + str(len(job_params)) + "\n")
		for task_params in job_params:
			myfile.write("Parameters: " + str(task_params) + "\n")
		myfile.write("-------------------------------------\n")
		time.sleep(random.randrange(10, 100))
		for task_params in job_params:
			task_start_time = time.time()
			task_id = task_params["id"]
			task_data = task_params["data"]
			monitoring.run_task(node_id, service_name, worker_id, job_id, task_id)
			command = ['docker','exec', container_id] + task_command + task_data
			monitoring.terminate_task(node_id, service_name, worker_id, job_id, task_id, task_start_time)
			output = subprocess.check_output(command)
			myfile.write("output: " + str(output) + "\n")
			print(output)
	monitoring.terminate_job(node_id, service_name, worker_id, job_id, job_start_time)