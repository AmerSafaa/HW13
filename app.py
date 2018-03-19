#import necessary libraries
import numpy as np

import sqlalchemy 
import os 
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session 
from sqlalchemy import inspect, create_engine, func, desc 
from sqlalchemy.engine import reflection 

 
from flask import Flask
from Flask import render_template
From Flask import jsonify
From Flask import request
from Flask import redirect
 
app = Flask(__name__) 
 
from flask_sqlalchemy import SQLAlchemy 
engine = create_engine("belly_button_biodiversity.sqlite") 
 
# Reflecting db into a new model 
 Base = automap_base() 
 
 
 # Reflect tables 
 Base.prepare(engine, reflect=True) 
 
 
 # Save to class 
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
     # Create inspector and connect it to the engine 
     inspector = inspect(engine) 
     # Collect the names of the tables within the db 
     # tables = inspector.get_table_names() 
     # using the inspector to print the column names of tables 
     columns = inspector.get_columns('samples') 
     names = [] 
     for column in columns[1:]: 
         names.append(column['name']) 
     return jsonify(names) 
 
 
 # Create a route that returns a list of OTU descriptions
 @app.route("/otu") 
 def description(): 
     results = session.query(Otu.lowest_taxonomic_unit_found).all() 
     otu_results = [] 
     for result in results: 
         otu_results.append(result[0]) 
     return jsonify(otu_results) 
 

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
     metadict = { 
         "AGE": result[0], 
         "BBTYPE": result[1], 
         "ETHNICITY": result[2], 
         "GENDER": result[3], 
         "LOCATION": result[4], 
         "SAMPLEID": result[5] 
     } 
     return jsonify(metadict) 
 
 
# Create a route for weekly Washing frequency 
@app.route('/wfreq/<sample>') 
def wfreq(sample): 
     sample_id = sample[3:] 
     result = session.query(Metadata.WFREQ,Metadata.SAMPLEID).filter(Metadata.SAMPLEID == sample_id).first() 
     return jsonify(result[0]) 
 
 
 # Create a route for OTU IDs and values per sample 
 @app.route('/samples/<sample>') 
 def samp(sample): 
     sample_id_query = f"Samples.{sample}" 
     results = session.query(Samples.otu_id, sample_id_query).order_by(desc(sample_id_query)) 
     sampdict = {"otu_ids": [result[0] for result in results], "sample_values": [result[1] for result in results]} 
     return jsonify(sampdict) 
 
 
 
 
 if __name__ == '__main__': 
    app.run() 
