
<h1>Data Modeling with Postgres Project</h1>

<h3>Installation</h3>

The project requires <b> Python 3.x </b> and the following Python libraries installed:
<ul>

  <li> <a href="https://wiki.postgresql.org/wiki/Main_Page" rel="nofollow">psycopg2</a> </li>
  <li> <a href="http://pandas.pydata.org" rel="nofollow">Pandas</a> </li>

</ul>

<h3> Project Motivation </h3>

The project's goal is to create a database schema and ETL pipeline in order for Sparkify to analyze the data they've been collecting on songs and user activity on their new music streaming app. The data is stored in JSON format consisting of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. 

<h3> File Descriptions </h3>

The files required to run the function are organized as followed:
<ul>
    <li> data - Folder containing project data</li>
    <li> etl.ipynb - Jupyter Notebook to assist in creating etl pipeline</li>
    <li> test.ipynb - Jupyter Notebook to test that the sql queries in the sql_queries.py file were property set up by testing if the table exists and that data has been properly inserted</li>
    <li> create_tables.py - Drops and creates tables from sql_queries.py file. Note, this file should be run prior to running etl script.</li>
    <li> etl.py - Reads and processes files from song_data and log_data and loads them in into the tables.</li>
    <li> sql_queries.py - Contains all the sql queries, which are imported into the etl pipeline and create_tables.py files.</li>
</ul>


<h3> Instructions to Load the JSON files </h3>

The JSON files can be loaded by using the following code

<code> df = pd.read_json(filepath, lines=True)</code>


<h3> Schema </h3>
The song play analysis schema is a star schema optimzied for queries on song play analysis using the song and log datasets. The star schema consists of a Fact Table, songplays, and 4 Dimension Tables: users, songs, artists, and time. 

<ul>
    <li> songplays - records in log data associated with song plays i.e. records with page NextSong</li>
    <li> users - users in the app</li>
    <li> songs - songs in music database</li>
    <li> artists - artists in music database</li>
    <li> etl.py - Reads and processes files from song_data and log_data and loads them in into the tables.</li>
    <li> time - timestamps of records in songplays broken down into specific units</li>
</ul>


<h3>Licensing, Authors, Acknowledgments</h3>

Credit should be given to the Million Songs Dataset and Udacity for the data. Licensing for the data can be found at the Million Songs Dataset website <a href="https://labrosa.ee.columbia.edu/millionsong/" rel="nofollow">here</a> </li> and 
Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.
