from risk import risk
from recommend import recommender
from getApps import getApps
from server import server
from database import db
import socket
import sys
from thread import *
import traceback
import json
import requests
import select
import BaseHTTPServer, SimpleHTTPServer, ssl
from data import App


def main() :

#    name = "com.hdezninirola.frequency"
    name = "no.nrk.yr"
#     name = "com.rovio.angrybirds"
#     dir = "/Users/Wschive/Desktop/"
#     name = "com.kabam.underworldandroid"
#     getApps.run("com.bitdefender.clueful")
#     risk.run("com.bitdefender.clueful")
#     recommender.recommend()

#     s = requests.Session()
# #     s.auth=('wilhelmws@gmail.com', '1.9.Alpha')
#     s.post("https://accounts.google.com/ServiceLogin", {"Email":'wilhelmws@gmail.com', "Passwd":'1.9.Alpha'})
#     print s
#     value = {"id":"com.squareenix.smoothieswipe"}
# #     r = s.get("https://play.google.com/store/apps/details", params = value)
# #     print r
#
#     g = s.get("http://play.google.com/store/apps/similar", params = value)
#     print g
#     print(g.url)
#     print g.content

#     works, but limited amount of calls
#     apiKey = {"key" :"9494f057c1a1a67ab30e5e7afdc6afe2"}
#     r = requests.get("http://api.playstoreapi.com/v1.1/apps/"+name, params = apiKey)
#     data = json.loads(r.content)
#     print data
#     print data["recommendedApps"]
    db.connect()
    server.run()
    print "it ran!"

def replaceRequest(name):
    if(db.doesExist(name)):
        app = db.getApp(name)
    else:
        downloadApp(name)

def downloadApp(name):
    app = App(name)
    getApps.run(name)
    app.analysis = risk.run(name)
#    app.version = on hold. needed? write about this. how to get?
    app.similar =
def getAppInfo(name):
#   works, but limited amount of calls
#     apiKey = {"key" :"9494f057c1a1a67ab30e5e7afdc6afe2"}
#     r = requests.get("http://api.playstoreapi.com/v1.1/apps/"+name, params = apiKey)
#     data = json.loads(r.content)
#     print data
#     print data["recommendedApps"]

if __name__ == "__main__" :
    main()