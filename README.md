# ETL-Application
A console based ETL Application developed for Erasmith Technologies Pvt. Ltd. 
###Create and activate a python3 virtual enviroment
``` 
    python3 -m venv env 
    source env/bin/activate
```

###Install dependencies 
```pip install -r requirements.txt```

###Run the extraction python script
```python3 extraction.py```


Extraction: The data has been downloaded from public platform Kaggle, the file used for extraction was originally formatted as .csv:
https://www.kaggle.com/mariaren/covid19-healthy-diet-dataset?select=Food_Supply_kcal_Data.csv

The .csv file is then read into a Pandas data frame and an SQLAlchemy connection is used along with it to import the data into an sqlite3 database.
