'''
Created on Mar 4, 2015

@author: Wschive
'''
import BaseHTTPServer, SimpleHTTPServer, ssl, requests
import json
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse
from data.App import App
from database import db
from getApps import getApps
from risk import risk


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
            rawResult = replaceRequest(hi.query)#list of appnames
            self.wfile.write(createReplaceResponse(rawResult))
           #findReplacement(hi.query)#find similar apps, then send list rated by most secure

    def do_POST(self):
        self.send_error(502, "not implemented")

def createReplaceResponse(raw):
    list = []
    for app in raw:
        list.append(db.getJSonApp(app.name))
    return json.dumps(list)

def replaceRequest(name):
    app = getOrDL(name)
    resultList = []
    if(app.similar):
        for similar in app.similar:
            temp = getOrDL(similar)
            if(temp is not None):
                resultList.append(temp)
        app.similar = sorted(resultList, key=getValue)#sorted list of similar apps
    else:
        print "similar apps list does not exist"
        return ["no similar apps"]


    return app.similar#list of suggested apps

def getOrDL(name):
    app =db.getApp(name)
#     try:
#         app = db.getApp(name)#add if published is old, redownload
#     except:
#         app = downloadApp(name)
#         if(app is not None):
#             db.saveApp(app)
    return app

def getValue(app):
    return app.analysis["Value"]


def downloadApp(name):
    appInfo = getAppInfo(name)
    if(appInfo["price"] == "free"):
        getApps.run(name)
        analysis = risk.run(name)
        extraInfo = appInfo["additionalInfo"]
        published = extraInfo[0]
        similar = appInfo["recommendedApps"]#is a list
        url  = appInfo["playStoreUrl"]
        logo = appInfo["logo"]
        app = App(name, url, logo, published, similar, analysis)
        return app
    print "app " + name + " is not free, will not be downloaded"
    return None


# returns json with all the info
def getAppInfo(name):
    file= open("data/apkinfo.txt")
    data = json.load(file)
    print "getAppInfo"
    return data
#    works, but limited amount of calls
#     apiKey = {"key" :"9494f057c1a1a67ab30e5e7afdc6afe2"}
#     r = requests.get("http://api.playstoreapi.com/v1.1/apps/"+name, params = apiKey)
#     data = json.loads(r.content)
#     return data
#     print data["recommendedApps"]


#     def do_OPTIONS(self):