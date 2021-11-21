import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine(
    'sqlite:////Users/azmirsuljic/Desktop/Class_homework/sqlalchemy hw/sqlalchemy-challenge/Resources/hawaii.sqlite')


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
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
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(
        measurement.date >= '2016-08-23').filter(measurement.date <= '2017-08-23').all()

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
    results = session.query(measurement.station, func.count(measurement.station)).group_by(
        measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    # return statement
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # create our session (link) from Python to the DB
    session = Session(engine)
    # Query the dates and the temp. observations of the most active station for the last year of data
    most_active = 'USC00519281'
    obser_data = session.query(measurement.date, measurement.tobs).filter(
        measurement.date >= '2016-08-23').filter(measurement.date <= '2017-08-23').filter(measurement.station == most_active).all()

    session.close()
# Convert list of tuples into normal list
    all_obs_data = list(np.ravel(obser_data))
# return statement
    return jsonify(all_obs_data)


@app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>")
def start_date(start):

    # create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    start_date_calc = []
    for min, avg, max in results:
        # create an empty object
        start_dict = {}
        # creat the keys
        start_dict["min_temp"] = min
        start_dict["avg_temp"] = avg
        start_dict["max_temp"] = max

    start_date_calc.append(start_dict)
    # start_calc = list(np.ravel(results))

    # return statement
    return jsonify(start_date_calc)
    # return jsonify(start_calc)


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_and_end(start_date, end_date):

    session = Session(engine)
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.
                            max(measurement.tobs)).filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    session.close()

    end_date_calc = []
    for min, avg, max in results:

        end_dict = {}

        end_dict["min_temp"] = min
        end_dict["avg_temp"] = avg
        end_dict["max_temp"] = max

    end_date_calc.append(end_dict)

    return jsonify(end_date_calc)


if __name__ == '__main__':
    app.run(debug=True)
