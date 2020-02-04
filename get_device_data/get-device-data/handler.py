import requests
import json
import psycopg2
import os

dbname = os.getenv('POSTGRESDBNAME')
user = os.getenv('POSTGRESUSER')
password = os.getenv('POSTGRESPASSWORD')
host = os.getenv('POSTGRESHOST')
port = os.getenv ('POSTGRESPORT')

params = {
  'dbname': dbname,
  'user': user,
  'password': password,
  'host': host,
  'port': port
}

def connection():
    conn = None
    try :
        conn = psycopg2.connect(**params)
    except Exception as e :
        print("[!] ",e)
    else:
        return conn

def query_db(query, args=(), one=False):
    cur = connection().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

def handle(req):
    if req == 'getalldevices':
        my_query = query_db("SELECT * FROM device")
        output=json.dumps(my_query, indent=4, sort_keys=True, default=str)
        print(output)
    elif 'getdevicebykey' in req:
        devicekey= req.split('_')[1]
        my_query = query_db("SELECT * FROM device WHERE device_key = '%s'" % devicekey)
        output=json.dumps(my_query, indent=4, sort_keys=True, default=str)
        print(output)
    elif 'getdevicebylocation' in req:
        devicelocation= req.split('_')[1]
        my_query = query_db("SELECT * FROM device WHERE device_location = '%s'" % devicelocation)
        output=json.dumps(my_query, indent=4, sort_keys=True, default=str)
        print(output)