#!flask/bin/python
from flask import Flask
import mysql.connector
import os
from flask import jsonify,json


app = Flask(__name__)

@app.route('/')
def index():
	mydb = mysql.connector.connect(
		host=os.environ.get('DB_HOST'),
		user=os.environ.get('DB_USER'),
		passwd=os.environ.get('DB_PASSWORD'))
	mycursor = mydb.cursor()
	mycursor.execute("USE irancell;")
	mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
	return jsonify(str("save"))

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True,port=80)
