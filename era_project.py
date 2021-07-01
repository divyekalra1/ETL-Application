import pandas as pd
df =pd.read_csv(r"c:\Users\Asus\Desktop\test_data.csv")

import re   
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

def check(email):   
  
    if(re.search(regex,email)):   
        return 1   
    else:   
        return 0

def func():
    for i in df['Ticket Assigned To In FFS']:
        if(i.isalpha()):
            pass
        else:
            print("Error while naming in incident id: \n",df.loc[df['Ticket Assigned To In FFS'] == i, 'Incident ID'])
            
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
    
    




if __name__ == "__main__":
    if('Email' in df.columns):
        for i in df['Email']:
            if(check(i) == 0):
                print("INVALID EMAIL!")
    func();
    