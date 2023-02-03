# ETL-Application
A console based ETL Application designed and developed for Erasmith Technologies Pvt. Ltd. 

## Create and activate a python3 virtual enviroment
```
python3 -m venv env
source env/bin/activate
```

## Install dependencies 
```pip install -r requirements.txt```

## Run the extraction python script
```sudo python3 extraction.py```

## Flow of the App
The way the application works is as follows: first, it checks the ```Target_Data``` folder for any new or unextracted files. If any are found, it extracts them into a global pandas dataframe that can be accessed and modified by all functions. The accepted file formats are .csv, .xls, and .xlsx. The ```Staging``` folder is used to temporarily store the files before they are placed in the ```Target_Data``` folder. After the data has been extracted, the ```createConfig(table_name, filetype)``` function is run to create a JSON file that contains a list of columns and their corresponding string data. The program then prompts the user to confirm that the JSON file is ready. Once the user enters ```y``` or ```Y```, the program iterates through the JSON file, reading the filters to be applied to each column and calling the ```filterSelect(str, config['columns'][i]['name'])``` function. This function is run in another loop that iterates through the filters for each column, passing the column name as an argument to each filter. Once all filters have been applied to all columns, the program creates an SQLite3 database using SQLAlchemy and transfers the data from the pandas dataframe to the SQLite3 table using ```df.to_sql(sqlite_table, sqlite_connection, index_label='id',if_exists=db_action_mode)```. The next file can then be placed in the ```Target_Data``` folder for ETL. Throughout the program, print and logging statements are used to display the progress of the application and any errors that may occur. To handle errors and ensure the flow of the application is not interrupted, try-except statements are used, with ```logging.exception()``` included in the except statement to log any traceback errors for the technical staff to troubleshoot later.
