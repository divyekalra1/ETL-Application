import pandas as pd
df =pd.read_csv(r"c:\Users\Asus\Desktop\test_data.csv")    # The read_csv() function will convert the exisiting csv database into pandas dataframe

# pandas library is used here as it converts the csv file into pandas dataframe upon which various filters can be applied using pre-defined pandas function

import re   
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'       # This regex is used to define a general format for checking the validity of emails present in the dataframe


def check(email):                                          # using above regex to check if the email is valid or not if valid this function will return 1 if invalid it returns 0
    if (re.search(regex, email)):
        return 1
    else:
        flga = 0
        flgb = 0
        for i in email:
            if (i == '@'):                                 # Checkinhg if email has '@ or not if yes flga is set to be 1
                flga = 1
            if (i == '.' and flga == 1):                   # further it needs to be checked that along with @ the email should contain '.' as well
                flgb = 1
        if (flga == 1 and flgb == 1):                      # if both the conditions are met the function returns 1
            return 1
        else:
            return 0

def func():
    for i in df['Ticket Assigned To In FFS']:
        if(i.isalpha()):
            pass
        else:
            print("Error while naming in incident id: \n",df.loc[df['Ticket Assigned To In FFS'] == i, 'Incident ID'])



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
            
nan_rowsa = df[df['FC Name if the ticket Assigned To'].isnull()]
for i in nan_rowsa['Incident ID']:
	print("Field empty in FC Name if the ticket Assigned To with Incident ID:",i)
	print("\n")


nan_rowsb = df[df['Ticket Accepted/Rejected/Unattended by FC Name'].isnull()]
for i in nan_rowsb['Incident ID']:
	print("Field empty in Ticket Accepted/Rejected/Unattended by FC Name with Incident ID:",i)
	print("\n")

nan_rowsc = df[df['RCIL staff'].isnull()]
for i in nan_rowsc['Incident ID']:
	print("Field empty in RCIL staff with Incident ID:",i)
    	print("\n")


nan_rowsd = df[df['Whether OFC is as per'].isnull()]
for i in nan_rowsd['Incident ID']:
    	print("Field empty in Whether OFC is as per with Incident ID:",i)
   	print("\n")


nan_rowse = df[df['QUAD cable (affected)'].isnull()]
for i in nan_rowse['Incident ID']:
	print("Field empty in QUAD cable (affected) with Incident ID:",i)
	print("\n")
	
	 	    
nan_rowsf = df[df['Lat/long of the fault location'].isnull()]
for i in nan_rowsf['Incident ID']:
	print("Field empty inLat/long of the fault location with Incident ID:",i)
	print("\n")

	    
df['Ticket Assigned To In FFS'] = df['Ticket Assigned To In FFS'].str.lower()

for i in df['PHONE NUMBERS']:
    if(type(i) == str and len(i) == 10):
        pass
    elif(type(i) == int):
        cnt = 0
        while(i):
            cnt = cnt +1
            i = i/10
            i = int(i)
        if(cnt == 10):
            pass
        else:
            print("INVALID PHONE NNUMBER in incident id: \n",df.loc[df['PHONE NUMBERS'] == i, 'Incident ID'])
    else:
        print("INVALID PHONE NNUMBER in incident id: \n",df.loc[df['PHONE NUMBERS'] == i, 'Incident ID'])

    
df = df.fillna(value = 'NULL')            # Every NaN value is converted to string type NULL
string_checker()                          # calling the string checker function to convert the string into title case


if __name__ == "__main__":
    if('Email' in df.columns):
        for i in df['Email']:
            if(check(i) == 0):
                print("INVALID EMAIL!")
    func()
    
