import os
import sqlite3

from tqdm import tqdm
from datetime import datetime

import logging
logger = logging.getLogger("DataBase_Manager")
logging.basicConfig(
    filename='logs.log',
    filemode='a',
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger.addHandler(logging.StreamHandler())

class DataBase_Manager:

    conn = None
    cursor = None
    db_name = 'weather_data.db'

    @classmethod
    def get_connection(cls):
        if cls.conn:
            return cls.conn
        cls.conn = sqlite3.connect(cls.db_name)
        logger.info('creating connection!!!')
        return cls.conn
    
    @classmethod
    def get_cursor(cls):
        if cls.cursor:
            return cls.cursor
        cls.cursor = cls.get_connection().cursor()
        return cls.cursor
    
    @classmethod
    def close_connection(cls):
        if cls.conn:
            cls.conn.close()
            cls.conn = None
            cls.cursor = None

    @classmethod
    def database_creation(cls):

        cursor = cls.get_cursor()
        
        cursor.execute(
            """
                    CREATE TABLE IF NOT EXISTS weather_data_records (
                            Station_id TEXT , 
                            date TEXT, 
                            max_temperature INTEGER , 
                            min_temperature INTEGER, 
                            precipitation INTEGER,
                            PRIMARY KEY (date, Station_id)
                    )
                    """
        )

        cursor.execute(
            """
                       CREATE TABLE IF NOT EXISTS weather_data_stats (
                            Station_id TEXT,
                            avg_max_temperature INTEGER , 
                            avg_min_temperature INTEGER, 
                            total_precipitation INTEGER,
                            PRIMARY KEY (Station_id)
                       )
                    """
        )

    @classmethod
    def read_file(cls, file_name=None):
        start = datetime.now()
        logger.info(f'Data ingestion started at: {start}')

        if file_name:
            wx_data_path = file_name
            for file in tqdm(os.listdir(wx_data_path)):
                if file.endswith(".txt"):
                    with open(f"{wx_data_path}/{file}") as f:
                        for line in f:
                            record = line.strip().split("\t")
                            record.insert(0, file[:-4])
                            cls.data_ingestion(record)
            
            cls.clean_data()
            cls.conn.commit()
            
        end = datetime.now()
        logger.info(f'Data ingestion completed at: {end}, total time taken {(end-start).seconds} seconds')
        

    @classmethod
    def data_ingestion(cls, record):

        cls.get_cursor().execute(
            "INSERT OR IGNORE INTO weather_data_records \
                (Station_id, date, max_temperature, min_temperature, precipitation) \
                    VALUES (?, ?, ?, ?, ?)",
            record,
        )

    @classmethod
    def clean_data(cls):
        cls.get_cursor().execute(
                """
                UPDATE weather_data_records
                SET
                    max_temperature = CASE WHEN max_temperature = -9999 THEN 0 ELSE max_temperature END,
                    min_temperature = CASE WHEN min_temperature = -9999 THEN 0 ELSE min_temperature END,
                    precipitation = CASE WHEN precipitation = -9999 THEN 0 ELSE precipitation END
                """
            )

    @classmethod
    def data_analysis(cls):
        cls.get_cursor().execute(
            """
                            INSERT OR IGNORE INTO weather_data_stats (
                                Station_id,
                                avg_max_temperature,
                                avg_min_temperature,
                                total_precipitation
                            )
                            SELECT
                                Station_id,
                                AVG(CAST(max_temperature AS REAL)) AS average_max_temperature,
                                AVG(CAST(min_temperature AS REAL)) AS average_min_temperature,
                                SUM(CAST(precipitation AS REAL)) AS total_precipitation
                            FROM weather_data_records Group By Station_id
                        """
        )
        cls.get_connection().commit()


if __name__ == "__main__":
    DataBase_Manager.database_creation()
    DataBase_Manager.read_file("wx_data")
    DataBase_Manager.data_analysis()
