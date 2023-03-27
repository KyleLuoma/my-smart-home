from flask import Flask
from flask import request, session
from flask_session import Session
import mariadb
import json

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

db_info = json.load(open("./dbinfo.json"))

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


@app.route("/updatetemp/", methods = ["GET", "POST"])
def update_temp():
    if request.method == "POST":
        print("From client", request.remote_addr)
        print(request.json['temperature'], ", ", request.json['humidity'])
        session['current_temp'] = request.json['temperature']
        session['current_humidity'] = request.json['humidity']
    return "received"


@app.route("/gettemp")
def get_temp():
    return("<p>Temperature: {}</p><p>Humidity: {}</p>".format(session['current_temp'], session['current_humidity']))