'''
The argument which will be provided in config file will be the column heading, entries of which should not be NULL
So what this function will do is it takes the column heading as argument and checks for NULL values in the function
if there is any NULL values or NaN values present in the column, it will use the logging module and log those warnings into
seperate .log file
'''

def null_checker(column_name):                  
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

    
def string_checker():
    li = df.columns.tolist()                # converts columns headings present in the dataframe to a list of columns
    for i in li:
        if type(df.loc[0,i]) == str and df.loc[0,i].find('@') == -1:        # checking if the element in the first row is string or not if yes calls the
            title_case(i)                   #title_case function that converts ever    
        
null_checker(column_name)   # caliing null_checker function
df     

df=df.fillna(value = 'NULL') # This command will convert all NaN values present in the table into NULL string type for
                             # readabilty

string_checker()    # calling string_checker function
df
