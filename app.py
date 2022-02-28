import datetime as dt
from lib2to3.pytree import _Results
from unittest import result
import numpy as np 
import pandas as pd
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################

# Datebase set up 

######################################

engine = create_engine("sqlite:///.sqlite")

# Reflect an exis
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

#Save referenes to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create our session from python to the DB
session = Session(engine)
##############################
#flask setup
##############################
app = Flask(__name__)
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data fro the last year"""
    pre_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= pre_year).all()

    precip = {date: prcp for date, prcp in precipitation}
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Station.station).all()

    station = list(np.ravel(results))

    return jsonify(stations.stations) # { stations []}
@app.rout("api/v1.0/tobs")
def temp_monthly():
    """Return the temp obserbation for previous year"""
    pre_year  = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results - session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC0051928').\
        filter(Measurement.date >= pre_year).all()

    # unravel resutls into list and converting to a pythong list
    temps = list(np.ravel(_Results))
    return jsonify(temps=temps)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    # Calculates min , avg, max with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__  == '__main__':
    app.run()
