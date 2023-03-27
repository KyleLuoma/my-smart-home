from flask import Flask
from flask import request
import mariadb
import json
import time

SMS_BLACKOUT_INTERVAL = 4 #hours minimum interval between messages

app = Flask(__name__)
app.config.from_object(__name__)

db_info = json.load(open("./dbinfo.json"))

add_observation_sql = """INSERT INTO observations(timestamp, station_ip, temp_f, humidity) VALUES (?, ?, ?, ?)"""

try:
    db_conn = mariadb.connect(
        user=db_info['username'],
        password=db_info['password'],
        host="192.168.1.17",
        port=3306,
        database='home-weather'
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

db_cur = db_conn.cursor()

f = open("./sql/create-observations-table.sql")
db_cur.execute(f.read())
f.close()
f = open("./sql/create-stations-table.sql")
db_cur.execute(f.read())
f.close()

try:
    update_temp_db_conn = mariadb.connect(
        user=db_info['username'],
        password=db_info['password'],
        host="192.168.1.17",
        port=3306,
        database='home-weather'
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform for update temperature route: {e}")
update_temp_db_cur = update_temp_db_conn.cursor()
@app.route("/updatetemp/", methods = ["GET", "POST"])
def update_temp():
    if request.method == "POST":
        print("From client", request.remote_addr)
        print(request.json['temperature'], ", ", request.json['humidity'])
        date_time = time.strftime('%Y-%m-%d %H:%M:%S')
        update_temp_db_cur.execute(add_observation_sql, (date_time, str(request.remote_addr), request.json['temperature'], request.json['humidity']))
        update_temp_db_conn.commit()
    return "received"


@app.route("/gettemp")
def get_temp():
    output = "<h1>Temp and Humidity</h1>"
    f = open("./sql/get-latest-observations.sql")
    db_cur.execute(f.read())
    hottest_location = ""
    hottest_temp = 0
    for row in db_cur:
        if row[3] > hottest_temp:
            hottest_temp = row[3]
            hottest_location = row[1]        
        print(row)
        output += ("<h2>"+row[1]+"</h2>\n") # Location
        output += ("<p>Temperature: {} </p>\n".format(str(row[3])))
        output += ("<p>Humidity: {} </p>\n".format(str(row[4])))
    f.close()
    output += "<h3>It is hotter in the {} right now. </h3>\n".format(hottest_location)
    return(output)