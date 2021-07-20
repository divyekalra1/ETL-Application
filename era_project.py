import pandas as pd
df =pd.read_csv(r"c:\Users\Asus\Desktop\test_data.csv")    # The read_csv() function will convert the exisiting csv database into pandas dataframe

# pandas library is used here as it converts the csv file into pandas dataframe upon which various filters can be applied using pre-defined pandas function

import re   
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'       # This regex is used to define a general format for checking the validity of emails present in the dataframe


def checkEmail(Email):    #function to verify email format
    new_email = df[Email].tolist()     # iterate through the list and check with regular expressions
    for i in new_email:
        if(re.search(regex,i)):   
                continue  
        else:
            flga = 0
            flgb = 0
            for j in new_email[new_email.index(i)]:         #if regex does not match then just check for '@' and '.'
                if(j == '@'):
                    flga =1
                if(j == '.' and flga == 1):
                    flgb = 1
            if(flga == 1 and flgb == 1):
                continue
            else:
                print("Invalid Email in Column Index -> " ,new_email.index(i) , "\n")     #print out the faulty column index for the particular email

def title_case(ch):                       # Converts every string type column into title case
    df[ch] = df[ch].apply(str.title)

# so the below defined function will loop through the columns and check if the elements conatined in the columns are string 
# or not if it is string then it converts the string into proper case format by calling the abover title_case function
       
def string_checker():                     # converts columns headings present in the dataframe to a list of columns
    li = df.columns.tolist()           
    for i in li:
        if type(df.loc[0,i]) == str and df.loc[0,i].find('@') == -1: # checking if the element in the first row is string or not
            title_case(i)                                            #  if yes calls the title_case function that converts every
                                                                     # string type column into title case

def checkPhoneNumber(phone_number):    #function to check phone format
    new_df = df[phone_number].tolist()
    for i in new_df:
        if(type(i) == str and len(i) == 10 and i.isdigit()):    #if the file cell has str type data type then apply these conditions
            pass
        elif(type(i) == int):   #if the data type is int check if it has 10 numbers
            cnt = 0
            while(i):
                cnt = cnt +1
                i = i/10
                i = int(i)
            if(cnt == 10):
                pass
            else:
                print("INVALID PHONE NUMBER in column index ->",new_df.index(i), "\n") #print the faulty column index corresponding to the phone numbers 
        else:
            print("INVALID PHONE NUMBER in column index ->",new_df.index(i), "\n")
            

    
df = df.fillna(value = 'NULL')            # Every NaN value is converted to string type NULL
string_checker()                          # calling the string checker function to convert the string into title case



