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

The way the application flows or runs is first of all when it is run it checks in a given folder Target_Data if any new or unextracted files are left then extracts it into a pandas dataframe which is kept global so each function can access and modify it with the file formats accepted being .csv, .xls and .xlsx.The Staging folder is to hold the files before putting them in the Target_Data folder. 
After the data is extracted into a pandas dataframe the ```def createConfig(table_name, filetype)``` function is run creating a json file which contains the list of column with string opposite to it to write the functions to be applied on that column and after creating json file, program asks if json file is ready, once the user has filled the json file he can enter 'y' or 'Y' in the prompt and press enter.
After this program runs a loop iterating through json file and reading filters to be applied on each column and calling ```filterSelect(str, config['columns'][i]['name'])``` function which is run in another loop iterating through the filters to be applied on the column which calls each filter giving them the column name as the argument.
Once all filters on all columns are applied the program creates a sqlalchemy engine and creates an sqlite3 database and uses ```df.to_sql(sqlite_table, sqlite_connection, index_label='id',if_exists=db_action_mode)``` to transfer the data in pandas dataframe to the sqlite3 table. 
Then, the next file can be put into the Target_Data folder for ETL.
Throughout the program print and logging statements are present showing the progress of application and errors occuring.
To handle the errors and not letting them stop the flow of application we have used try and except statements in every place where there is a scope of error and used ```logging.exception()``` in the except statement to log the traceback of error so the technical staff can trace the error later on