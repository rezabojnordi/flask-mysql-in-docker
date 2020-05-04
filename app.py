#!flask/bin/python
from flask import Flask
import mysql.connector
import os
from flask import jsonify,json,request
import socket


#-----------
mydb = mysql.connector.connect(
	host=os.environ.get('DB_HOST'),
	user=os.environ.get('DB_USER'),
	passwd=os.environ.get('DB_PASSWORD'))

#-----------

app = Flask(__name__)

# @app.route('/')
# def index():
# 	mycursor = mydb.cursor()
# 	mycursor.execute("USE irancell;")
# 	mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
# 	return jsonify(str("save"))

#-------------------------------
def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return jsonify(results)




def success_result(status,message):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    results["data"]['message']=message
    return jsonify(results)

#-------------------------------# return error_result("fail","insert error%s"%e) 


@app.route('/create_tb',methods=['POST'])
def create_tb():
	#dbname =request.form.get("dbname","")
	json_data = request.get_json()
	#request.form['projectFilepath']
	tmp_str = ""
	for i in json_data["tables"]:
		print(i["field"])
		tmp_str += str(i["field"])+" "+str(i["type"])+" "
	mycursor = mydb.cursor()
	mycursor.execute("USE irancell;")
	mycursor.execute("CREATE TABLE"+" "+str(json_data["table_name"])+" "+"(id INT AUTO_INCREMENT PRIMARY KEY,"+" "+tmp_str+ ")")
	return str("save db")



@app.route('/rm_tb',methods=['GET'])
def rm_tb():
	table_name =request.form.get("table_name","")
	mycursor = mydb.cursor()
	mycursor.execute("USE irancell;")
	mycursor.execute("DROP TABLE" +" "+str(table_name))
	return str("remove tables"+" "+str(table_name))



@app.route("/add_website_link",methods=['POST'])
def add_website_link():
	try:
		json_data = request.get_json()
		mycursor = mydb.cursor()
		mycursor.execute("USE irancell;")
		sql = "INSERT INTO website_link (link,click,time,enable) VALUES (%s, %s,%s,%s)"
		val = (str(json_data["link"]),str(json_data["click"]),
		str(json_data["time"]),str(json_data["enable"]))
	# val = [("John", "Highway 21"),("reza","bojnordi")]
		mycursor.execute(sql, val)
		mydb.commit()
		return jsonify("save in tables")
	except expression as e:
		return error_result("fail","insert error%s"%e) 




@app.route('/get_app',methods=['GET'])
def get_app():
	mycursor = mydb.cursor()
	mycursor.execute("USE irancell;")
	ip_address = request.remote_addr
	ip = phone_ip(ip_address)
	#ip_id,link_id,expire,time,
	app = "select * from website_link"
	mycursor.execute(app)
	myresult = mycursor.fetchall()
	resultBanner ={}
	tuple_link = []
	for count,row in enumerate(myresult):
		resultBanner[str(count)]={
			"link":row[1],
			"click":row[2],
			"time":row[3],
			"enable":row[4]
		}
		tuple_link.append(row[0])
	cn_tuple = tuple(tuple_link)

	tmp = application_info(ip_address,cn_tuple)
	return success_result("success",tmp)
	#return str(tmp)


def application_info(ip_add,resultBanner):
	mycursor = mydb.cursor()
	mycursor.execute("USE irancell;")
	select_phone_ip = "SELECT * FROM phone_ip WHERE address_ip ="+"'"+str(ip_add)+"'"
	mycursor.execute(select_phone_ip)
	myresult = mycursor.fetchone()
	insert_app = "INSERT INTO app (ip_id, link_id,expire,time) VALUES (%s,%s,%s,%s)"
	res_data=[]
	for insert in resultBanner:
		res_data.append((myresult[0],insert,"3658","2:25"))
	mycursor.executemany(insert_app, res_data)
	mydb.commit()
	return "save in app"



def phone_ip(ip_add):
	mycursor = mydb.cursor()
	mycursor.execute("USE irancell;")
	select = "SELECT * FROM phone_ip WHERE address_ip ="+"'"+str(ip_add)+"'"
	mycursor.execute(select)
	myresult = mycursor.fetchall()
	if(myresult !=[]):
		#return "error"+str(myresult)
		return "0"
	else:
		sql = "INSERT INTO phone_ip (address_ip) VALUES (%s)"
		val = [(str(ip_add))]
		mycursor.execute(sql, val)
		mydb.commit()
		return "1"





# 	return jsonify(json_data["name"])


if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True,port=80)
