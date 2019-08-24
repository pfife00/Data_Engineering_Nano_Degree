import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')


# DROP TABLES

#"CREATE SCHEMA IF NOT EXISTS dist;"
#"SET search_path TO dist;"

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song_table;"
artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
time_table_drop = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES

#Create staging table from Log Dataset
staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events_table (
        event_id INT IDENTITY(0,1) NOT NULL,
        artist_name VARCHAR(255),
        auth VARCHAR(20),
        first_name VARCHAR(255),
        gender VARCHAR(1),
        item_in_session INTEGER,
        last_name VARCHAR(255),
        length DOUBLE PRECISION,
        level VARCHAR(50),
        location VARCHAR(255),
        method VARCHAR(5),
        page VARCHAR(50),
        registration VARCHAR(50),
        session_id BIGINT,
        song_title VARCHAR(255),
        status INTEGER,
        ts VARCHAR(50),
        user_agent TEXT,
        user_id VARCHAR(255),
        PRIMARY KEY (event_id)
        );
    """)

#Create staging table from Song Dataset
staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs_table (
        num_songs INTEGER,
        artist_id VARCHAR(100) NOT NULL,
        artist_latitude DOUBLE PRECISION,
        artist_longitude DOUBLE PRECISION,
        artist_location VARCHAR(255),
        artist_name VARCHAR(255),
        song_id VARCHAR(100) NOT NULL,
        title VARCHAR(255),
        duration DOUBLE PRECISION,
        year INTEGER,
        PRIMARY KEY (song_id)
        );
    """)

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay_table (
        songplay_id INT IDENTITY(0,1) NOT NULL,
        start_time TIMESTAMP,
        user_id VARCHAR(255) NOT NULL,
        level VARCHAR(4),
        song_id VARCHAR(100) NOT NULL,
        artist_id VARCHAR(100) NOT NULL,
        session_id BIGINT NOT NULL,
        location VARCHAR(200),
        user_agent TEXT,
        PRIMARY KEY(songplay_id)
        );
    """)

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS user_table (
        user_id VARCHAR(255),
        first_name VARCHAR(100),
        last_name VARCHAR(255),
        gender VARCHAR(1),
        level VARCHAR(4),
        PRIMARY KEY(user_id)
        );
    """)

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_table (
        song_id VARCHAR(100) NOT NULL,
        title VARCHAR(255),
        artist_id VARCHAR(100) NOT NULL,
        year INTEGER,
        duration DOUBLE PRECISION,
        PRIMARY KEY(song_id)
        );
    """)

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist_table (
        artist_id VARCHAR(100) NOT NULL,
        name VARCHAR(255),
        location VARCHAR(255),
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        PRIMARY KEY(artist_id)
        );
    """)

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_table (
        start_time TIMESTAMP,
        hour INTEGER,
        day INTEGER,
        week INTEGER,
        month INTEGER,
        year INTEGER,
        weekday INTEGER,
        PRIMARY KEY(start_time)
        );
    """)

# STAGING TABLES
#'s3://udacity-dend/song_data'
staging_events_copy = ("""
    COPY staging_events_table from 's3://udacity-dend/log_data'
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE off
    REGION 'us-west-2'
    JSON 's3://udacity-dend/log_json_path.json';
    """).format(config.get('IAM_ROLE', 'ARN') )

staging_songs_copy = ("""
    COPY staging_songs_table from 's3://udacity-dend/song_data'
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE off
    REGION 'us-west-2'
    JSON 'auto';
    """).format(config.get('IAM_ROLE', 'arn'))

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay_table (start_time, user_id, level, song_id, artist_id,
                                session_id, location, user_agent)
    SELECT DISTINCT
        TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' as start_time,
        e.user_id,
        e.level,
        s.song_id,
        s.artist_id,
        e.session_id,
        e.location,
        e.user_agent
    FROM staging_events_table e, staging_songs_table s
    WHERE e.page = 'NextSong'
    AND e.song_title = s.title
    AND user_id NOT IN (
        SELECT DISTINCT s.user_id
        FROM songplay_table s
        WHERE s.user_id = user_id
        AND s.start_time = start_time
        AND s.session_id = session_id)
    """)

user_table_insert = ("""
    INSERT INTO user_table (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT
        user_id,
        first_name,
        last_name,
        gender,
        level
    FROM staging_events_table e
    WHERE e.page = 'NextSong'
    AND user_id NOT IN (SELECT DISTINCT user_id FROM user_table)
    """)

song_table_insert = ("""
    INSERT INTO song_table (song_id, title, artist_id, year, duration)
    SELECT DISTINCT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs_table
    WHERE song_id NOT IN (SELECT DISTINCT song_id FROM song_table)
    """)

artist_table_insert = ("""
    INSERT INTO artist_table (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs_table
    WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artist_table)
    """)

time_table_insert = ("""
    INSERT INTO time_table (start_time, hour, day, week, month, year, weekday)
    SELECT
        start_time,
        EXTRACT(hr from start_time) AS hour,
        EXTRACT(d from start_time) AS day,
        EXTRACT(w from start_time) AS week,
        EXTRACT(mon from start_time) AS month,
        EXTRACT(yr from start_time) AS year,
        EXTRACT(weekday from start_time) AS weekday
    FROM (
        SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time
        FROM staging_events_table s
        )
    WHERE start_time NOT IN (SELECT DISTINCT start_time FROM time_table)
    """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
