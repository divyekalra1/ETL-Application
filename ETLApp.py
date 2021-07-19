'''
Importing all required Files and libraries
'''
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
import dt as DATETIME
import re   

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
''' 
    A pandas dataframe is used to import data from a csv file downloaded from kaggle to an sqlite3 database file present in the same 
    directory
''' 
config = {}
filter_names = ["checkNull", "checkUpper", "checkLower", "checkProperCase", "stripSpaces", "checkEmail", "checkDateTime", "checkPhoneNumber"]
num_filters = len(filter_names)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler("Logged_Data.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def main():
    Base = declarative_base() 
    '''
    echo = True is required if you want to see the commands SQLAlchemy is sending to the databse. Set it to False if it's not required
    '''
    engine = create_engine('sqlite:///ETL-database.db', echo = True) 
    logger.info("Database Created")
    sqlite_connection = engine.connect() # sqlite3 connection initialised
    script_dir = os.path.dirname(__file__) # Retrieved the relativ path of the current directory i.e. ETL-Application
    directory = Path(script_dir + "Target_Data")  # Starts looking for new files in the Target_Data directory
    old_path = Path() # Empty generator object
    while True:
        if not keyboard.is_pressed('c'):  
            time, file_path = max((f.stat().st_mtime, f) for f in directory.iterdir())
            if not file_path == old_path:
                global df
                print(file_path.suffix)
                df = checkformat(file_path) #Checking for the format of the file and reading it into a pandas dataframe
                sqlite_table = f"{file_path.stem}" #Name for the table being created from a new data file  
                # checking if config file exists and create a config file according to the datafile in case it doesn't exist
                rewrite_choice = createConfig(file_path.stem, file_path.suffix)

                if rewrite_choice == 1: # continue with existing config file
                    print("Continuing with same config file")
                    logger.info("Continuing with an existing config file")
                else:
                    while (1):          # waiting for user to make changes in config file
                        character = input(".json file configured ? [Y/y]  :")
                        if character == 'Y' or character == 'y':
                            break
                    logger.info("Received response from user to proceed with transformation")

                # loads appropriate config file corresponding to the incoming file
                script_dir = os.path.dirname(__file__)
                rel_path = "configs/" + file_path.stem + ".json" 
                abs_file_path = os.path.join(script_dir, rel_path)
                try:
                    with open(abs_file_path, 'r') as config_file:
                        config = json.load(config_file)
                except:
                    logger.exception(f"unable to load {rel_path}")
                    print(f"unable to load {rel_path}")

                # applying filters as specified in config file
                for i in range(config['num_columns']):
                    filter_list = config['columns'][i]['filters'].split(',')    # creates a list of filters to be applied
                    for str in filter_list:
                        str = str.strip()                                       # isolates filter name string, strips spaces
                        try:
                            filterSelect(str, config['columns'][i]['name'])
                            if str != "":
                                logger.info(f"{str} filter applied to column \"{config['columns'][i]['name']}\"")
                            else :
                                logger.info(f"No filter applied to column \"{config['columns'][i]['name']}\"")
                        except:
                            logger.exception(f"{str} filter FAILED to apply to column \"{config['columns'][i]['name']}\"")

                db_action_mode = 'append'
                # LOADING
                try:
                    check = engine.has_table(sqlite_table)
                    if config["overwrite"].lower == "true":
                        db_action_mode = 'replace'
                    df.to_sql(sqlite_table, sqlite_connection, index_label='id', if_exists=db_action_mode) # Exporting the validated data to an SQL table
                    logger.info(f"Table {sqlite_table} created")
                except ValueError as ve: # Raise ValueError if table already exists
                    print(ve)
                old_path = file_path # overwrite old path with current path
        else:
            break
    Base.metadata.create_all(engine) #Issue CREATE TABLE statement
    sqlite_connection.close() #Close the connection
    engine.dispose() #dispose of the engine
    logger.info("Sqlite3 connection closed and Engine disposed.")
def checkformat(file_path):
    if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
        frame = pd.read_excel(f"Target_Data/{file_path.name}", engine='openpyxl')
    elif file_path.suffix == '.csv':
        frame = pd.read_csv(f"Target_Data/{file_path.name}")
    # json file support to be added later
    # elif file_path.suffix == '.json':
    #     frame = pd.read_json(f"Target_Data/{file_path.name}")
    return frame
    
def createConfig(table_name, filetype):
    '''
    creates config file using the parameters passed, table name, and filetype, and stores the required information as config.json
    the user can now edit config.json with the appropriate filters to apply on the columns
    returns 1 if existing config file of the same name is found
    returns 0 otherwise
    '''
    print("Checking for existing config file")
    #check if same file exists
    try:
        script_dir = os.path.dirname(__file__)
        directory = Path(script_dir + "configs") 
        str = table_name + ".json"
        for f in directory.iterdir():
            if  str == f.name:
                print("Matching Config Found!")
                return 1
    except:
        logger.exception(f"Ran into an issue when looking for an existing config file {table_name}.json")


    print("\n\t\t\tCreating a new config file(.json)")
    # storing information about the database
    config['table_name'] = table_name
    config["filetype"] = filetype
    config["overwrite"] = "False"
    config['num_columns'] = len(df.columns)
    # Storing column names as list of dictionaries
    config['columns'] = []
    list = df.columns.tolist() 
    for i in range(config["num_columns"]):
        col_name = list[i]

        # leaving space to add filters
        filter_choices = ""

        # adding all fields for this column 
        config['columns'].append({
            'name': col_name,
            'filters': filter_choices
            })

    # saves the JSON file in the configs folder with the same filename as the datafile
    try:
        # getting filepath to open
        script_dir = os.path.dirname(__file__)
        rel_path = "configs/" + table_name + ".json" 
        abs_file_path = os.path.join(script_dir, rel_path)

        # opening the file
        with open(abs_file_path , 'w') as config_file:
            config_file.write(json.dumps(config, indent = 4))

        logger.info(f" {table_name}.json config file saved inside of the configs folder. Ready to be configured with filters")
        print(f" {table_name}.json config file saved inside of the configs folder. Ready to be configured with filters")
    except:
        logger.exception(f"Unable to save {table_name}.json config file in the configs folder")
        print(f"Unable to save {table_name}.json config file in the configs folder")

    return 0


def filterSelect(func_name, column_name):
    '''
    Calls the function whose name is passed in the parameter as a string, and passes in column_name into that function
    '''
    try:
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

        logger.info(f"selectFilter finished calling function {func_name}")
    except:
        logger.exception(f"Unable to call function {func_name}")



def checkNull(column_name):                  
    # INPUT WILL BE FROM CONFIG FILE
    try:
        '''
         This list contains a series of boolean values if the datavalue is NaN it will have True in its corresponding 'i'th 
         position or it wll have False in its corresponding 'i'th position
        '''
        li = df[column_name].isnull().tolist() 
        num = 0 
        lis=[]
        '''empty list which will contain the idices of all the rows which have NaN values '''
        rows = df.shape[0]
        for i in li:
            if i == True:
                lis.append(num)
                logger.info("Error on line " + f"{num+1}\n" + f"{df.iloc[num]}")
            num = num + 1
        print('indices found with null values', lis)
        lis.reverse()
        ''' reverses the list'''

        for j in lis:
            df.drop(index = j, inplace = True)
        logger.info('Sucessfully removed the rows that had NaN in ' + f"{column_name}")    

    except:
        '''
        if the column name provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        print('Column heading specified not present in table')  
        logger.exception(f'Column name "{column_name}" specified not present in table') 
        # LOG THIS INTO .LOG FIlE INSTEAD OF PRINTING


def checkDateTime(column_name):
    listi = df[column_name].tolist()    
    listr = []
    dt = ""
    dd = ""
    i=0
    for row in listi:
        dt,dd = DATETIME.ddt(row)
        i = i + 1
        if dt=="":
            print("Loop ", i)
            listr.append(DATETIME.ddf(dd, listi))
        else:
            pass #Time function to be added 
        #error printed in function the string is errored
    # for row in listr:
         
def checkProperCase(column_name):
    '''
    So if the argumnet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,column_name]) == str:    
                df.loc[i,column_name] = df.loc[i,column_name].title() 
                '''converts the element into title case'''
        logger.info('Successfully converted all the elements in the '+ f"{column_name}" ' to title case')
  
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.info(f'Column name "{column_name}" specified not present in table')

             
def checkUpper(column_name):
    '''
    So if the argumenet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,column_name]) == str:    
                df.loc[i,column_name] = df.loc[i,column_name].upper() 
                '''converts the element into upper case'''
        logger.info('Successfully converted all the elements in the '+ f"{column_name}" ' to upper case')   

           
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        logger.info(f'Column name "{column_name}" specified not present in table')

        
def stripSpaces(column_name):
    '''
    So if the argumnet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,column_name]) == str:    
                df.loc[i,column_name] = df.loc[i,column_name].strip() 
                '''strips the element for empty spaces'''
        logger.info('Successfully stripped for spaces all the elements in the '+ f"{column_name}")  

           
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.info(f'Column name "{column_name}" specified not present in table')
        
