from sqlalchemy import Column
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from pathlib import Path
import keyboard
import os
import json
import logging

#import vippultime as vippul
''' 
    A pandas dataframe is used to import data from a csv file downloaded from kaggle to an sqlite3 database file present in the same 
    directory
''' 
config = {}
filter_names = ["checkNull", "checkUpper", "checkLower", "checkProperCase", "stripSpaces", "checkEmail", "checkDatTime", "checkPhoneNumber"]
num_filters = len(filter_names)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler("Logged_Data.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def main():
   
    Base = declarative_base() 
    print("Creating Database...")
    engine = create_engine('sqlite:///ETL-database.db', echo = True)
    sqlite_connection = engine.connect() #connection definition
    script_dir = os.path.dirname(__file__)
    directory = Path(script_dir + "Target_Data") 
    old_path = Path() # Empty generator object
    while True:
        if not keyboard.is_pressed('c'):  
            time, file_path = max((f.stat().st_mtime, f) for f in directory.iterdir())
            if not file_path == old_path:
                global df
                print(file_path.suffix)
                df = checkformat(file_path) #Checking for the format of the file and reading it into a pandas dataframe
                sqlite_table = f"{file_path.stem}" #Name for the table being created from a new data file  

                rewrite_choice = createConfig(file_path.stem, file_path.suffix, df)
                if rewrite_choice == 1: # continue with existing config file
                    print("Processing data according to existing config file")
                else:
                    while (1):          # waiting for user to make changes in config file
                        character = input("JSON Ready?\n")
                        if character == 'Y' or character == 'y':
                            break
                script_dir = os.path.dirname(__file__)
                rel_path = "configs/" + file_path.stem + ".json" 
                abs_file_path = os.path.join(script_dir, rel_path)
                with open(abs_file_path, 'r') as config_file:
                    config = json.load(config_file)

                for i in range(config['num_columns']):
                    filter_list = config['columns'][i]['filters'].split(',')
                    for str in filter_list:
                        str = str.strip()
                        filterSelect(str, config['columns'][i]['name'])


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


def checkformat(file_path):
    if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
        frame = pd.read_excel(f"Target_Data/{file_path.name}", engine='openpyxl')
    elif file_path.suffix == '.csv':
        frame = pd.read_csv(f"Target_Data/{file_path.name}")
    # json file support to be added later
    # elif file_path.suffix == '.json':
    #     frame = pd.read_json(f"Target_Data/{file_path.name}")
    return frame
    
def createConfig(table_name, filetype, df):
    '''
    creates config file using the parameters passed, table name, filetype, and the pandas dataframe df and stores it as config.json
    the user will have to manually edit config.json with the appropriate filters
    returns 1 if doesn't want to reconfigure in case of existing config file
    returns 0 otherwise
    '''
    print("checking for existing config file")
    #check if same file exists
    script_dir = os.path.dirname(__file__)
    directory = Path(script_dir + "configs") 
    str = table_name + ".json"
    for f in directory.iterdir():
        if  str == f.name:
            print("Matching Config Found!")
            return 1
            # print("A config file for this filename already exists\nChoose an option (1 or 2)\n" \
            #         "1) continue with existing config file\n" \
            #         "2) overwrite existing config file and reconfigure\n")
            # rewrite_choice = int(input("Enter Option: "))
            # if rewrite_choice == 2: #wants to rewrite existing config file
            #     continue
            # elif rewrite_choice == 1:
            #     return 1
            # else:
            #     return 1

    print("\n\n\t\t\t\t\t----------CONFIG CREATOR----------\n")

    config['table_name'] = table_name

    config["filetype"] = filetype
    
    config['num_columns'] = len(df.columns)

    config['columns'] = []
    list = df.columns.tolist() 
    for i in range(config["num_columns"]):
        col_name = list[i]

        filter_choices = ""

        config['columns'].append({
            'name': col_name,
            'filters': filter_choices
            })

    script_dir = os.path.dirname(__file__)
    rel_path = "configs/" + table_name + ".json" 
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path , 'w') as config_file:
        config_file.write(json.dumps(config, indent = 4))
    return 0


def filterSelect(func_name, column_name):
    '''
    Calls the function who's name is passed in the parameter as a string
    '''
    if(func_name == "checkNull"):
        checkNull(column_name)
    elif (func_name == "checkUpper"):
        checkUpper(column_name)
    elif (func_name == "checkLower"):
        checkLower(column_name)
    elif (func_name == "checkProperCase"):
        checkProperCase(column_name)
    elif (func_name == "stripSpaces"):
        stripSpaces(column_name)
    elif (func_name == "checkEmail"):
        checkEmail(column_name)
    elif (func_name == "checkDateTime"):
        checkDateTime(column_name)
    elif (func_name == "checkPhoneNumber"):
        checkPhoneNumber(column_name)


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
                logger.info("Error on line " + f"{num+1}\n" + f"{df.iloc[num]}")
                # df.drop(index = num, inplace = True)


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


# def checkDateTime(column_name):
    
#     dt = ""
#     dd = ""
#     for row in df[column_name]:
#         dt,dd = vippul.ddt(row)
#         vippul.ddf(dd, df[column_name])
#         vippul.ft(dt, df[column_name])

def checkProperCase(column_name): #W
    num = 0
    for i in df[column_name]:
        if type(i) == str:
            df.loc[num,column_name] = df.loc[num,column_name].title()
        num = num + 1    
             
def checkUpper(column_name):
    n = 0
    for i in df[column_name]:
        if type(i) == str:
            df.loc[n,column_name] = df.loc[n,column_name].upper()
        n = n + 1  
        
def stripSpaces(column_name): #W
    n = 0
    for i in df[column_name]:
        if type(i) == str:
            df.loc[n,column_name] = df.loc[n,column_name].strip()
        n = n + 1   
        
def checkLower(column_name):
    n = 0
    for i in df[column_name]:
        if type(i) == str:
            df.loc[n,column_name] = df.loc[n,column_name].lower()
        n = n + 1 


def checkPhoneNumber(phone_number):   #function to check the format of phone numbers
    for i in df[phone_number]:
        if(type(i) == str and len(i) == 10):   #if the number is in string format in the dataframe
            pass
        elif(type(i) == int):
            cnt = 0
            while(i):                           #if the number is in integer format in the dataframe
                cnt = cnt +1
                i = i/10
                i = int(i)
            if(cnt == 10):
                pass
            else:
                print("INVALID PHONE NNUMBER  \n",df.index[df[phone_number] == i])  #return if the number is invalid
        else:
            print("INVALID PHONE NNUMBER \n",df.index[df[phone_number] == i])


def checkEmail(Email):                        #function to check validity of the Email
    for i in df[Email]:
        if (re.search(regex, i)):             #using regex to check all the known domains
            continue
        else:
            flga = 0
            flgb = 0
            for i in df[Email]:
                if (i == '@'):                #username should atleast have an '@'
                    flga = 1
                if (i == '.' and flga == 1):  #username should atleast have a '.'
                    flgb = 1
            if (flga == 1 and flgb == 1):
                continue
            else:
                print("Invalid Email in Column Index \n ", df.index[df[Email] == i])    #return the index to the console file if the mail format is wrong


if __name__ == "__main__":
   main()
