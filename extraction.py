import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
import logging
from pathlib import Path
import keyboard

"""creating logger"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler("extraction.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

''' 
    A pandas dataframe is used to import data from a csv file downloaded from kaggle to an sqlite3 database file present in the same 
    directory
'''

Base = declarative_base()


def checkformat(file_path):
    if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
        frame = pd.read_excel(
            f"extracted_files\{file_path.name}", engine='openpyxl')
        logger.info("file format=excel")
    elif file_path.suffix == '.csv':
        frame = pd.read_csv(f"extracted_files\{file_path.name}")
        logger.info("file format=csv")
    # json file support to be added later
    # elif file_path.suffix == '.json':
    #     frame = pd.read_json(f"extracted_files/{file_path.name}")
    return frame


if __name__ == "__main__":
    print("Creating Database...")
    logger.info("CReating dataabse")
    engine = create_engine('sqlite:///ETL-database.db', echo=True)
    sqlite_connection = engine.connect()  # connection definition
    directory = Path(
        "D:\Workdesk\PS-1\ETL-Application\extracted_files")
    old_path = Path()
    while True:
        if not keyboard.is_pressed('c'):
            time, file_path = max((f.stat().st_mtime, f)
                                  for f in directory.iterdir())
            if not file_path == old_path:
                global df
                # Checking for the format of the file and reading it into a pandas dataframe
                df = checkformat(file_path)
                # Name for the table being created from a new data file
                sqlite_table = f"{file_path.stem} Table"
                try:
                    check = engine.has_table(sqlite_table)
                    # Importing data to an sqlite3 database
                    df.to_sql(sqlite_table, sqlite_connection,
                              index_label='id', if_exists='fail')
                except ValueError as ve:  # Raise ValueError if table already exists
                    print(ve)
                    logger.exception("-Error-")
                except:
                    logger.exception("-Error-")
                old_path = file_path

        else:
            break

    Base.metadata.create_all(engine)  # Issue CREATE TABLE statement

    sqlite_connection.close()  # Close the connection
    engine.dispose()  # dispose of the engine
    logger.info('connection closed and engine disposed')
    logger.info('Extraction complete')
