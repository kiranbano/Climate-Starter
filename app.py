import sqlalchemy
import flask_sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from flask import Flask
import datetime as dt
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect= True)

# save refernces to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create our session/ link from python to the database
session = Session(engine)

# setup the flask

app = Flask(__name__)

# FLASK ROUTES

app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the preciptation data for the last year"""
  
    # calculate the date  1 year ago from last date in databse
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year_date).\
            group_by(Measurement.date).all()
    

  
    total_precipitation = []
    
    for precip in preciptation:
        precip_dict = {}
        precip_dict["date"] = precip[0]
        precip_dict["prcp"] = precip[1]
        total_precipitation.append(precip_dict)    
        return jsonify(total_precipitation)

 
 
@app.route("/apiv1.0/stations")    
def stations():
    """Return a list of stations.""" 

    results = session.query(Stations.station).all()
# Unravel results into an ID ARRAY
    
    stations = list(np.ravel(results))

    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations (tobs) for previous year""" 
   
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # query all tobs of most active station from last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_year_date).all()
        
    temps = list(np.ravel(results))

    return jsonify(temps=temps)
 


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    new_start = start.replace(" ", "")
    new_end = end.replace(" ", "")
    results = session.query(func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    
    new_data = list(np.ravel(results))
    return jsonify(new_data)

if __name__ == "__main__":
    app.run(debug=True)
    