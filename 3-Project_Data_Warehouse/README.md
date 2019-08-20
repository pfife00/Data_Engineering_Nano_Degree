<h1>Project: Data Warehouse</h1>

<h3>Installation</h3>

The project requires <b> Python 3.x </b> and <a href="http://initd.org/psycopg/docs/" rel="nofollow">Psycopg</a>. 
Pyscopg can be installed on your computer by running the following command in the terminal window:
<br><code>$ pip install psycopg2</code></br>

Also the following module is required from the Python Standard Library:
<ul>

  <li> <a href="https://docs.python.org/3/library/configparser.html" rel="nofollow">configparser</a> </li>

</ul>
If you wish to use Infrastructure as Code (IAC) then the following Python library should be intalled:
<ul>

  <li> <a href="http://pandas.pydata.org" rel="nofollow">Pandas</a> </li>

</ul>

<h3>Project Motivation</h3>
The project's goal is to build an ETL pipeline for a database hosted on AWS redshift. The music streaming startup, Sparkify, has grown their user base and song base and wants to move their processes and data into the cloud. The data currently resides in AWS S3 which contains a directory of JSON logs and a directory of JSON metadata. The objective is to build an ETL pipeline which extracts the data from S3, stages the data in Redshift, and transforms the data into a set of dimensional tables in order for the analytics team to continue finding insights to the data.

<h3>File Descriptions</h3>
The files required to run the function are organized as follows:
<ul>
        <li> create_tables.py - Drops and creates tables from sql_queries.py file. Also loads the parameters stored within the dwh.cfg file. Note, create_tables.py should be run prior to running etl script.</li>
    <li> etl.py - Copies the data from S3 to the staging tables. Inserts the data to the appropriate defined tables.</li>
    <li> sql_queries.py - Contains all the sql queries, which are imported into the etl pipeline and create_tables.py files.</li>
</ul>

<h3> Instructions to Load the JSON files </h3>
The data are contained in two datasets consisting of JSON files. The Song dataset is stored in S3 and can accessed from the link below.
<br>s3://udacity-dend/song_data</br>
<br>The Log dataset is stored in S3 and can be accessed from the link below.</br>
s3://udacity-dend/log_json_path.json
The datasets are copied from S3 to the two staging tables defined within sql_queries.py.
<ul>
    <li> staging_events_table - stores the data from the Log dataset</li>
    <li> staging_songs_table - stores the data from the song dataset.</li>
</ul>
The data are copied from S3 to the staging_events_table by executing the below code within sql_queries.py
<pre>
<codeblock>
staging_events_copy = ("""
    COPY staging_events_table from 's3://udacity-dend/log_data'
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE off
    REGION 'us-west-2'
    JSON 's3://udacity-dend/log_json_path.json';
    """).format(config.get('IAM_ROLE', 'ARN') )
    </codeblock>
</pre>

The data are copied from S3 to the staging_songs_table by executing the below code within sql_queries.py
<pre>
<codeblock>
staging_songs_copy = ("""
    COPY staging_songs_table from 's3://udacity-dend/song_data'
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE off
    REGION 'us-west-2'
    JSON 'auto';
    """).format(config.get('IAM_ROLE', 'arn'))
</codeblock>
</pre>

<h3> Schema </h3>
The datset schema is a star schema optimzied for queries on song play analysis using the song and log datasets. The star schema consists of a Fact Table, songplay_table, and 4 Dimension Tables: user_table, song_table, artist_table, and time_table. 

<ul>
    <li> songplay_table - records in log data associated with song plays i.e. records with page NextSong</li>
    <li> user_table - app users</li>
    <li> song_table - songs in music database</li>
    <li> artist_table - artists in music database</li>
    <li> time_table - timestamps of records in songplays broken down into specific units</li>
</ul>

<h3>Licensing, Authors, Acknowledgments</h3>

Credit should be given to the Million Songs Dataset and Udacity for the data. Licensing for the data can be found at the Million Songs Dataset website <a href="https://labrosa.ee.columbia.edu/millionsong/" rel="nofollow">here</a> </li> and 
Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.