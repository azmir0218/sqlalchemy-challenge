# SQLAlchemy - Surfs Up!
## Objective
To obtain Hawaii weather information for vacation purposes by performing basic climate analysis and data exploration using available climate database. 

## Steps taken to complete:

* Used SQLAlchemy `create_engine` to connect to sqlite database.

* Used SQLAlchemy `automap_base()` to reflect tables into classes and save a reference to those classes called `Station` and `Measurement`.

* Linked Python to the database by creating an SQLAlchemy session.

### Precipitation Analysis

* Started by finding the most recent date in the data set.

* Using this date, retrieved the last 12 months of precipitation data by querying the 12 preceding months of data. Loaded the query results into a Pandas DataFrame and plotted the results using the DataFrame plot method. Printed the summary statistics for the precipitation data. 

### Station Analysis
* Designed various queries such as : query to calculate the total number of stations in the dataset, query to find the most active stations, query to retrieve the last 12 months of temperature observations. 
* Plotted the results
## Step 2 - Climate App

 Designed a Flask API based on the queries that have just been developed.Used Flask to create the routes for the webpage. 

### Temperature Analysis I

* Was there a meaningful difference between the temperature in, for example, June and December? 
* Used Pandas to perform data analysis on temperature across all available years in the dataset. 

##Tools used:
SQLAlchemy, Pandas, Matplotlib
