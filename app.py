from flask import Flask, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    
    return( "Welcome to Climate Analysis API<br/>"
            f"List all available api routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start-date><br/>"
            f"/api/v1.0/<start-date>/<end-date><br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    precdata = session.query(measurement.station, measurement.date, measurement.prcp).all()
    
    session.close()
    
    precipitation = []
    for date, prcp, station in precdata:
        precdata_dict = {}
        precdata_dict['station'] = station
        precdata_dict['date'] = date
        precdata_dict['prcp'] = prcp
        precipitation.append(precdata_dict)
        
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    st=session.query(Station).all()
    stations=[]  
    for station in st:
        stations.append(station.station)
        
    session.close()
    return jsonify(stations)    
        
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    year_data = session.query(measurement.station, measurement.date, measurement.tobs)\
            .filter(measurement.station == 'USC00519281').filter(measurement.date > '2016-08-22').all()
    
    session.close()
    year_temp = []
    for tobs in year_data:
        year_temp.append(tobs)
    return jsonify(year_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    calc = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),
                  func.max(measurement.tobs)).filter(measurement.date >= start).\
                  filter(measurement.date <= end).all()
    session.close()
    return jsonify(calc)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    calc = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),
                  func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    return jsonify(calc)

if __name__ == "__main__":
    app.run(debug=False)