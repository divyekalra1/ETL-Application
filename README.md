# ETL-Application
A console based ETL Application developed for Erasmith Technologies Pvt. Ltd. 

## Create and activate a python3 virtual enviroment
```
python3 -m venv env
source env/bin/activate
```

## Install dependencies 
```pip install -r requirements.txt```

## Run the extraction python script
```sudo python3 extraction.py```


Extraction: The data has been downloaded from public platform Kaggle, the file used for extraction was originally formatted as .csv/.xlsx:
https://www.kaggle.com/mariaren/covid19-healthy-diet-dataset?select=Food_Supply_kcal_Data.csv
https://www.kaggle.com/varpit94/goldman-sachs-stock-data-updated-till-1jul2021

The .csv file is then read into a Pandas data frame and an SQLAlchemy connection is used along with it to import the data into an sqlite3 database.

Link to the google drive for this project : https://drive.google.com/drive/folders/1Stl16Z5i03GDCxKczD-IjtOqF5IMXsk2?usp=sharing

#date formats supported
Date
#char and int:-
dd mmm yy
dd mmm yyyy
mmm dd yy
mmm dd yyyy

#int only:-
mm dd yy
mm dd yyyy
dd mm yy
dd mm yyyy
yyyy mm dd
