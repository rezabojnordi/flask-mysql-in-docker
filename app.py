#!flask/bin/python
from flask import Flask
import mysql.connector
import os
from flask import jsonify,json,request
import socket
from time import time
import random


#-----------
mydb = mysql.connector.connect(
	host=os.environ.get('DB_HOST'),
	user=os.environ.get('DB_USER'),
	passwd=os.environ.get('DB_PASSWORD'),
	
	)

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
    results["status"]=status
    results["data"]=message
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
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("USE irancell;")
		sql = "INSERT INTO website_link (url,click,time,agent) VALUES (%s, %s,%s,%s)"
		val = (str(json_data["url"]),str(json_data["click"]),
		str(json_data["time"]),str(json_data["agent"]))
	# val = [("John", "Highway 21"),("reza","bojnordi")]
		mycursor.execute(sql, val)
		mydb.commit()
		return jsonify("save in tables")
	except expression as e:
		return error_result("fail","insert error%s"%e) 









# @app.route('/get_app',methods=['GET'])
# def get_app():
# 	mycursor = mydb.cursor()
# 	mycursor.execute("USE irancell;")
# 	ip_address = request.remote_addr
# 	#ip_id,link_id,expire,time,
# 	# 'SELECT a.tutorial_id, a.tutorial_author, b.tutorial_count
#     #   FROM tutorials_tbl a, tcount_tbl b
#     #   WHERE a.tutorial_author = b.tutorial_author';
# 	#app = "SELECT * from website_link where enable=1 LEFT JOIN app ON id=app.link_id and app.expire > %d"%time_now
# 	#app = " SELECT website_link.id,website_link.link,website_link.click,website_link.time from website_link LEFT JOIN app ON website_link.id=app.link_id and app.expire < %d where website_link.enable=1;"%time_now
# 	#app ="select * from website_link join app on website_link.id = app.link_id and app.expire < %d and website_link .enable=1;"%time_now
# 	ip = phone_ip(ip_address)
# 	time_now = int(time())
# 	app ="select * from website_link where website_link.agent =1 and website_link.id not in (select link_id from app where app.expire > %d and app.ip_id=(select id from phone_ip where phone_ip.address_ip ='%s'))"%(time_now,ip_address)
# 	mycursor.execute(app)
# 	myresult = mycursor.fetchall()
# 	resultBanner ={}
# 	tuple_link = []
# 	for count,row in enumerate(myresult):
# 		times = random.randint(10, 60)
# 		resultBanner[str(count)]={
# 			"url":row[1],
# 			"click":row[2],
# 			"time":times,
# 		}
# 		tuple_link.append(row[0])
# 	if (len(tuple_link) > 0):
# 		cn_tuple = tuple(tuple_link)
# 		tmp = application_info(row[4],cn_tuple)
# 		return success_result("success",resultBanner)
# 	return error_result("restart","restart airplan") 
# 	#return str(tmp)


@app.route('/remove_app',methods=['DELETE'])
def remove_app():
	# table_name =request.form.get("table_name","")
	mycursor = mydb.cursor(buffered=True)
	mycursor.execute("USE irancell;")
	#mycursor.execute("DROP TABLE" +" "+str(table_name))
	mycursor.execute("delete from app")
	return success_result("success","remove app")


"""
def for get all ip
"""
@app.route('/phone_ip',methods=['GET'])
def get_phone_ip():
	mycursor = mydb.cursor(buffered=True)
	mycursor.execute("USE irancell;")
	select = "SELECT * FROM phone_ip"
	mycursor.execute(select)
	myresult = mycursor.fetchall()
	return success_result("success",myresult)


"""
def for get all website_link
"""
@app.route('/get_website_link',methods=['GET'])
def get_website_link():
	mycursor = mydb.cursor(buffered=True)
	mycursor.execute("USE irancell;")
	select = "SELECT * FROM website_link"
	mycursor.execute(select)
	myresult = mycursor.fetchall()
	data={}
	for row in myresult:
		data["url"] = row[1]
		data["click"] = row[2]
		data["time"] = row[3]
		data["agent"] = row[4]
	return success_result("success",data)



