from prometheus_client import Counter, Gauge, Histogram
import time, sys
from datadog import DogStatsd

statsd = DogStatsd(host="stastd", port=9125)

JQUEUING_WORKER_ADDED_COUNT = 'jqueuing_worker_added_count'
JQUEUING_WORKER_COUNT = "jqueuing_worker_count" 

def add_worker(node_id, service_name):
	statsd.increment(JQUEUING_WORKER_ADDED_COUNT,
		tags=[
			'node_id:%s' % node_id,
		]
	)
	statsd.increment(node_id,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
		]
	)

JQUEUING_WORKER_TERMINATED_COUNT = 'jqueuing_worker_terminated_count'
def terminate_worker(node_id, service_name):
	statsd.decrement(node_id,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
		]
	)
JQUEUING_JOB_RUNNING_COUNT = 'jqueuing_job_running_count'
JQUEUING_JOB_ACCOMPLISHED_COUNT = 'jqueuing_job_accomplished_count'
JQUEUING_JOB_ACCOMPLISHED_LATENCY = 'jqueuing_job_accomplished_latency'

def run_job(node_id, service_name, qworker_id, job_id):
	statsd.increment(JQUEUING_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

def terminate_job(node_id, service_name, qworker_id, job_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUING_JOB_ACCOMPLISHED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.increment(JQUEUING_JOB_ACCOMPLISHED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)
	statsd.decrement(JQUEUING_JOB_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
		]
	)

JQUEUING_TASK_RUNNING_COUNT = 'jqueuing_task_running_count'
JQUEUING_TASK_ACCOMPLISHED_COUNT = 'jqueuing_task_accomplished_count'
JQUEUING_TASK_ACCOMPLISHED_LATENCY = 'jqueuing_task_accomplished_latency'

def run_task(node_id, service_name, qworker_id, job_id, task_id):
	statsd.increment(JQUEUING_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)

def terminate_task(node_id, service_name, qworker_id, job_id, task_id, start_time):
	elapsed_time = time.time() - start_time
	statsd.histogram(JQUEUING_TASK_ACCOMPLISHED_LATENCY,
		elapsed_time,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.increment(JQUEUING_TASK_ACCOMPLISHED_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
	statsd.decrement(JQUEUING_TASK_RUNNING_COUNT,
		tags=[
			'node_id:%s' % node_id,
			'service_name:%s' % service_name,
			'qworker_id: %s' % qworker_id,
			'job_id: %s' % job_id,
			'task_id: %s' % task_id,
		]
	)
