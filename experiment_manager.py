from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, json, time, ast, random
from pprint import pprint
from threading import Thread

import job_manager
import prometheus_getter

from experiment import Experiment 

prometheus_protocol = 'http'
prometheus_ip       = '172.31.1.1'
prometheus_port     = 9090

experiments = {}
def add_experiment(experiment_json):
	output = "experiment_json: " + str(experiment_json)
	private_id = str(int(round(time.time() * 1000))) + "_" + str(random.randrange(100, 999))
	experiment_id = "exp_" + private_id

	experiment = Experiment(experiment_id, private_id, experiment_json)
	experiment_thread = Thread(target = experiment.start, args = ())
	experiment_thread.start()

	experiments[experiment_id] = {'experiment': experiment, 'thread': experiment_thread}
	print(output)
	return str(experiment_id) + " has been added & started successfully ! \n"

def del_experiment(experiment_json):
	customer_service_name = experiment_json['service_name']
	if (backend_experiment_db.exists(customer_service_name)):
		backend_experiment_db.delete(customer_service_name)
		return "Customer Service " + customer_service_name + " has been removed from the queue" + "\n"
	return "Customer Service " + customer_service_name + " wasn't found in the queue" + "\n"

class HTTP(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		data = None
		binary = None
		html_file = open('./index.html','r')
		response = html_file.read()
		html_file.close()
		#print(response)
		binary = bytes(json.dumps(response),"utf-8")

		self._set_headers()
		self.wfile.write(binary)

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
		#pprint(vars(self))
		# Doesn't do anything with posted data
		content_length= None
		data_json = None
		data =None
		try:
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			data = self.rfile.read(int(content_length)).decode('utf-8')
			print('data : ' + str(data))
			data_json = ast.literal_eval(data)
			print(data_json['service_name'])
			pass
		except Exception as e:
			print("Error in parsing the content_length and packet data")
		data_back = ""

		if (self.path == '/experiment/result'):

			
			print('data_json' + str(data))
			html_file = open('./index.html','a')
			html_file.write("<p>" + data + "<p><br>")
			html_file.close()
			data_back = "received"
			print("------------------/experiment/result---------------")
		if (self.path == '/experiment/add'):
			print(str(data_json))
			data_back = add_experiment(data_json)
			print("------------------/experiment/add---------------")
		elif (self.path == '/experiment/del'):
			print(str(data_json))
			data_back = del_experiment(data_json)
			print("------------------/experiment/del---------------")
		
		self._set_headers()
		self.wfile.write(bytes(str(data_back), "utf-8"))


def start_experiment_receiver(port=8081):
	server_address = ('', port)
	httpd = HTTPServer(server_address, HTTP)
	print('Starting Experiment Manager HTTP Server...' + str(port))
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("***** Error in Experiment Manager HTTP Server *****")
		pass

	httpd.server_close()
	print(time.asctime(), "Experiment Manager Server Stopped - %s:%s" % (server_address, port))

if __name__ == '__main__':

	job_manager_thread = Thread(target = job_manager.start_job_manager, args = ())
	job_manager_thread.start()

	prometheus_getter_thread = Thread(target = prometheus_getter.start, 
		args = (prometheus_protocol, prometheus_ip, prometheus_port, experiments,)
		)
	prometheus_getter_thread.start()

	experiment_receiver_thread = Thread(target = start_experiment_receiver, args = ())
	experiment_receiver_thread.start()