import redis 
JOB_QUEUE_PREFIX 	= 	'jqueue_service_'
broker_protocol		= 	'pyamqp'
broker_username 	= 	'guest'
#broker_username 	= 	'admin'
broker_password 	= 	''
#broker_password 	= 	'mypass'
broker_server		=	'127.0.0.1'
#broker_server		=	'rabbit'

def broker():
	broker 	= 	broker_protocol + '://' + broker_username 
	if (broker_password != ''):
		broker 	= broker + ':' + broker_password
	broker 	= 	broker + '@' + broker_server + '//'
	return broker

backend_protocol 			= 	'redis'
backend_server	 			=	'127.0.0.1'
#backend_server	 			=	'redis'
backend_port     			=	6379
backend_db		 			=	0
backend_experiment_db_id	=	10

backend_experiment_db = redis.StrictRedis(
	host=backend_server, 
	port=backend_port, 
	db=backend_experiment_db_id, 
	charset="utf-8", 
	decode_responses=True
	)
 	
def backend(db):
	backend = backend_protocol + '://' + backend_server + ':' + str(backend_port) + '/' + str(db)
	return backend
