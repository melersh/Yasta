'''
Created on Aug 27, 2013

@author: mohamedelersh
'''
from flask import request, make_response
from yasta import app
from google.appengine.ext import ndb

class Station(ndb.Model):
    nearest_cell_ids = ndb.IntegerProperty(repeated=True)
    name = ndb.StringProperty()
    full_name = ndb.StringProperty()
    
@app.route("/station",  methods=['POST'])
def createStation():
    station = Station()
    station.name = request.values.get('name')
    station.full_name = request.values.get('full_name')
    station.put()
    resp = make_response('', 201)
    resp.headers['Location'] = '/station/' + station.name
    return resp

@app.route("/station/<station_name>",  methods=['GET'])
def getStationByStationName(station_name):
    qry = Station.query(Station.name == station_name)
    stations = qry.fetch(1)
    if len(stations) == 0:
        result = "No station found with name '" + station_name + "' !"
    else:
        result = "Found station <br>"
        for station in stations:
            result += station.full_name + "<br>"

    return result
