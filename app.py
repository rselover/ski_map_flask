#import pandas as pd
#import geopandas as gpd
#from shapely.geometry import Point
#import sqlite3
#import pyodbc
import json
import mysql.connector as sql

from flask import Flask, render_template
from flask import jsonify
app= Flask(__name__)

@app.route("/kids_ski.geojson")

def db_geojson():
    # Will update with pyodbc
    #sql_data=('kids_ski.db')
    #conn=sqlite3.connect(sql_data)
    server='skidata.coanuqqxa6px.us-west-2.rds.amazonaws.com'
    port=3306
    db='skidata'
    usr='skiadmin'
    pwd='RTtxdrNgw6tKNKQ'
    conn=sql.connect(user=usr,password=pwd,host=server,database=db)
#    conn_str='DRIVER={MySQL ODBC 3.51 Driver};SERVER='+server+';DATABASE='+database+';USER='+user+'PASSWORD='+pwd+'OPTION=3;'
#    conn=pyodbc.connect(conn_str)

    cursor=conn.cursor()

    cursor.execute('select * from kids_ski')
    result=cursor.fetchall()

    feature_list=[]

    for i in range(len(result)):
        r_dict=[dict(zip([column[0] for column in cursor.description],result[i])) for x in list(range(len(result)))]
        g_dict={}
        g_dict['geometry']={"type":"Point","coordinates":[r_dict[i]['lon'],r_dict[i]['lat']]}
        del r_dict[i]['lat']
        del r_dict[i]['lon']
        g_dict['properties']=r_dict[i]
        g_dict['type']="Feature"
        feature_list.append(g_dict)

    geojson={"type":"FeatureCollection","features":feature_list}

    return jsonify(geojson)

#Added per https://stackoverflow.com/questions/22181384/javascript-no-access-control-allow-origin-header-is-present-on-the-requested

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == "__main__":
    app.run(debug=True)
