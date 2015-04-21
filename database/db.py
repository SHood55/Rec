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
    print "DB connected and cursor created"

def saveApp(app):
    sql = """INSERT INTO `App`(`name`, `permissions`, `similar`, `published`, `logoUrl`, `play_store_url`) VALUES (%s,%s,%s,%s,%s,%s)"""
    if(app):
        connect.cursor.execute(sql, (app.name,json.dumps(app.permissions),json.dumps(app.similar),json.dumps(app.published),app.logo,app.url))
        connect.db.commit()
    else:
        print "element was missing from full App"

    print "saved ", app.name
def getAll():
    connect.cursor.execute("SELECT * FROM App")


# print all the first cell of all the rows
    for row in connect.cursor.fetchall() :
        print row[0]

def getApp(name):
    sql = """SELECT * FROM App WHERE name =%s"""
    connect.cursor.execute(sql,[name])
    row = connect.cursor.fetchone()
    permissions = ast.literal_eval(row[1])
    similar = ast.literal_eval(row[2])
    published = row[3]
    logo= row[4]
    url = row[5]
    app = App(name, url, logo, published, similar, permissions)

    return app

def getJSonApp(name):
    app = getApp(name)
    data = {}
    data["permissions"] = app.permissions
    data["logo"] = app.logo
    data["url"] = app.url
    data["name"] = app.name
    return data
def doesExist(name):
    #returns 1 if found, 0 if not
    connect.cursor.execute("SELECT EXISTS(SELECT 1 FROM App WHERE name = '%s')" % (name))
    result = connect.cursor.fetchone()
    return result[0] == 1



