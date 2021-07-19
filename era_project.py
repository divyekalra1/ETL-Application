import pandas as pd
df =pd.read_csv(r"c:\Users\Asus\Desktop\test_data.csv")    # The read_csv() function will convert the exisiting csv database into pandas dataframe

# pandas library is used here as it converts the csv file into pandas dataframe upon which various filters can be applied using pre-defined pandas function

import re   
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'       # This regex is used to define a general format for checking the validity of emails present in the dataframe


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

    
df = df.fillna(value = 'NULL')            # Every NaN value is converted to string type NULL
string_checker()                          # calling the string checker function to convert the string into title case



