# Imports
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

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

# Setup Flask
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
###### Precipitation endpoint ######
@app.route("/api/v1.0/precipitation")
def precipitation():
    print('Attempting to reach precipitation endpoint')
    # Set up variables to do calculations with
    recent_date = dt.date(2017,8,23)
    query_date = recent_date - dt.timedelta(days=365)
    active_station = 'USC00519281'
    # Create connection to DB with session
    session = Session(engine)
    # Query the data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).order_by(
            Measurement.date).all()
    # Close the session
    session.close()

    # Appenend and format our results to a list
    prcp_info = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_info.append(prcp_dict)
    # Return the JSONify results
    return jsonify(prcp_info)

@app.route("/api/v1.0/stations")
def stations():
    print("Attempting to reach precipitstion endpoint")
    #pull data
    session = Session(engine)
    results = session.query(Station.station, Station.station).all()
    session.close()
    #return results
    return jsonify(results)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)