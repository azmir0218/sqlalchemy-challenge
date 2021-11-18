import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
# measurement = Base.classes.measurement
# station = Base.classes.station
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
        f"/api/v1.0/stations <br/>"
        f"api/v1.0/tobs <br/>"
        f"api/v1.0/[start-date format: yyyy-mm-dd]<br/>"
        f"api.v1.0/[start-date format: yyyy-mm-dd]/[end-date format: yyyy-mm-dd]"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Base.classes.measurement.date, Base.classes.measurement.prcp).filter(
        Base.classes.measurement.date >= '2016-08-23').filter(Base.classes.measurement.date <= '2017-08-23').all()

    # close the session
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_measurements = []
    for date, prcp in results:
        # create an empty object
        measurement_dict = {}
        # creat the keys
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp

        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Base.classes.measurement.station, func.count(Base.classes.measurement.station)).group_by(
        Base.classes.measurement.station).order_by(func.count(Base.classes.measurement.station).desc()).al()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    # return statement
    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
