class Experiment_Service:
    def __init__(self, name):
		self.service_name								= name
		self.jqueuer_worker_added_count					=	0
	
		self.jqueuer_job_added_count					=	0
		self.jqueuer_job_running_count					=	0

		self.jqueuer_task_running_count					=	0
		self.jqueuer_task_accomplished_count			=	0
		self.jqueuer_task_accomplished_latency			=	0
		self.jqueuer_task_accomplished_latency_count	=	0
		self.jqueuer_task_accomplished_latency_sum		=	0

		self.jqueuer_job_accomplished_count				=	0
		self.jqueuer_job_accomplished_latency			=	0
		self.jqueuer_job_accomplished_latency_count		=	0
		self.jqueuer_job_accomplished_latency_sum		=	0

	def update_jqueuer_worker_added_count:

	def update(self, variable, json):
