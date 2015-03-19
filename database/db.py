'''
Created on Mar 18, 2015

@author: Wschive
'''
import MySQLdb


def connect():
    db = MySQLdb.connect(host="mysql.stud.ntnu.no", # your host, usually localhost
                     user="wilhelmw", # your username
                      passwd="bendik99", # your password
                      db="wilhelmw_thesis") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
    connect.cursor = db.cursor()
    print "DB connected and cursor created"

def saveApp(app):
    if(app.name and app.version and app.risks and app.similar):
        connect.cursor.execute("save this shizzle")
        connect.cursor.commit
    else:
        print "element was missing from full App"

def getAll():
    connect.cursor.execute("SELECT * FROM App")


# print all the first cell of all the rows
    for row in connect.cursor.fetchall() :
        print row[0]

def doesExist(name):
    #returns 1 if found, 0 if not
    connect.cursor.execute("SELECT EXISTS(SELECT 1 FROM App WHERE name = '%s')"% (name))
    result = connect.cursor.fetchone()
    return result[0] == 1