def checkLower(column_name):
    '''
    So if the argumnet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,column_name]) == str:    
                df.loc[i,column_name] = df.loc[i,column_name].lower() 
                '''converts the element into lower case'''
        logger.info('Successfully converted all the elements in the '+ f"{column_name}" ' to lower case')        
  
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.info(f'Column name "{column_name}" specified not present in table')

#return the index to the console file if the mail format is wrong
def checkEmail(column_name):                        #function to check validity of the Email
    for i in df[column_name]:
        if (re.search(regex, i)):             #using regex to check all the known domains
            continue
        else:
            flga = 0
            flgb = 0
            for i in df[column_name]:
                num = 0
                if (i == '@'):                #username should atleast have an '@'
                    flga = 1
                if (i == '.' and flga == 1):  #username should atleast have a '.'
                    flgb = 1
            if (flga == 1 and flgb == 1):
                continue
            else:
                logger.info(f"Invalid Email in Column")    #return the index to the console file if the mail format is wrong


def checkPhoneNumber(column_name):   #function to check the format of phone numbers
    for i in df[column_name]:
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
                print("INVALID PHONE NNUMBER  \n",df.index[df[column_name] == i])  #return if the number is invalid
        else:
            print("INVALID PHONE NNUMBER \n",df.index[df[column_name] == i])


if __name__ == "__main__":
   main()