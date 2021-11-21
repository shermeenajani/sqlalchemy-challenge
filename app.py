import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data for one year"""
    # Query precipitation data for one year
    one_year_prcp = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= "2016-08-24")\
    .order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from precipitation data for one year
    Hawaiiprecipitation = []
    for Date, Precipitation in one_year_prcp:
        precipitation_dict = {}
        precipitation_dict["date"] = Date
        precipitation_dict["prcp"] = Precipitation
        Hawaiiprecipitation.append(precipitation_dict)

    return jsonify(Hawaiiprecipitation)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station"""
    # Query station data
    StationCounts = session.query(Station.station).all()

    session.close()

    # Return the list of stations
    stations = list(np.ravel(StationCounts))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of observed temperature"""
    # Query temperature data
    one_year_temp = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= "2016-08-24")\
        .filter(Measurement.station=='USC00519281')\
        .order_by(Measurement.date).all()

    session.close()

    # Return a list of temperature data for one year for the most active station
    tobs = list(np.ravel(one_year_temp))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def startdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a min, avg and max temperature from a start date"""
    # Query temperature data
    startdate = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()

    session.close()

    # Return the min, avg and max temperature from a start date
    startlist= list(np.ravel(startdate))

    return jsonify(startlist)

@app.route("/api/v1.0/<start>/<end>")
def startenddate(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return min, avg and max temperature for a time period"""
    # Query temperature data from start to end date
    startenddate = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()

    session.close()

    # Return the min, avg and max temperature for a time period
    startendlist= list(np.ravel(startenddate))

    return jsonify(startendlist)
    
if __name__ == '__main__':
    app.run(debug=True)
