import csv
import json
import psycopg2

# DATABASE INFO
dbInf = open('C:/Users/savac/Desktop/Feedback/jsonFiles/databaseInfo.json')
db_info = json.load(dbInf)
hostname = db_info['hostname']
database = db_info['databaseName']
username = db_info['username']
pwd = db_info['password']
port_id = db_info['portID']
dbInf.close()

def insert():
    cursor,connection = None,None
    try:
        connection = psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
        cursor = connection.cursor()
        insert_script = 'INSERT INTO faculties (name,years) VALUES (%s,%s)'
        with open("C:/Users/savac/Desktop/Feedback/CSV/facultati.csv","r",encoding='iso8859-2') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                insert_data = (row[0], row[1])
                cursor.execute(insert_script, insert_data)
                connection.commit()
    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

insert()












