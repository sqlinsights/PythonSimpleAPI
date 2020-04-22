import flask
import yaml
import pyodbc
import json
from flask import render_template

with open('AppSetting.yml') as config:
    configurations = yaml.load(config)

server = configurations['connectionStrings']['server']
database = configurations['connectionStrings']['database']
username = configurations['connectionStrings']['userid']
password = configurations['connectionStrings']['password']


def getPerson(BusinessEntityID):
    conn = pyodbc.connect(
        "DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={0}; database={1}; trusted_connection=no;UID={2};PWD={3}"
        .format(server, database, username, password))
    cursor = conn.cursor()
    cursor.execute(
        'SELECT  BusinessEntityID, FirstName, LastName from Person.Person where BusinessEntityID = {0}'
        .format(BusinessEntityID)
    )
    columns = [column[0] for column in cursor.description]
    results = []
    #rows = cursor.fetchall()
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return {'results':results}

def getPersons():
    conn = pyodbc.connect(
        "DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={0}; database={1}; trusted_connection=no;UID={2};PWD={3}"
        .format(server, database, username, password))
    cursor = conn.cursor()
    cursor.execute(
        'SELECT  BusinessEntityID, FirstName, LastName from Person.Person'
    )
    columns = [column[0] for column in cursor.description]
    results = []
    #rows = cursor.fetchall()
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return {'results':results}


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/persons', methods=['GET'])
def persons():
    return getPersons()

@app.route('/person/<int:BusinessEntityID>', methods=['GET'])
def person(BusinessEntityID):
    return getPerson(BusinessEntityID)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


app.run()