def insert_apps(ip_id,resultBanner):
	my_cursor = mydb.cursor(buffered=True)
	my_cursor.execute("USE irancell;")
	select = "SELECT * FROM app WHERE ip_id ="+"'"+str(ip_id[0])+"'"
	my_cursor.execute(select)
	my_result = my_cursor.fetchone()

	if (my_result != None):
		return my_result
	else:
		insert_app = "INSERT INTO app (ip_id, link_id,expire,time,status) VALUES (%s,%s,%s,%s,%s)"
		res_data=[]
		expire = time()
		for i in range(len(resultBanner)):
			for j in range(len(resultBanner[i])):
				pass
			res_data.append((ip_id[0],resultBanner[i][0],expire,resultBanner[i][3],"pending"))
		my_cursor.executemany(insert_app, res_data)
		mydb.commit()
		return my_result



def phone_ip(ip_add):
	my_cursor = mydb.cursor(buffered=True)
	my_cursor.execute("USE irancell;")
	select = "SELECT * FROM phone_ip WHERE address_ip ="+"'"+str(ip_add)+"'"
	select_all = "SELECT * FROM phone_ip"
	my_cursor.execute(select)
	my_result = my_cursor.fetchone()
	if (my_result != None):
		#return "error"+str(myresult)
		return my_result
	else:
		sql = "INSERT INTO phone_ip (address_ip) VALUES (%s)"
		val = [(str(ip_add))]
		my_cursor.execute(sql, val)
		mydb.commit()
		return my_result

		
	#"select * from website_link where website_link.enable =1 and website_link.id not in (select link_id from app where app.expire > %d and app.ip_id=(select id from phone_ip where phone_ip.address_ip ='%s'))"%(time_now,ip_address)
##	"SELECT * FROM website_link where website_link.id not in (select link_id from app where app.link_id ='1' and app.ip_id=(select id from phone_ip where phone_ip.address_ip='172.19.0.1'))"
	#SELECT * FROM website_link where website_link.id not in (select link_id from app where app.link_id ='1' and app.ip_id=(select id from phone_ip where ='172.19.0.1'))
   #"SELECT * FROM website_link where website_link.id not in (select link_id from app where app.link_id ='1' and app.ip_id=(select id from phone_ip where phone_ip.address_ip='172.19.0.1') and app.status=(select status from app where status='pending'))"	
#	SELECT * FROM website_link where website_link.id in (select link_id from app where app.link_id ='%s' and app.ip_id=(select id from phone_ip where phone_ip.address_ip='%s' and app.status='pending'))

	#select = "SELECT * FROM website_link where website_link.id in (select link_id from app where app.link_id ='%s' and app.ip_id=(select id from phone_ip where phone_ip.address_ip='%s' and app.status='pending'))"%(1,"172.19.0.1")
    #select = "select website_link.url,website_link.click,website_link.time,app.status,phone_ip.address_ip from website_link inner join app on app.link_id = website_link.id inner join phone_ip on app.ip_id = phone_ip.id where app.status='pending' and phone_ip.address_ip='172.19.0.1'"
   #select website_link.url,website_link.click,website_link.time,app.status,phone_ip.address_ip from website_link inner join app on app.link_id = website_link.id inner join phone_ip on app.ip_id = phone_ip.id where app.status='pending'
