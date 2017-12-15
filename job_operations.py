from __future__ import absolute_import, unicode_literals
import time, shlex, subprocess, random

from jqueuing_worker import job_app
import jqueuing_worker as jqw
import monitoring

print("Job Operations - Started")

@job_app.task(bind=True)
def add(self, exp_id, job_queue_id, job):
	job_params  = job['params']
	job_command 	= job['command']
	job_start_time = time.time()

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
			for task in job['tasks']:
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
				command = ['docker','exec', container_id] + task_command + [str(task["data"])]
				monitoring.terminate_task(node_id, exp_id, service_name, worker_id, job_queue_id, task["id"], task_start_time)
				output = subprocess.check_output(command)
				myfile.write("output: " + str(output) + "\n")
				print(output)
				time.sleep(random.randrange(10, 100))
		else:
			tasks = job['tasks']
			print("Tasks : There is an array of " + str(tasks['count']))

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
				monitoring.terminate_task(node_id, exp_id, service_name, worker_id, job_queue_id, task_id , task_start_time)
				output = subprocess.check_output(command)
				myfile.write("output: " + str(output) + "\n")
				print(worker_id + " - Output: " + str(output))
				time.sleep(random.randrange(10, 100))
		print("......................................................")
		print(worker_id + " has finished the job " + job_queue_id + " - " + exp_id)
		return output

			
	monitoring.terminate_job(node_id, exp_id, service_name, worker_id, job_queue_id, job_start_time)