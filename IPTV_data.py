import os
import datetime
import mysql.connector
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


# reading data from a file config.cfg
def read_db_config(filename='config.cfg', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)
 
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return db


# file modification read date
def modification_date(filename):
    time = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(time)


# data read request
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e :
        print(f"The error '{e}' occurred")


# execution request
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


# search function
def func_search(ext):
    result = list()
    for file in os.listdir("."):
        if file.endswith(ext):
            result.append(file)
    return result


if __name__ == '__main__':
    
    # database connections
    db_config = read_db_config()
    try:
        connection = MySQLConnection(**db_config)

    except Error as e :
        print(f"The error '{e}' occurred")
        raise

    # create table channels_name
    query = """
    CREATE TABLE IF NOT EXISTS channels_name (
    id_channel INTEGER NOT NULL AUTO_INCREMENT,
    name_channel VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_channel),
    UNIQUE(name_channel)
    )
    """
    execute_query(connection, query)

    # create table data_video
    query = """
    CREATE TABLE IF NOT EXISTS data_video (
    id_video INTEGER AUTO_INCREMENT,
    name_video VARCHAR(30) NOT NULL,
    id_channel_f INTEGER NOT NULL,
    sum_error INTEGER,
    date TIMESTAMP,
    PRIMARY KEY (id_video),
    FOREIGN KEY (id_channel_f) REFERENCES channels_name (id_channel)
    )
    """
    execute_query(connection, query)

    # search for errors in the file
    str_error = (f'Error while decoding stream {chr(35)}0:1: Invalid data found when processing input' + '\n')

    # search function .ts
    files_ts = func_search(".ts")

    # file analysis module for errors
    for file in files_ts :
        sum_error = 0

        # name_video check request
        query =f"""
        SELECT name_video, date
        FROM data_video 
        WHERE name_video = '{file}' AND date = '{modification_date(file)}'
        """
        select_name_video = execute_read_query(connection, query)

        # check for recurrences by name_video
        if len(select_name_video) == 0:
            command = f'ffmpeg -v error -i {file} -map 0:1 -f null - 2>{file}.log'
            os.system(command)

            # open file for reading
            file_log = f"{file}.log"
            open_file = open(file_log,'r')

            # error counter
            for str_log in open_file :
                if str_log == str_error :
                    sum_error = sum_error+1

            # file name announcement
            name_channel = file.split('_')

            # request to check the channel name
            query = f"""
            SELECT id_channel 
            FROM channels_name 
            WHERE name_channel = '{name_channel[0]}'
            """
            select_id_channel = execute_read_query(connection, query)

            # entering data into a table channels_name with validation
            if len(select_id_channel) == 0 :
                query = f"""
                INSERT INTO
                channels_name (name_channel)
                VALUES
                ('{name_channel[0]}');
                """
                execute_query(connection, query)

                query = f"""
                SELECT id_channel
                FROM channels_name 
                WHERE name_channel = '{name_channel[0]}'
                """
                select_id_channel = execute_read_query(connection, query)

            # entering data into the table date_video
            query = f"""
            INSERT INTO
            data_video (name_video, id_channel_f, sum_error, date)
            VALUES
            ('{file}', '{select_id_channel[0][0]}', '{sum_error}', '{modification_date(file)}');
            """
            execute_query(connection, query)

        else:
            continue

    # disconnecting from the database
    connection.close()