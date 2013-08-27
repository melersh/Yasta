'''
Created on Aug 27, 2013

@author: mohamedelersh
'''

from flask import Flask, request


app = Flask('yasta')
app.debug = True

# app.config.from_object('settings')

@app.route("/station", methods=['GET'])
def getStationById():
    stationid = int(request.values.get('id', 1) );
    return 'Station %d' % stationid;


if __name__ == '__main__':
    app.run();