# Imports
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
# Import pandas to make dict from dataframes
import pandas as pd

# Setting up Database
# Create engine and reflect 
db_path = 'Resources/hawaii.sqlite'
engine = create_engine(f"sqlite:///{db_path}")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create session
session = Session(engine)

# Calculate vars for app calculations
query_date = dt.date(2017, 8,23) - dt.timedelta(days=365)
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
# Making pandas dataframes
df = pd.DataFrame(results, columns=['Date', 'Prcp'])
# Drop the missing frames
df = df.dropna()
# Reset dataframe indexc
df = df.reset_index()
# Create a dictonary to jsonify results
prcp_dict = df.to_dict('results')

###

results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').all()
# Create dict of the stations
stations = session.query(Station.station, Station.name).all()
stations_df = pd.DataFrame(stations, columns=['Station', 'Name'])
stations_dict = stations_df.to_dict('results')
print(stations_dict)
# Create dict of the Temp Obs (tobs)
tobs_df = pd.DataFrame(results, columns=['Station', 'Date', 'Temperature'])
tobs_dict = tobs_df.to_dict('results')

# Setup Flask App
app = Flask(__name__)

# Apps Index Route
@app.route('/')
def home():
    """List all available api routes."""
    return (
        f'<strong>Api Endpoints</strong><br/>'
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )
### Precipitation endpoint ###
@app.route('/api/v1.0/precipitation')
def precipitation():
    return jsonify(prcp_dict)
### Stations endpoint ###
@app.route('/api/v1.0/stations')
def stations():
    return jsonify(stations_dict)
### Tobs endpoint ###
@app.route('/api/v1.0/tobs')
def tobs():
    return jsonify(tobs_dict)
### <start> endpoints ###
@app.route('/api/v1.0/<date>')
def start(date):
    start_results = session.query(Measurement.date, func.avg(Measurement.tobs,func.min(Measurement.tobs),func.max(Measurement.tobs))).\
                 filter(Measurement.station >= date).\
                     group_by(Measurement.station).all()
    return jsonify(start_results)            

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)