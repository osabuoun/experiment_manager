from prometheus_client import Counter, Gauge, Histogram
import time, sys
from parameters import statsd


JQUEUER_JOB_ADDED 			= 'jqueuer_job_added'
JQUEUER_JOB_ADDED_TIMESTAMP = 'jqueuer_job_added_timestamp'
def add_job(experiment_id ,service_name, job_id):
	statsd.gauge(JQUEUER_JOB_ADDED_TIMESTAMP,
		time.time(),
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'job_id: %s' % job_id,
		]
	)
	statsd.gauge(JQUEUER_JOB_ADDED,
		time.time(),
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'job_id: %s' % job_id,
		]
	)

JQUEUER_TASK_ADDED 			= 'jqueuer_task_added'
JQUEUER_JOB_ADDED_TIMESTAMP = 'jqueuer_task_added_timestamp'
def add_task(experiment_id ,service_name, job_id, task_id):
	statsd.gauge(JQUEUER_JOB_ADDED_TIMESTAMP,
		time.time(),
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.gauge(JQUEUER_TASK_ADDED,
		time.time(),
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)

JQUEUER_EXPERIMENT_ACTUAL_START_TIMESTAMP = 'jqueuer_experiment_actual_start_timestamp'
def experiment_actual_start_timestamp(experiment_id ,service_name, experiment_actual_start_timestamp):
	statsd.gauge(JQUEUER_EXPERIMENT_ACTUAL_START_TIMESTAMP,
		experiment_actual_start_timestamp,
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
		]
	)
