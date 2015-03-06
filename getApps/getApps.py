#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
from pprint import pprint

from googleplay import GooglePlayAPI
from helpers import sizeof_fmt
import config


def run(packagename):


#         print "Usage: %s packagename [filename]"
#         print "Download an app."
#         print "If filename is not present, will write to packagename.apk."




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
