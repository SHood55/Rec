
from androguard.core.bytecodes import apk
from androguard.core import androconf
from androguard.core.analysis import risk
from androguard.core.bytecodes.apk import APK

def display_result(res) :

    for i in res :
        print "\t", i
        for j in res[i] :
            print "\t\t", j, res[i][j]

def analyze_app(filename, ri, a) :
    print filename
    return ri.with_apk(a)


def run(name,dir = ""):

    ri = risk.RiskIndicator()
    ri.add_risk_analysis( risk.RedFlags() )
    ri.add_risk_analysis( risk.FuzzyRisk() )
    ret_type = androconf.is_android(dir + name + ".apk")
    if ret_type == "APK" :
        a = apk.APK(dir + name + ".apk")
        return analyze_app( name, ri, a )
    else:
        print "ret_type was not APK"

def permissions(name, dir=""):
    
    a = APK(dir+name+".apk")
    
    #TODO: append list with score from watchdog
    
    return a.permissions
    


