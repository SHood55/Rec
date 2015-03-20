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
        app = downloadApp(name)
        db.saveApp(app)


    return #list of suggested apps



def downloadApp(name):
    appInfo = getAppInfo(name)
    app = App(name)
    if(appInfo["price"] == "free"):
        getApps.run(name)
        app.analysis = risk.run(name)
        extraInfo = appInfo["additionalInfo"]
        app.published = extraInfo["datePublished"]
        app.similar = appInfo["recommendedApps"]
        app.url  = appInfo["playStoreUrl"]
        app.logo = appInfo["logo"]
        return app


# returns json with all the info
def getAppInfo(name):
    file= open("../data/apkinfo")
    data = json.loads(file)
    return data
#    works, but limited amount of calls
#     apiKey = {"key" :"9494f057c1a1a67ab30e5e7afdc6afe2"}
#     r = requests.get("http://api.playstoreapi.com/v1.1/apps/"+name, params = apiKey)
#     data = json.loads(r.content)
#     return data
#     print data["recommendedApps"]

if __name__ == "__main__" :
    main()