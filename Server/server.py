'''
Created on Mar 4, 2015

@author: Wschive
'''
import BaseHTTPServer, SimpleHTTPServer, ssl, requests
import json
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse

def getIP():
    print "getting ip"
    r = requests.get("http://jsonip.com")
    tempJson = r.json()
    ip = tempJson["ip"]
    return ip.encode("utf-8")

def run(server_class=BaseHTTPServer.HTTPServer):



    ip = getIP()
    port = 8888
    handler = MyHandler
    server_address = (ip, port)
    httpd = server_class(server_address, handler)
    print "starting server at", str(ip)+":"+str(port)
    httpd.serve_forever()

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type',    'text/html')
        self.end_headers()
        print self.path
        print "hi"
        hi = urlparse(self.path)
        if(hi.path == "/replace"):
            print "replace app called"
            main.replaceRequest(hi.query)
           #findReplacement(hi.query)#find similar apps, then send list rated by most secure
        self.wfile.write(hi.query)

    def do_POST(self):
        self.send_error(502, "not implemented")



#     def do_OPTIONS(self):