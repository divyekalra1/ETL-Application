import pandas as pd
import pyodbc

data = pd.read_csv('Food_Supply_kcal_Data.csv')
x = []
n = input("no of columns")
for i in range(n):
    x[i] = input()

listofcolumns = list(x)
df = pd.DataFrame(data, columns=listofcolumns)

print(df)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=RON\SQLEXPRESS;'
                      'Database=TestDB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute(
    'CREATE TABLE people_info (Name nvarchar(50), Country nvarchar(50), Age int)')

"""to put pandas dataframe in """

for row in df.itertuples():
    cursor.execute('''
                INSERT INTO TestDB.dbo.people_info (Name, Country, Age)
                VALUES (?,?,?)
                ''',
                   row.Name,
                   row.Country,
                   row.Age
                   )
conn.commit()
