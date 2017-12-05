from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, json, time, ast, random
from pprint import pprint

import experiment_operations

class HTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        #pprint(vars(self))
        # Doesn't do anything with posted data
        content_length= None
        data_json = None
        try:
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            data = self.rfile.read(int(content_length)).decode('utf-8')
            data_json = ast.literal_eval(data)
            print(data_json['service_name'])
            pass
        except Exception as e:
            print("Error in parsing the content_length and packet data")
        data_back = ""

        if (self.path == '/experiment/add'):
            print(str(data_json))
            data_back = experiment_operations.add_experiment(data_json)
            print("------------------/experiment/add---------------")
        elif (self.path == '/experiment/del'):
            print(str(data_json))
            data_back = experiment_operations.del_experiment(data_json)
            print("------------------/experiment/del---------------")
        
        self._set_headers()
        self.wfile.write(bytes(str(data_back), "utf-8"))


def start(port=8777):
    server_address = ('', port)
    httpd = HTTPServer(server_address, HTTP)
    print('Starting httpd...' + str(port))
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("*************************************")
        pass

    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (server_address, port))

if __name__ == '__main__':
    start()