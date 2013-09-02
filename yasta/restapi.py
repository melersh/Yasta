'''
Created on Aug 27, 2013

@author: mohamedelersh
'''
from flask import request, make_response
from yasta import app
from google.appengine.ext import ndb
import logging 


class Station(ndb.Model):
    nearest_cell_ids = ndb.IntegerProperty(repeated=True)
    name = ndb.StringProperty()
    full_name = ndb.StringProperty()
    
    
class Route(ndb.Model):
    """Models an individual Route entry with all route details, like fair, working hours, source and destination stations, landmarks, and markable stations."""
    route_id = ndb.StringProperty()
    name = ndb.StringProperty()
    landmark = ndb.StringProperty(indexed=False)
    station_src = ndb.StringProperty()
    station_dest = ndb.StringProperty()
    working_hours_start = ndb.StringProperty(indexed=False)
    working_hours_end = ndb.StringProperty(indexed=False)
    fair= ndb.StringProperty()
    markable_stations = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    
@app.route("/route",  methods=['POST'])
def createRoute():
    route = Route()
    route.route_id = request.values.get('route_id')
    route.name = request.values.get('name')
    route.landmark = request.values.get('landmark')
    route.station_src = request.values.get('station_src')
    route.station_dest = request.values.get('station_dest')
    route.working_hours_start = request.values.get('working_hours_start')
    route.working_hours_end = request.values.get('working_hours_end')
    route.fair= request.values.get('fair')
    route.markable_stations = request.values.get('markable_stations')
    logging.log(logging.INFO, "Before put")
    route_key = route.put()
    logging.log(logging.INFO, "After put")

    resp = make_response('', 201)
    resp.headers['Location'] = '/route/' + str(route_key.id())
    return resp

@app.route("/search/<station_id>",  methods=['GET'])
def getAvailableRoutes(station_id):
    qry = Route.query(Route.station_src == station_id)
    available_routes = qry.fetch(10)
    if len(available_routes) == 0:
        result = "No available routes from your station.. id = '" + station_id + "' !"
    else:
        result = "Found Routes <br>"
        for route in available_routes:
            result += route.route_id + "  ==> moves from " +  route.landmark + " fair amount equal to " + route.fair + "EGP<br>"
    return result



@app.route("/fair/<route_id>",  methods=['GET'])
def getRouteFair(route_id):
    qry = Route.query(Route.route_id == route_id)
    tarrif = qry.fetch(1)
    if len(tarrif) == 0:
        result = "No Tarrif defined for this route. id = '" + route_id + "' !<br>"
    else:
        result = "Found Tarrif for route id =  '" + route_id + "' !"
        for route in tarrif:
            result +=  " Fair for " + route.route_id + "equal to " + route.fair + "EGP<br>"
    return result

@app.route("/route/<route_id>",  methods=['GET'])
def getRouteDetails(route_id):
    qry = Route.query(Route.route_id == route_id)
    route_record = qry.fetch(1)
    if len(route_record) == 0:
        result = "No details defined for this route. id = '" + route_id + "' !<br>"
    else:
        result = "Route Details for route. id = " + route_id + "' !<br><br>"
    for route in route_record:
        result +=  "Route Name is " + route.name + ".<br> "
        result +=  "fair equal to " + route.fair + "EGP<br> "
        result +=  "Land Mark is " + route.landmark + ".<br> "
        result +=  "markable stations in route are " + route.markable_stations + ".<br> "
    return result










@app.route("/station",  methods=['POST'])
def createStation():
    station = Station()
    station.name = request.values.get('name')
    station.full_name = request.values.get('full_name')
    station_key = station.put()
    resp = make_response('', 201)
    resp.headers['Location'] = '/station/' + str(station_key.id())
    return resp

@app.route("/station/<int:sid>",  methods=['GET'])
def getStationByStationId(sid):
    station_key = ndb.Key('Station', sid) 
    station = station_key.get()
    if station == None:
        result = "No station found with id '" + str(sid) + "' !"
    else:
        result = "Found station <br>"
        result += station.full_name + "<br>"

    return result

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
