#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
from pprint import pprint
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt
import config


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
    
def getPermissions(packageName, multiple = False):

    api = GooglePlayAPI(config.ANDROID_ID)
    api.login(config.GOOGLE_LOGIN, config.GOOGLE_PASSWORD, AUTH_TOKEN)

    # Only one app
    if (not multiple):
        response = api.details(packageName)
        result =  []
        print "\n".join(i.encode('utf8') for i in response.docV2.details.appDetails.permission)
        values = response.docV2.details.appDetails.permission._values
        result = [x.encode('utf-8') for x in values]

        return result

    else: # More than one app
        response = api.bulkDetails(packageName)
        result = {}
        for entry in response.entry:
            if (not not entry.ListFields()): # if the entry is not empty
                result[entry.doc.docid] = entry.doc.details.appDetails.permission
        return result
