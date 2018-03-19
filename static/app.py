# Import Necessary libraries
import numpy as np

import os 
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session 
from sqlalchemy import inspect, create_engine, func, desc 
from sqlalchemy.engine import reflection 

 
from flask import ( 
     Flask, 
     render_template, 
     jsonify, 
     request, 
     redirect) 
 
app = Flask(__name__) 

from flask_sqlalchemy import SQLAlchemy 
 
Base = automap_base() 

engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite") 
 
Base.prepare(engine, reflect=True) 
 
 
Metadata = Base.classes.samples_metadata 
Otu = Base.classes.otu 
Samples = Base.classes.samples 
 
session = Session(engine) 
 
 
 def __repr__(self): 
     return '<Bio %r>' % (self.name) 
 
 
 # Create a route to return the dashboard homepage 
 @app.route("/") 
 def home(): 
     return render_template("index.html") 
 
 
 #Create a route that returns a list of the sample names 
 @app.route("/names") 
 def names_list(): 
     inspector = inspect(engine) 
     tables = inspector.get_table_names() 
     columns = inspector.get_columns('samples') 
     names = [] 
     for column in columns[1:]: 
         names.append(column['name']) 
     return jsonify(names) 
 
 
 # Create a route that returns a list of OTU descriptions
 @app.route("/otu") 
 def description(): 
     descrip = session.query(Otu.lowest_taxonomic_unit_found).all() 
     otu_descrip = [] 
     for descrip in descrips: 
         otu_descrips.append(descrip) 
     return jsonify(otu_descrips) 
 

 # Create a route for Metadata per sample
 @app.route('/metadata/<sample>') 
 def sample_meta(sample): 
     sample_id = sample[3:] 
     result = session.query(Metadata.AGE,\ 
                            Metadata.BBTYPE,\ 
                            Metadata.ETHNICITY,\ 
                           Metadata.GENDER,\ 
                            Metadata.LOCATION,\ 
                            Metadata.SAMPLEID)\ 
                     .filter(Metadata.SAMPLEID==sample_id).first() 
     metadatadictionary = { 
         "AGE": result[0], 
         "BBTYPE": result[1], 
         "ETHNICITY": result[2], 
         "GENDER": result[3], 
         "LOCATION": result[4], 
         "SAMPLEID": result[5] 
     } 
     return jsonify(metadatadictionary) 
 
 
# Create a route for weekly Washing frequency 
@app.route('/wfreq/<sample>') 
def wfreq(sample): 
     sample_id = sample[3:] 
     frequency = session.query(Metadata.wfreq,Metadata.SAMPLEID).filter(Metadata.SAMPLEID == sample_id).first() 
     return jsonify(frequency[0]) 
 
 
 # Create a route for OTU IDs and values per sample 
 @app.route('/samples/<sample>') 
 def persamp(sample): 
     sample_id_query = f"Samples.{sample}" 
     results = session.query(Samples.otu_id, sample_id_query).order_by(desc(sample_id_query)) 
     sampledictionary = {"otu_ids": [result[0] for result in results], 
                 "sample_values": [result[1] for result in results]} 
     return jsonify(sampledictionary) 
 
 
 if __name__ == '__main__': 
    app.run(debug=True) 
