#################################################
# Imports
#################################################
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import os
import sys

# Setup the path to the sql file
print(os.path.dirname(__file__))

root_project_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, root_project_path)

file_path = os.path.join(root_project_path, "../resources/hawaii.sqlite")

#################################################
# Database Setup and Reflection
#################################################

# Create the engine
engine = create_engine(f'sqlite:///{file_path}')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/start/end"
     )

# Precipitation path
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    # Return the JSON representation of your dictionary.

    # Create our engine session 
    session = Session(engine)

    # List of rain data including the date and prcp of each date
    rain_data = session.query(Measurement.date, Measurement.prcp).all()

    # then close session don't need it anymore
    session.close()

    # Create a dict from the row data and append to a list of rain_hi
    rain_list = []
    for date, prcp in rain_data:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        rain_list.append(rain_dict)

    # Turn resulting dict into a JSON
    return jsonify(rain_list)

# Create station path
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.

    # Create our engine session 
    session = Session(engine)

    # Query all unique station names
    stations = session.query(Station.station).distinct().all()

    # then close session don't need it anymore
    session.close()

    # Turn resulting station list into a JSON
    return jsonify(stations)

# Create temperature data path
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    
    # Create our engine session 
    session = Session(engine)

    # Find the most recent date in the data, split it into its parts
    # of the date, and calculate the date one year prior to the most recent date
    recent_date = session.query(func.max(Measurement.date)).scalar()
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    query_date = recent_date - dt.timedelta(days=365)
    
    # Find the most active station by querying out the station name along
    # with a count of how many measurements were made by the station
    # ordered descending. The first one will be the station we are looking for.
    most_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    active_station = most_active[0][0]

    # Query out the data for the most active station within the past year
    # in the data using the calculated date for one year prior.
    most_active_info = session.query(Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station == active_station).all()

    # then close session don't need it anymore
    session.close()

    # List all the temperature data from the query and turn it into JSON
    all_tobs = list(np.ravel(most_active_info))

    return jsonify(all_tobs)
    
# Create start path
@app.route("/api/v1.0/<start>")
def temp_stats(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

    # Create our engine session 
    session = Session(engine)

    # Query out the max temp, min temp, avg temp between a date entered
    # into by user and all dates greater than entered date and close session
    temps_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    # then close session don't need it anymore
    session.close()

    # Get the max temp, min temp, avg temp from the tuple to be turned into a JSON
    statline = [temps_start[0][0], temps_start[0][1], round(temps_start[0][2],2)]

    return jsonify(statline)

# Create start/end path
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_2(start, end):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

    # Create our engine session 
    session = Session(engine)

    # Query out the max temp, min temp, avg temp between a start date
    # end date range entered by the user and close session
    temps_start_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).\
                  filter(Measurement.date <= end).all()

    session.close()

    # Get the max temp, min temp, avg temp from the tuple to be madeturned into a JSON
    statline = [temps_start_end[0][0], temps_start_end[0][1], round(temps_start_end[0][2],2)]

    return jsonify(statline)

#################################################
# Flask main method
#################################################
if __name__ == "__main__":
    app.run(debug=False)

