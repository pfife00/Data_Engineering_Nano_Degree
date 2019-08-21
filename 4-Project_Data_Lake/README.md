<h1>Project: Data Lake</h1>

<h3>Installation</h3>

The project requires <b> Python 3.x </b> and <a href="https://pypi.org/project/pyspark/" rel="nofollow">pyspark</a>. 
Pyspark can be installed on your computer by running the following command in the terminal window:
<br><code>$ pip install pyspark</code></br>

Also the following module is required from the Python Standard Library:
<ul>

  <li> <a href="https://docs.python.org/3/library/configparser.html" rel="nofollow">configparser</a> </li>

</ul>


<h3>Project Motivation</h3>
The project's goal is to build an ETL pipeline which reads the data from S3, processes the data within spark and then write the data back to S3. Sparkify has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. 


<h3>Star Schema</h4>
The Star Schema is constructed with the following tables:
<ul>
 Fact Table
    <li>songplays - records in log data associated with song plays i.e. records with page NextSong</li>
    Dimension Tables
    <li>users - users in the app</li>
    <li>songs - songs in music database</li>
    <li>artists - artists in music database</li>
    <li>time - timestamps of records in songplays broken down into specific units</li>
</ul>

<h3>File Descriptions</h3>
The files required to run the function are organized as follows:
<ul>
        <li> etl.py - Copies data from S3, processes the data in spark and then writes the data back to S3</li>
    <li> dl.cfg - Contains AWS credentials.</li>
</ul>

<h3>Licensing, Authors, Acknowledgments</h3>

Credit should be given to the Million Songs Dataset and Udacity for the data. Licensing for the data can be found at the Million Songs Dataset website <a href="https://labrosa.ee.columbia.edu/millionsong/" rel="nofollow">here</a> </li> and 
Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.