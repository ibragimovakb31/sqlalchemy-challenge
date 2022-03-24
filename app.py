
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

#flask setup
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    test = (f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

    return (test)

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    date_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
   
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date>=date_ago).all()
    
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    date_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    results=(session.query(measurement.date,(measurement.tobs))
                    .filter(func.strftime(measurement.date) > date_ago)
                    .filter(measurement.station=='USC00519281')
                    .all())

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("//api/v1.0/<start>")
@app.route("//api/v1.0/<start>/<end>")
def start1(start=None, end=None):
    session = Session(engine)
    if not end:
        results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
            filter(measurement.date == #lar\ger or equal to then start date 'USC00519281').all() 
    
    results = session.query
if __name__ == '__main__':
    
    #other on esmaller equal end adye larfer eqauls start dfate
    app.run(debug=True)



    @app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end=None):

    q = session.query(str(func.min(Measurement.tobs)), str(func.max(Measurement.tobs)), str(func.round(func.avg(Measurement.tobs))))

    if start:
        q = q.filter(Measurement.date >= start)

    if end:
        q = q.filter(Measurement.date <= end)

    # convert results into a dictionary (I opted for a dictionary instead of a list here so that it was clear with labels which temp was the min, the max, and the average)

    results = q.all()[0]

    keys = ["Min Temp", "Max Temp", "Avg Temp"]

    temp_dict = {keys[i]: results[i] for i in range(len(keys))}

    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)

