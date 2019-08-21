import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('AWS', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('AWS', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    """
    Function to initialize spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Function to process the song data through the following steps:
        1) Get filepath to song data file
        2) Read sond data file
        3) Extract columns to create songs table
        4) Write songs table to parquet files partitioned by year and artist
        5) Extract columns to create artists table
        6) Write artists table to parquet files
    """
    # get filepath to song data file
    songdata_schema = StructType([
        StructField("song_id", StringType(), True),
        StructField("year", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("artist_id", StringType(), True),
        StructField("artist_name", StringType(), True),
        StructField("artist_location", StringType(), True),
        StructField("artist_latitude", DoubleType(), True),
        StructField("artist_longitude", DoubleType(), True),
    ])
    song_data = input_data + "song-data/*/*/*/*.json"
    song_data = spark.read.json(input_data, schema=songdata_schema)

    # read song data file
    df = song_data

    # extract columns to create songs table
    artist_id = "artist_id"
    artist_latitude = "artist_latitude"
    artist_location = "artist_location"
    artist_longitude = "artist_longitude"
    artist_name = "artist_name"
    duration = "duration"
    num_songs = "num_songs"
    song_id = "song_id"
    title = "title"
    year = "year"

    #drop duplicates if they exist
    df = df.dropDuplicates('song_id', 'artist_id', 'year', 'duration', 'artist_id',
                           'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude')

    # select needed columns and write songs table to parquet files partitioned by year and artist
    songs_table = df.select('song_id', 'artist_id', 'year', 'duration')
    songs_table.write.partitionBy('year', 'artist_id').parquet(output_data + "songs")

    #select needed columns and and write artists table to parquet files
    artists_table = df.select('artist_id', 'artist_name', 'artist_location', 'artist_latitude',
                              'artist_longitude')
    artists_table.write.parquet(output_data + "artists")


def process_log_data(spark, input_data, output_data):
    """
    This function processes the log data within spark
    """
    # get filepath to log data file
    log_data = os.path.join(input_data,"log_data/*/*/*.json")

    # read log data file
    df = spark.read.json(log_data)

    #drop duplicates if they exist
    df = df.dropDuplicates('ts', 'userId', 'level','sessionId', 'location', 'userAgent', 'firstName', 'lastName', 'gender', 'level')

    # filter by actions for song plays
    df = df['ts', 'userId', 'level','sessionId', 'location', 'userAgent']

    # extract columns for users table
    artists_table = df['userId', 'firstName', 'lastName', 'gender', 'level']

    # write users table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'users.parquet'), 'overwrite')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    df = df.withColumn('timestamp', get_timestamp(df.ts))

    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(int(int(x)/1000)))
    get_week = udf(lambda x: calendar.day_name[x.weekday()])
    get_weekday = udf(lambda x: x.isocalendar()[1])
    get_hour = udf(lambda x: x.hour)
    get_day = udf(lambda x : x.day)
    get_year = udf(lambda x: x.year)
    get_month = udf(lambda x: x.month)

    df = df.withColumn('start_time', get_datetime(df.ts))
    df = df.withColumn('hour', get_hour(df.start_time))
    df = df.withColumn('day', get_day(df.start_time))
    df = df.withColumn('week', get_week(df.start_time))
    df = df.withColumn('month', get_month(df.start_time))
    df = df.withColumn('year', get_year(df.start_time))
    df = df.withColumn('weekday', get_weekday(df.start_time))

    # extract columns to create time table
    time_table = df['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']

    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'time.parquet'), 'overwrite')

    # read in song data to use for songplays table
    song_df = spark.read.parquet("songs.parquet")

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = df.join(song_df, song_df.title == df.song)
    songplays_table = df['start_time', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent']
    songplays_table.select(monotonically_increasing_id().alias('songplay_id')).collect()

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year","month").parquet(output_data+"songplays")

def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
