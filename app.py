import json
import mysql.connector as sql
import os
from flask import Flask, render_template
from flask import jsonify
app = Flask(__name__)

@app.route('/mbkey/')
def mbkey():
  data=jsonify(os.getenv("MB"))
  return data.get_data(as_text=True)

@app.route('/') # this is the home page route
def db_geojson():

    conn = sql.connect(user=os.getenv("USR"), password=os.getenv("PASS"), host=os.getenv("SERVER"), database= os.getenv("DB"))

    cursor = conn.cursor()

    cursor.execute('select * from kids_ski')
    result = cursor.fetchall()

    feature_list = []

    for i in range(len(result)):
        r_dict = [
            dict(zip([column[0] for column in cursor.description], result[i]))
            for x in list(range(len(result)))
        ]
        g_dict = {}
        g_dict['geometry'] = {
            "type": "Point",
            "coordinates": [r_dict[i]['lon'], r_dict[i]['lat']]
        }
        del r_dict[i]['lat']
        del r_dict[i]['lon']
        g_dict['properties'] = r_dict[i]
        g_dict['type'] = "Feature"
        feature_list.append(g_dict)

    geojson = {"type": "FeatureCollection", "features": feature_list}

    data=jsonify(geojson)
    return data.get_data(as_text=True)
    

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response
   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080) # This line is required to run Flask on repl.it
