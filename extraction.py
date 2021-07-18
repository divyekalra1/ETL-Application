from sqlalchemy import Column
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from pathlib import Path
import keyboard
import os
import vippultime as vippul
''' 
    A pandas dataframe is used to import data from a csv file downloaded from kaggle to an sqlite3 database file present in the same 
    directory
''' 
config = {}

def main():
    print("Creating Database...")
    engine = create_engine('sqlite:///ETL-database.db', echo = True)
    sqlite_connection = engine.connect() #connection definition

    #directory = Path("/home/divyekalra/Desktop/ETL-Application/extracted_files") 
    directory = os.cwd()
    old_path = Path() # Empty generator object
    while True:
        if not keyboard.is_pressed('c'):  
            time, file_path = max((f.stat().st_mtime, f) for f in directory.iterdir())
            if not file_path == old_path:
                global df
                print(file_path.suffix)
                df = checkformat(file_path) #Checking for the format of the file and reading it into a pandas dataframe
                # call config and append to config.json with default values and column names etc taking from the new dataframe
                sqlite_table = f"{file_path.stem} Table" #Name for the table being created from a new data file  
                #call config (file_path.stem, file_path.suffix, df)
                createConfig(file_path.stem, file_path.suffix, df)
                while (1):
                    character = input("JSON Ready?\n")
                    if character == 'Y' or character == 'y':
                        break

                with open("config.json", 'r') as config_file:
                    config = json.load(config_file)

                for i in range(config['num_columns']):
                    filter_list = config['columns'][i]['filters'].split(',')
                    for str in filter_list:
                        str = str.strip()
                        filterSelect(str, config['column'][i]['name'])


                # LOADING
                try:
                    check = engine.has_table(sqlite_table)
                    df.to_sql(sqlite_table, sqlite_connection, index_label='id', if_exists='fail') #Importing data to an sqlite3 database
                except ValueError as ve: # Raise ValueError if table already exists
                    print(ve)
                old_path = file_path # overwrite old path with current path
        
        else:
            break
    Base.metadata.create_all(engine) #Issue CREATE TABLE statement
    
    sqlite_connection.close() #Close the connection
    engine.dispose() #dispose of the engine


Base = declarative_base() 
def checkformat(file_path):
    if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
        frame = pd.read_excel(f"extracted_files/{file_path.name}", engine='openpyxl')
    elif file_path.suffix == '.csv':
        frame = pd.read_csv(f"extracted_files/{file_path.name}")
    # json file support to be added later
    # elif file_path.suffix == '.json':
    #     frame = pd.read_json(f"extracted_files/{file_path.name}")
    return frame
    
def createConfig(table_name, filetype, df):
    '''
    creates config file using the parameters passed, table name, filetype, and the pandas dataframe df and stores it as config.json
    the user will have to manually edit config.json with the appropriate filters
    '''
    
    print("\n\n\t\t\t\t\t----------CONFIG CREATOR----------\n")

    config['table_name'] = table_name

    config["filetype"] = filetype
    
    config['num_columns'] = len(df.columns)

    config['columns'] = [] 
    for i in range(len(num_columns)):
        col_name = df.column[i]

        filter_choices = ""

        config['columns'].append({
            'name': col_name,
            'filters': filter_choices
            })

    # script_dir = os.path.dirname(__file__)
    # rel_path = "configs/user_defined/" + config_name + ".json" 
    # abs_file_path = os.path.join(script_dir, rel_path)
    with open(config.json, 'a') as config_file:
        config_file.write(json.dumps(config, indent = 4))


def filterSelect(func_name, column_name):
    '''
    Calls the function who's name is passed in the parameter as a string
    '''
    if(func_name == "checkNull"):           #done
        checkNull(column_name)
    elif (func_name == "checkAllCaps"):
        checkAllCaps(column_name)
    elif (func_name == "checkAllLower"):
        checkAllLower(column_name)
    elif (func_name == "checkProperCase"):            #done
        checkProperCase(column_name)
    elif (func_name == "checkEmail"):
        checkEmail(column_name)
    elif (func_name == "checkDateTime"):           #done
        checkDateTime(column_name)

    


'''
The argument which will be provided in config file will be the column heading, entries of which should not be NULL
So what this function will do is it takes the column heading as argument and checks for NULL values in the function
if there is any NULL values or NaN values present in the column, it will use the logging module and log those warnings into
seperate .log file
'''

def checkNull(column_name):                  
    # INPUT WILL BE FROM CONFIG FILE
    try:
        
        '''
         This list contains a series of boolean values if the datavalue is NaN it will have True in its corresponding 'i'th 
         position or it wll have False in its corresponding 'i'th position
        '''
        
        li = df[column_name].isnull().tolist() 
        num = 0                                
        for i in li:
            if i == True:
                df.drop(index = num, inplace = True)
#                 logging.warning(df.iloc[num])
                # LOG THIS INTO .LOG FIlE INSTEAD OF DROPPING
            num = num + 1
    except:
        
        '''
        if the argument returned is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        print('Column heading specified not present in table')   
        # LOG THIS INTO .LOG FIlE INSTEAD OF PRINTING
        
'''
The below function is called by string_checker to convert the corresponding datavalues into title case.
'''

def title_case(name):
    df[name] = df[name].apply(str.title)

'''
The below function, when called iterates through the column heading of the table and calls the title_case function which wil
convert all the column entries that are of type string into Title Case format.
'''    
'''
Title Case is the type of casing that will have first letter of the string changed to UPPER case and rest of the characters in
the string will be lowered case. Whenever there is space encountered, the next letter encountered will be converted to UPPER
case
'''    

    
def checkProperCase(column_name):
    li = df.columns.tolist()                # converts columns headings present in the dataframe to a list of columns
    for i in li:
        if type(df.loc[0,i]) == str and df.loc[0,i].find('@') == -1:        # checking if the element in the first row is string or not if yes calls the
            title_case(i)                   #title_case function that converts ever    



def checkDateTime(column_name):
    
    dt = ""
    dd = ""
    for row in df[column_name]:
        dt,dd = vippul.ddt(row)
        vippul.ddf(dd, df[column_name])
        vippul.ft(dt, df[column_name])



if __name__ == "__main__":
   main()