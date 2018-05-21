import time, math, datetime, random
from parameters import JOB_QUEUE_PREFIX
from celery import subtask
import monitoring, job_operations

class Experiment:
	def __init__(self, experiment_id, private_id, experiment):
		self.log = ""
		self.experiment_actual_start_timestamp	= 	self.time_now()

		self.experiment_id 	= experiment_id
		print("**********************************")
		print(str(experiment_id))
		print(str(private_id))
		print(str(experiment))
		print("**********************************")
		self.image_url = experiment['image_url']
		try:
			self.service_name 	= self.image_url.replace("/","_").replace(":","_").replace(".","_").replace("-","_") + "__" + private_id
			self.add_service(self.service_name)
		except Exception as e:
			self.service_name 	= None
		self.experiment = experiment
		monitoring.experiment_actual_start_timestamp(self.experiment_id, self.service_name, self.experiment_actual_start_timestamp)

	def add_log(self, text):
		if (text):
			self.log += text
			self.log += "\n"

	def time_now(self):
		return datetime.datetime.now().timestamp()

	def add_tasks(self, tasks, job_id):
		for task in tasks:
			self.jqueuer_task_added_count += 1
			monitoring.add_task(self.experiment_id, self.service_name, job_id, task['id'])
			self.add_log("The task {} of job {} has been added to monitoring".
				format(str(task['id']), str(job_id)) )

	def add_job(self, job, job_id = None):
		if (not job_id):
			job_id = job["id"]

		self.add_tasks(job['tasks'], job_id)

		self.jqueuer_job_added_count += 1 
		monitoring.add_job(self.experiment_id, self.service_name, job_id)

		job_queue_id = "j_" + self.service_name +"_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))

		chain = subtask('job_operations.add', queue = JOB_QUEUE_PREFIX + self.service_name)
		chain.delay(self.experiment_id, job_queue_id, job)

		self.add_log("The job_id {} ,job_queue_id: {} - ,JOB_QUEUE_PREFIX: {}has just been added".
			format(str(job_id), str(job_queue_id), str(JOB_QUEUE_PREFIX)))

	def process_job_list(self):
		self.add_log("There is a list of " + str(len(self.experiment['jobs'])))
		for job in self.experiment['jobs']:
			try:
				job_params = job['params'] 
			except Exception as e:
				job['params'] = self.experiment['params'] 
			try:
				job_command = job['command'] 
			except Exception as e:
				job['command'] = self.experiment['command']

			output = self.add_job(job)
			self.add_log(output)

	def process_job_array(self):
		jobs = self.experiment['jobs']
		print("There is an array of " + str(jobs['count']))
		try:
			job_params = jobs['params'] 
		except Exception as e:
			jobs['params'] = self.experiment['params'] 
		try:
			job_command = jobs['command'] 
		except Exception as e:
			jobs['command'] = self.experiment['command']

		for x in range(0,jobs['count']):
			job_id = jobs['id'] + "_" + str(x)
			output = self.add_job(jobs, job_id)
			self.add_log(output)

	def process_jobs(self):
		output = ""
		if (isinstance(self.experiment['jobs'], list)):
			output = self.process_job_list()
		else:
			output = self.process_job_array()
		self.task_per_job_avg = math.ceil(self.jqueuer_task_added_count / self.jqueuer_job_added_count)
		self.add_log(output)

	def start(self):
		self.process_jobs()
