from prometheus_client import Counter, Gauge, Histogram
import time, sys
from parameters import statsd

#JQUEUER_WORKER_ADDED_COUNT = 'jqueuer_worker_added_count'
JQUEUER_WORKER_COUNT = "jqueuer_worker_count" 

def add_worker(node_id, service_name):
	statsd.increment(JQUEUER_WORKER_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
		]
	)

#JQUEUER_WORKER_TERMINATED_COUNT = 'jqueuer_worker_terminated_count'
def terminate_worker(node_id, service_name):
	statsd.decrement(JQUEUER_WORKER_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
		]
	)
JQUEUER_JOB_ADDED_COUNT = 'jqueuer_job_added_count'
JQUEUER_JOB_RUNNING_COUNT = 'jqueuer_job_running_count'
JQUEUER_JOB_STARTED_COUNT = 'jqueuer_job_started_count'
JQUEUER_JOB_ACCOMPLISHED_COUNT = 'jqueuer_job_accomplished_count'
JQUEUER_JOB_ACCOMPLISHED_LATENCY = 'jqueuer_job_accomplished_latency'
JQUEUER_JOB_FAILED_COUNT = 'jqueuer_job_failed_count'
JQUEUER_JOB_FAILED_LATENCY = 'jqueuer_job_failed_latency'

def add_job(experiment_id ,service_name, job_id):
	statsd.increment(JQUEUER_JOB_ADDED_COUNT,
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'job_id: %s' % job_id,
		]
	)

def run_job(node_id, experiment_id ,service_name, qworker_id, job_id):
	statsd.increment(JQUEUER_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.increment(JQUEUER_JOB_STARTED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

def terminate_job(node_id, experiment_id ,service_name, qworker_id, job_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUER_JOB_ACCOMPLISHED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.increment(JQUEUER_JOB_ACCOMPLISHED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.decrement(JQUEUER_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

def job_failed(node_id, experiment_id ,service_name, qworker_id, job_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUER_JOB_FAILED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.increment(JQUEUER_JOB_FAILED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.decrement(JQUEUER_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

JQUEUER_TASK_ADDED_COUNT = 'jqueuer_task_added_count'
JQUEUER_TASK_RUNNING_COUNT = 'jqueuer_task_running_count'
JQUEUER_TASK_STARTED_COUNT = 'jqueuer_task_started_count'
JQUEUER_TASK_ACCOMPLISHED_COUNT = 'jqueuer_task_accomplished_count'
JQUEUER_TASK_ACCOMPLISHED_LATENCY = 'jqueuer_task_accomplished_latency'
JQUEUER_TASK_FAILED_COUNT = 'jqueuer_task_failed_count'
JQUEUER_TASK_FAILED_LATENCY = 'jqueuer_task_failed_latency'

def add_task(experiment_id ,service_name, job_id, task_count = 1):
	statsd.increment(JQUEUER_TASK_ADDED_COUNT,
		tags=[
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'job_id: %s' % job_id,
		],
		value=task_count
	)

def run_task(node_id, experiment_id ,service_name, qworker_id, job_id, task_id):
	statsd.increment(JQUEUER_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.increment(JQUEUER_TASK_STARTED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
def terminate_task(node_id, experiment_id ,service_name, qworker_id, job_id, task_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUER_TASK_ACCOMPLISHED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.increment(JQUEUER_TASK_ACCOMPLISHED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.decrement(JQUEUER_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)

def task_failed(node_id, experiment_id ,service_name, qworker_id, job_id, task_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUER_TASK_FAILED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.increment(JQUEUER_TASK_FAILED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.decrement(JQUEUER_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'experiment_id:%s' % experiment_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