def get_app(phone_ip,resultBanner):
	my_cursor = mydb.cursor(buffered=True)
	my_cursor.execute("USE irancell;")
	
	select ="select website_link.url,website_link.click,website_link.time,app.status,phone_ip.address_ip FROM website_link inner join app on app.link_id=website_link.id inner join phone_ip on app.ip_id=phone_ip.id WHERE app.status='pending' and phone_ip.address_ip='%s'"%(phone_ip[1])
	my_cursor.execute(select)
	my_result = my_cursor.fetchall()
	site = []
	agents = ["Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/46.1.2.5140",
	"Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/46.1.2.5140",
	"Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 EdgiOS/46.1.2 Mobile/15E148 Safari/605.1.15",
	"Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36 Edge/40.15254.603",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
	"Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
	"Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
	"Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.153 Safari/537.36",
	"Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.153 Safari/537.36",
	"Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.153 Safari/537.36",
	"Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/85.0",
	"Mozilla/5.0 (Android 11; Mobile; LG-M255; rv:85.0) Gecko/85.0 Firefox/85.0",
	"Mozilla/5.0 (X11; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0",
	"Mozilla/5.0 (Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
	"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:85.0) Gecko/20100101 Firefox/85.0"]

		
	agent_rand = random.randint(0, 25)
	for i in range(len(my_result)):
		for j in range(len(my_result[i])):
			pass
		site.append({
			"url":resultBanner[i][1],
			"click":resultBanner[i][0],
			"time":resultBanner[i][2],
			"time":resultBanner[i][3],
			"agent": agents[agent_rand],
			"status":"ok"
		})

	return site



@app.route('/v1/token',methods=['GET'])
def token():
	'''
	# headser
	read mac from header if mac exist in your tables generete token and return
	Note:
	tables consis of mac and token
	if mac is not exisist in our databse return permission deny otherwise store token for mac and return it.
	disable and enable filed in tables 
	'''
	pass


@app.route('/v1/check',methods=['GET'])
def check():
	my_cursor = mydb.cursor(buffered=True)
	my_cursor.execute("USE irancell;")
	# header read token and check exist in your tables
	# check disiable and enable mac
	ip_address = request.remote_addr
	select = "SELECT * FROM website_link"
	my_cursor.execute(select)
	my_result = my_cursor.fetchall()
	data=[]
	ip = phone_ip(ip_address)
	for row in my_result:
		data.append(row)
	app_info = insert_apps(ip,data)
	get_app_all = get_app(ip,data)
	return success_result("success",get_app_all)


@app.route('/v1/status_ok',methods=['POST'])
def status_ok():
	my_cursor = mydb.cursor(buffered=True)
	my_cursor.execute("USE irancell;")
	ip_address = request.remote_addr
	url = request.args.get('url')
	is_status = "ok"
	expire = time()
	###"Update app SET status ='ok' WHERE app.ip_id =(select id from phone_ip where phone_ip.address_ip='172.19.0.1' and app.time='18')"
	#update_status = "Update app SET status ='%s' WHERE app.ip_id =(select id from phone_ip where phone_ip.address_ip='%s' and app.time='%s')"%(is_status,ip_address,time) 
	#my_cursor.execute(update_status)
	#mydb.commit()
	### add id_mac for app tables
	# select phone_id 
	select_phone_id = "select id from phone_ip where phone_ip.address_ip='%s')"%(ip_address)
	select_link_id = "select id from website_link where website_link.url='%s')"%(url)
	insert_status = "INSERT INTO app(ip_id,link_id,expire,time,status) valuses (%s,%s,%s,%s,%s)"
	val = (select_phone_id,select_link_id,expire,"",is_status)
	my_cursor.execute(insert_status, val)
	mydb.commit()
	return success_result("success",[])



# if __name__ == '__main__':
# 	app.run(host= '0.0.0.0',debug=True,port=80)


# 		insert_app = "INSERT INTO app (ip_id, link_id,expire,time,status) VALUES (%s,%s,%s,%s,%s)"
# 		res_data=[]
# 		expire = time()
# 		for i in range(len(resultBanner)):
# 			for j in range(len(resultBanner[i])):
# 				pass
# 			res_data.append((ip_id[0],resultBanner[i][0],expire,resultBanner[i][3],"pending"))
# 		my_cursor.executemany(insert_app, res_data)
# 		mydb.commit()
# 		return my_result