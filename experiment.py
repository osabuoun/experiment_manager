import time, math, datetime, random
from parameters import backend_experiment_db, JOB_QUEUE_PREFIX
from celery import subtask
import monitoring, job_operations, time_decoder

class Experiment:
	def __init__(self, experiment_id, private_id, experiment):
		self.log = ""
		self.actual_start_timestamp	= 	self.time_now()
		self.experiment_id 	= experiment_id
		#self.autoscaler = autoscaler
		self.image_url = experiment['image_url']
		try:
			self.service_name 	= self.image_url.replace("/","_").replace(":","_") + "__" + private_id
			#self.add_service(self.service_name)
		except Exception as e:
			self.service_name 	= None
		self.experiment = experiment

	def add_log(self, text):
		self.log += text
		self.log += "\n"

	def time_now(self):
		return datetime.datetime.now().timestamp()

	def add_service(self, service_name):
		if (backend_experiment_db.exists(service_name)):
			return ""
		backend_experiment_db.set(service_name, 
			{'experiment_id':self.experiment_id})
		output = "A new service has just been added " + service_name + "\n"
		self.add_log(output)

	def run_service(self):
		pass

	def update(self, query_var, result):
		if (query_var == 'jqueuer_task_added_count'):
			self.jqueuer_task_added_count = int(result[value][1])
		elif (query_var == 'jqueuer_task_running_count'):
			self.jqueuer_task_running_count = int(result[value][1])
		elif (query_var == 'jqueuer_task_started_count'):
			self.jqueuer_task_started_count = int(result[value][1])
		elif (query_var == 'jqueuer_task_accomplished_count'):
			self.jqueuer_task_accomplished_count = int(result[value][1])
		elif (query_var == 'jqueuer_task_accomplished_latency'):
			self.jqueuer_task_accomplished_latency = int(result[value][1])
		elif (query_var == 'jqueuer_task_accomplished_latency_count'):
			self.jqueuer_task_accomplished_latency_count = int(result[value][1])
		elif (query_var == 'jqueuer_task_accomplished_latency_sum'):
			self.jqueuer_task_accomplished_latency_sum = int(result[value][1])
		elif (query_var == 'jqueuer_job_running_count'):
			self.jqueuer_job_running_count = int(result[value][1])
		elif (query_var == 'jqueuer_job_started_count'):
			self.jqueuer_job_started_count = int(result[value][1])
		elif (query_var == 'jqueuer_job_accomplished_count'):
			self.jqueuer_job_accomplished_count = int(result[value][1])
		elif (query_var == 'jqueuer_job_accomplished_latency'):
			self.jqueuer_job_accomplished_latency = int(result[value][1])
		elif (query_var == 'jqueuer_job_accomplished_latency_count'):
			self.jqueuer_job_accomplished_latency_count = int(result[value][1])
		elif (query_var == 'jqueuer_job_accomplished_latency_sum'):
			self.jqueuer_job_accomplished_latency_sum = int(result[value][1])
		elif (query_var == 'jqueuer_job_failed_count'):
			self.jqueuer_job_failed_count = int(result[value][1])
		elif (query_var == 'jqueuer_job_failed_latency'):
			self.jqueuer_job_failed_latency = int(result[value][1])
		elif (query_var == 'jqueuer_job_failed_latency_count'):
			self.jqueuer_job_failed_latency_count = int(result[value][1])
		elif (query_var == 'jqueuer_job_failed_latency_sum'):
			self.jqueuer_job_failed_latency_sum = int(result[value][1])

		'''
		query_vars = {
			#'jqueuer_worker_count': self.jqueuer_worker_count = int(result[value][1]),
			'jqueuer_task_added_count': self.jqueuer_task_added_count = int(result[value][1]),
			'jqueuer_task_running_count': self.jqueuer_task_running_count = int(result[value][1]),
			'jqueuer_task_started_count': self.jqueuer_task_started_count = int(result[value][1]),
			'jqueuer_task_accomplished_count': self.jqueuer_task_accomplished_count = int(result[value][1]),
			'jqueuer_task_accomplished_latency': self.jqueuer_task_accomplished_latency = int(result[value][1]),
			'jqueuer_task_accomplished_latency_count': self.jqueuer_task_accomplished_latency_count = int(result[value][1]),
			'jqueuer_task_accomplished_latency_sum': self.jqueuer_task_accomplished_latency_sum = int(result[value][1]),
			'jqueuer_job_running_count': self.jqueuer_job_running_count = int(result[value][1]),
			'jqueuer_job_started_count': self.jqueuer_job_started_count = int(result[value][1]),
			'jqueuer_job_accomplished_count': self.jqueuer_job_accomplished_count = int(result[value][1]),
			'jqueuer_job_accomplished_latency': self.jqueuer_job_accomplished_latency = int(result[value][1]),
			'jqueuer_job_accomplished_latency_count': self.jqueuer_job_accomplished_latency_count = int(result[value][1]),
			'jqueuer_job_accomplished_latency_sum': self.jqueuer_job_accomplished_latency_sum = int(result[value][1]),
			'jqueuer_job_failed_count': self.jqueuer_job_failed_count = int(result[value][1]),
			'jqueuer_job_failed_latency': self.jqueuer_job_failed_latency = int(result[value][1]),
			'jqueuer_job_failed_latency_count': self.jqueuer_job_failed_latency_count = int(result[value][1]),
			'jqueuer_job_failed_latency_sum': self.jqueuer_job_failed_latency_sum = int(result[value][1]),
		}
		query_vars[query_var]
		'''

	def init_counters(self):
		self.service_replica_count 					=	0
		self.jqueuer_worker_count 					=	0

		self.jqueuer_task_added_count				= 	0 
		self.jqueuer_task_running_count				=	0
		self.jqueuer_task_started_count				=	0
		self.jqueuer_task_accomplished_count		=	0
		self.jqueuer_task_accomplished_latency		=	0
		self.jqueuer_task_accomplished_latency_count=	0
		self.jqueuer_task_accomplished_latency_sum	=	0

		self.jqueuer_job_added_count				=	0
		self.jqueuer_job_running_count				=	0
		self.jqueuer_job_started_count				=	0
		self.jqueuer_job_accomplished_count			=	0
		self.jqueuer_job_accomplished_latency		=	0
		self.jqueuer_job_accomplished_latency_count	=	0
		self.jqueuer_job_accomplished_latency_sum	=	0

		self.task_per_job_avg						=	0

		self.jqueuer_job_failed_count				=	0
		self.jqueuer_job_failed_latency				=	0
		self.jqueuer_job_failed_latency_count		=	0
		self.jqueuer_job_failed_latency_sum			=	0

	def process_jobs(self):
		output = ""
		if (isinstance(self.experiment['jobs'], list)):
			output = self.process_job_list()
		else:
			output = self.process_job_array()
		self.add_log(output)

	def get_task_count(self, tasks):
		count = 0
		try:
			if (isinstance(tasks, list)):
				count = len(tasks)
			else:
				count = tasks['count']
		except Exception as e:
			count = 0
		return count 

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
				job['command'] = experiment['command']

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
			output = self.add_job(jobs)
			self.add_log(output)

	def add_job(self, job):
		print('self.service_name:' + self.service_name)
		job_queue_id = "j_" + self.service_name +"_" + str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
		self.add_log("job_queue_id:" + job_queue_id + " - JOB_QUEUE_PREFIX:" + JOB_QUEUE_PREFIX)

		chain = subtask('job_operations.add', queue = JOB_QUEUE_PREFIX + self.service_name)
		chain.delay(self.experiment_id, job_queue_id, job)
		self.jqueuer_job_added_count += 1 
		monitoring.add_job(self.experiment_id, self.service_name, job_queue_id)
		self.add_log("The job " + str(job['id']) + " has just been added")

		task_count = self.get_task_count(job['tasks'])
		monitoring.add_task(self.experiment_id, self.service_name, job_queue_id, task_count)
		self.jqueuer_task_added_count += task_count
		self.task_per_job_avg = math.ceil(self.jqueuer_task_added_count / jqueuer_job_added_count)
		self.add_log("The job " + str(job['id']) + " has " + str(task_count) + " tasks, they have just been added")

	def update_params(self):
		self.deadline				=	time_decoder.get_seconds(experiment['experiment_deadline'])
		self.deadline_timestamp		= 	self.actual_start_timestamp + self.customer_deadline

		#self.single_job_duration	=	time_decoder.get_seconds(experiment['single_job_duration'])
		#self.all_job_duration		=	self.single_job_duration * self.jqueuer_job_added_count
		self.replica_min = int(experiment['replica_min'])
		self.replica_max = int(experiment['replica_max'])

		self.single_task_duration	=	time_decoder.get_seconds(experiment['single_task_duration'])
		'''
		self.all_job_duration		=	self.single_task_duration * self.jqueuer_task_added_count
		self.estimated_deadline				=	self.single_task_duration * self.jqueuer_task_added_count
		self.estimated_deadline_timestamp	=	self.actual_start_timestamp + self.estimated_deadline
		'''


	def calc_replica_count(self):
		jobs_running_count = self.jqueuer_job_started_count - self.jqueuer_job_accomplished_count
		jobs_queued = self.jqueuer_job_added_count - jobs_running_count
		time_needed = 0
		if (self.service_replica_count > 0):
			time_needed = jobs_queued * (self.single_task_duration * self.task_per_job_avg) / self.service_replica_count
		else :
			time_needed = jobs_queued * (self.single_task_duration * self.task_per_job_avg) 

		time_remaining	=	self.time_now() - self.deadline_timestamp
		replica_needed	= 	jobs_queued * (self.single_task_duration * self.task_per_job_avg) / time_remaining

		if (replica_needed > self.service_replica_count):
			if (replica_needed > self.replica_max):
				replica_needed = self.replica_max
		else:
			if (replica_needed < self.replica_min):
				replica_needed = self.replica_min
		return replica_needed


	def start(self):
		self.init_counters()
		self.process_jobs()
		self.update_params()
		self.calc_replica_count()
		self.run_service()
		while self.jqueuer_job_accomplished_count < self.jqueuer_job_added_count:
			replica_needed = self.calc_replica_count()
			if (replica_needed != self.service_replica_count):
				#self.autoscaler.scale(replica_needed)
				print("I should scale now")
			time.sleep(15)
