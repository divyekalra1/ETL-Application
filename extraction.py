import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine  # , Column, Integer, String, ForeignKey
#from sqlalchemy.orm import sessionmaker, relationship
import logging  # for logging

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


if __name__ == "__main__":

    print("Creating Database...")
    logger.info('Creating Database')

    # username:passworrd@localhost:5432 after :// before /
    engine = create_engine('sqlite:///ETL-database.db', echo=True)
    sqlite_connection = engine.connect()  # connection definition

    sqlite_table = "kaggle_database"  # Random name for the imported Kaggle database

    Base.metadata.create_all(engine)  # Issue CREATE TABLE statement

    try:
        file_name = "Food_Supply_kcal_Data.csv"  # just name of file
        df = pd.read_csv(file_name)  # pandas reading csv into df
        check = engine.has_table(sqlite_table)  # checking if table exists
        df.to_sql(sqlite_table, sqlite_connection, index_label='id',
                  if_exists='fail')  # Importing data to an sqlite3 database

    except ValueError as ve:  # Raise ValueError if table already exists
        print(ve)
        logger.exception("-Errror-")

    # login all users created
    logger.info(engine.execute("SELECT * FROM users").fetchall())

    # Session()= sessionmaker(bind=engine)

    # session = Session()

    # user = session.query(User).all()

    # session.close()

    sqlite_connection.close()  # Close the connection
    engine.dispose()  # dispose of engine
    logger.info('connection closed and engine disposed')
    logger.info('Extraction completed')
