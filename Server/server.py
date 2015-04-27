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
import io
import os.path




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
        list.append(db.getJSonApp(app.packageName))
    return json.dumps(list)

def replaceRequest(packageName):
    app = getOrDL(packageName)
    resultList = []
    if(app.similar):
        for similar in app.similar:
            temp = getOrDL(similar)
            if(temp is not None):
                resultList.append(temp)
#         app.similar = sorted(resultList, key=getValue)#sorted list of similar apps
        app.similar = resultList
    else:
        print "similar apps list does not exist"
        return ["no similar apps"]


    return app.similar#list of suggested apps

def getOrDL(packageName):
#     app =db.getApp(name)
    print "getOrDL", packageName
    try:
        app = db.getApp(packageName)#add if published is old, redownload
    except:
        app = downloadApp(packageName)
        if(app is not None):
            db.saveApp(app)
            try:
                db.saveApp(app)
            except:
                print "app exists in db", app.packageName
    return app

def getValue(app):
    fuzzy = app.analysis["FuzzyRisk"]
    return fuzzy["VALUE"]


def downloadApp(packageName):
    print "downloadApp", packageName
    appInfo = getAppInfo(packageName)
    if(appInfo["price"] == "free"):
        try:
            permissions = risk.permissions(packageName)
#             analysis = risk.run(name)
        except:
            getApps.run(packageName)
            permissions = risk.permissions(packageName)
#             analysis = risk.run(name)
        s = appInfo["description"]
        infoline = s.split(".",1)[0]
        similar = appInfo["recommendedApps"]#is a list
        logo = appInfo["logo"]
        appname = appInfo["appName"]
        app = App(appname, packageName, logo, infoline, similar, permissions)
        return app
    print "app " + packageName + " is not free, will not be downloaded"
    return None


# returns json with all the info
def getAppInfo(packageName):

    if(os.path.isfile("data/"+packageName+".json") ):
        file= open("data/"+packageName+".json")
        data = json.load(file)
        return data

#    works, but limited amount of calls
    print "getting Appinfo for ", packageName
    apiKey = {"key" :"9494f057c1a1a67ab30e5e7afdc6afe2"}
    r = requests.get("http://api.playstoreapi.com/v1.1/apps/"+packageName, params = apiKey)
    data = json.loads(r.content)
    with open("data/" + packageName + ".json", 'w') as f:
       f.write(json.dumps(data))
    return data
#     print data["recommendedApps"]


#     def do_OPTIONS(self):