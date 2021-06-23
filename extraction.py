from sqlalchemy import Column
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

''' 
    A pandas dataframe is used to import data from a csv file downloaded from kaggle to an sqlite3 database file present in the same 
    directory
''' 

Base = declarative_base() 


if __name__ == "__main__":
    
    print("Creating Database...")
    engine = create_engine('sqlite:///ETL-database.db', echo = True)
    sqlite_connection = engine.connect() #connection definition
    sqlite_table = "kaggle_database" #Random name for the imported Kaggle database

    Base.metadata.create_all(engine) #Issue CREATE TABLE statement
    
    try:
        file_name = "Food_Supply_kcal_Data.csv" 
        df = pd.read_csv(file_name)
        check = engine.has_table(sqlite_table)
        df.to_sql(sqlite_table, sqlite_connection, index_label='id', if_exists='fail') #Importing data to an sqlite3 database
        
    except ValueError as ve: # Raise ValueError if table already exists
        print(ve)
    
    sqlite_connection.close() #Close the connection
    engine.dispose() #dispose of engine