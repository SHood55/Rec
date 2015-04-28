#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
from pprint import pprint
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt
import config
from bs4 import BeautifulSoup
import requests


def run(packagename):

    if (len(sys.argv) == 3):
        filename = sys.argv[2]
    else:
        filename = packagename + ".apk"

# Connect
    api = GooglePlayAPI(config.ANDROID_ID)

    api.login(config.GOOGLE_LOGIN, config.GOOGLE_PASSWORD, AUTH_TOKEN)

# Get the version code and the offer type from the app details
    m = api.details(packagename)
    doc = m.docV2
    vc = doc.details.appDetails.versionCode
    ot = doc.offer[0].offerType

# Download
    print "Downloading %s..." % sizeof_fmt(doc.details.appDetails.installationSize),
    data = api.download(packagename, vc, ot)
    open(filename, "wb").write(data)
    print "Done"

def getSimilar(packageName):

    s = requests.Session()
    s.post("https://accounts.google.com/ServiceLogin", {"Email":'wilhelmws@gmail.com', "Passwd":'1.9.Alpha'})
    print s
    value = {"id":"no.nrk.yr"}
# r = s.get("https://play.google.com/store/apps/details", params = value)
# print r
    g = s.get("http://play.google.com/store/apps/similar", params = value)
    print g
    soup = BeautifulSoup( g.content)
    print soup.title
    apps = soup.find_all("a", class_ = "title")
    logos = soup.find_all("img", class_ = "cover-image")

    result = {}
    for link, logo in zip(apps, logos):
        print(link.get("href"))
        line = link.get("href")
        image = logo.get("data-cover-small")
        result[(line.split("=",1)[1])] = image
        return result

def getPermissions(packageName, multiple = False):

    api = GooglePlayAPI(config.ANDROID_ID)
    api.login(config.GOOGLE_LOGIN, config.GOOGLE_PASSWORD, AUTH_TOKEN)
    result = {}
    # Only one app
    if (not multiple):
        response = api.details(packageName)
        permissions =  []
        values = response.docV2.details.appDetails.permission._values
        permissions = [x.encode('utf-8') for x in values]
        name = response.docV2.title
        name = name.encode("utf8")
        result[name] = permissions
        return result

    else: # More than one app
        response = api.bulkDetails(packageName)
        for entry in response.entry:
            if (not not entry.ListFields()): # if the entry is not empty
                result[entry.doc.docid] = entry.doc.details.appDetails.permission
        return result
