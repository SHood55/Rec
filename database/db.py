'''
Created on Mar 18, 2015

@author: Wschive
'''
import MySQLdb
import ast
from data.App import App
from _ast import TryExcept
import json

def connect():
    connect.db = MySQLdb.connect(host="mysql.stud.ntnu.no", # your host, usually localhost
                     user="wilhelmw", # your username
                      passwd="bendik99", # your password
                      db="wilhelmw_thesis") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
    connect.cursor = connect.db.cursor()
    connect.db.set_character_set('utf8')
    connect.cursor.execute('SET NAMES utf8;')
    connect.cursor.execute('SET CHARACTER SET utf8;')
    connect.cursor.execute('SET character_set_connection=utf8;')
    print "DB connected and cursor created"

def saveApp(app):
    sql = """INSERT INTO `App`(`name`, `permissions`, `similar`, `logoUrl`, `infoline`,`packageName`) VALUES (%s,%s,%s,%s,%s,%s)"""
    if(app):
        connect.cursor.execute(sql, (app.name,json.dumps(app.permissions),json.dumps(app.similar),app.logo,app.infoline, app.packageName))
        connect.db.commit()
    else:
        print "element was missing from full App"

    print "saved ", app.packageName
def getAll():
    connect.cursor.execute("SELECT * FROM App")


# print all the first cell of all the rows
    for row in connect.cursor.fetchall() :
        print row[0]

def getApp(packageName):
    sql = """SELECT * FROM App WHERE packageName =%s"""
    connect.cursor.execute(sql,[packageName])
    row = connect.cursor.fetchone()
    realName = row[0]
    permissions = ast.literal_eval(row[1])
    similar = ast.literal_eval(row[2])
    logo= row[3]
    infoline = row[4]
    packageName = row[5]
    app = App(realName, packageName,logo, infoline, similar, permissions, )

    return app

def getJSonApp(packageName):
    app = getApp(packageName)
    data = {}
    data["permissions"] = app.permissions
    data["logo"] = app.logo
    data["infoLine"] = app.infoline
    data["name"] = app.name
    data["packageName"] = app.packageName
    return data

def doesExist(packageName):
    #returns 1 if found, 0 if not
    connect.cursor.execute("SELECT EXISTS(SELECT 1 FROM App WHERE packageName = '%s')" % (packageName))
    result = connect.cursor.fetchone()
    return result[0] == 1



