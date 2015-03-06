
from androguard.core.bytecodes import apk
from androguard.core.analysis import auto
from scikits.crab import datasets
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import pearson_correlation
from scikits.crab.similarities import UserSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender
import sys, os
from androguard.core.bytecodes.dvm import *
from androguard.core.bytecode import *
from androguard.core.bytecodes.jvm import *
from androguard.core.analysis.analysis import *
from androguard.core.analysis.ganalysis import *
from androguard.decompiler.decompiler import *
import traceback

from optparse import OptionParser

from androguard.core import androconf
from androguard.core.analysis import risk
from androguard.core import analysis


def display_result(res) :

    for i in res :
        print "\t", i
        for j in res[i] :
            print "\t\t", j, res[i][j]

def analyze_app(filename, ri, a) :
    print filename
    risk = ri.with_apk(a)
    updated = False
    try:
        with open('data/data.json') as file:
            print "opening json"
            list = json.load(file)
    except:
        print traceback.print_exc()
        list = [{'Name': filename, 'Value': risk["FuzzyRisk"]["VALUE"], "RedFlags":risk["RedFlags"]}]

    newList = [{'Name': filename, 'Value': risk["FuzzyRisk"]["VALUE"], "RedFlags":risk["RedFlags"]}]
    if list:
        for var in list :
            if(var['Name'] == newList[0]['Name']) and not updated:
                print "json updated or similar found"
                var.update(newList[0])
                updated = True
                break
    else:
        list = newList

    if not updated:
        print "extending list"
        list.extend(newList)

    with open('data/data.json', 'w') as outfile:
        print "dumping json"
        json.dump(list, outfile)


#     display_result( ri.with_apk( a ) )

def analyze_dex(filename, ri, d) :
    print filename
    display_result( ri.with_dex( d ) )

def AnalyzeDex(filename, raw=False, decompiler=None):
    """
        Analyze an android dex file and setup all stuff for a more quickly analysis !

        :param filename: the filename of the android dex file or a buffer which represents the dex file
        :type filename: string
        :param raw: True is you would like to use a buffer (optional)
        :type raw: boolean

        :rtype: return the :class:`DalvikVMFormat`, and :class:`VMAnalysis` objects
    """
    androconf.debug("DalvikVMFormat ...")

    d = None
    if raw == False:
        d = DalvikVMFormat(open(filename, "rb").read())
    else:
        d = DalvikVMFormat(filename)

    androconf.debug("Export VM to python namespace")
    d.create_python_export()

    androconf.debug("VMAnalysis ...")
    dx = uVMAnalysis(d)

    androconf.debug("GVMAnalysis ...")
    gx = GVMAnalysis(dx, None)

    d.set_vmanalysis(dx)
    d.set_gvmanalysis(gx)

    RunDecompiler(d, dx, decompiler)

    androconf.debug("XREF ...")
    d.create_xref()
    androconf.debug("DREF ...")
    d.create_dref()

    return d, dx

def RunDecompiler(d, dx, decompiler):
    """
        Run the decompiler on a specific analysis

        :param d: the DalvikVMFormat object
        :type d: :class:`DalvikVMFormat` object
        :param dx: the analysis of the format
        :type dx: :class:`VMAnalysis` object
        :param decompiler: the type of decompiler to use ("dad", "dex2jad", "ded")
        :type decompiler: string
    """
    if decompiler != None:
      androconf.debug("Decompiler ...")
      decompiler = decompiler.lower()
      if decompiler == "dex2jad":
        d.set_decompiler(DecompilerDex2Jad(d,
                                           androconf.CONF["PATH_DEX2JAR"],
                                           androconf.CONF["BIN_DEX2JAR"],
                                           androconf.CONF["PATH_JAD"],
                                           androconf.CONF["BIN_JAD"],
                                           androconf.CONF["TMP_DIRECTORY"]))
      elif decompiler == "dex2fernflower":
        d.set_decompiler(DecompilerDex2Fernflower(d,
                                                  androconf.CONF["PATH_DEX2JAR"],
                                                  androconf.CONF["BIN_DEX2JAR"],
                                                  androconf.CONF["PATH_FERNFLOWER"],
                                                  androconf.CONF["BIN_FERNFLOWER"],
                                                  androconf.CONF["OPTIONS_FERNFLOWER"],
                                                  androconf.CONF["TMP_DIRECTORY"]))
      elif decompiler == "ded":
        d.set_decompiler(DecompilerDed(d,
                                       androconf.CONF["PATH_DED"],
                                       androconf.CONF["BIN_DED"],
                                       androconf.CONF["TMP_DIRECTORY"]))
      else:
        d.set_decompiler(DecompilerDAD(d, dx))



def run(name,dir = ""):

    ri = risk.RiskIndicator()
    ri.add_risk_analysis( risk.RedFlags() )
    ri.add_risk_analysis( risk.FuzzyRisk() )
    ret_type = androconf.is_android(dir + name + ".apk")
    if ret_type == "APK" :
        a = apk.APK(dir + name + ".apk")
        analyze_app( name, ri, a )
    elif ret_type == "DEX" :
        analyze_dex( name, ri, open(name, "r").read() )


#     for root, dirs, files in os.walk( dir, followlinks=True ) :
#         if files != [] :
#             for f in files :
#                 real_filename = root
#                 if real_filename[-1] != "/" :
#                     real_filename += "/"
#                 real_filename += f
#
#                 ret_type = androconf.is_android( real_filename )
#                 if ret_type == "APK"  :
#                     try :
#                         a = apk.APK( real_filename )
#                         analyze_app( real_filename, ri, a )
#                     except Exception, e :
#                         print e
#
#                 elif ret_type == "DEX" :
#                     analyze_dex( real_filename, ri, open(real_filename, "r").read() )
#             a = apk.APK("/Users/Wschive/Documents/Java/Recommender/Server/src/" + name + ".apk")
#             que = a.get_libraries()
#             b = a.get_permissions()
#             buff = a.get_android_manifest_xml().toprettyxml(encoding="utf-8")
#
#
#
#              root = ET.fromstring(buff)
#             for child in root:
#                  for test in child:
#                      print "tag = " + test.tag + " + ", test.attrib
#                  print "tag = " + child.tag, child.attrib
#
#
#              for lib in root.findall("str: uses-library"):
#                  print lib.attrib
#
#             fd = codecs.open("/Users/Wschive/Documents/LiClipse Workspace/RecServer/" + name + ".xml", "w", "utf-8")
#             fd.write( buff )
#             fd.close()



