import requests
import json
import psycopg2
import os

# export the i.e export POSTGRESDBNAME='demo'

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

def insert_device_db(device_key, device_name, device_desc, device_location):
    try: 
        cur = connection().cursor()
        postgres_insert_query = """ INSERT INTO device (device_key, device_name, device_desc, device_location) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (device_key, device_name, device_desc, device_location)
        cur.execute(postgres_insert_query, record_to_insert)
        cur.connection.commit()
        count = cur.rowcount
        print (count, "Record inserted successfully into device table")
    except Exception as e :
        print("failed to insert data", e)
    finally:
        cur.close
        cur.connection.close()

my_string="hello python world?4dcf92826314c9c3308b643fa0e579b87f7afe42&Samsung&Galaxy&319583"
values_list = my_string.split("?",1)[1] 
values = values_list.split("&")
insert_device_db (values[0],values[1],values[2],values[3])
print(values)

def handle(req):
    if 'insertdatadevices' in req:
        values_list=req.split("?",1)[1] 
        values = values_list.split("&")
        insert_device_db(values[0],values[1],values[2],values[3])
        print("successful")


