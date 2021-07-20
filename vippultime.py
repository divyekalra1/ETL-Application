from datetime import datetime
import logging
import pandas as pd

df=pd.read_csv('demodata.csv')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler("datetime.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

count=0

formatr=""

def ddt(inp):
    """
    date time stirng seperate based on space
    """
    pa=''
    pb=''
    a=''
    b=""
    flag=0
    for i in inp:
        if i==" " and flag==0:
            pa=a
            flag=1
        elif flag==1:
            b=b+str(i)
        else:
            a = a + str(i)
    pb=b
    dd=''
    dt=""
    """
    : only exists in time string so assign parts to dt and dd
    """
    if ":" in pa:
        dt=pa
        dd=pb
    else:
        dt=pb
        dd=pa
    return dt,dd

def ddloop(din):
    """
    seperate date string into a,b,c and flag and form for error handling and information
    """
    a,b,c='','',''
    form=''
    flag=0
    for i in din:
        if i.isdigit() and flag==0:
            a=a+str(i)
        elif i.isdigit() and flag==1:
            b=b+str(i)
        elif i.isdigit() and flag==2:
            c=c+str(i)
        elif i=="-":
            flag+=1
            form='-'
        elif i=="/":
            flag+=1
            form='/'
        elif i=="\\":
            flag+=1
            form='\\'
        elif i=='.':
            flag+=1
            form='.'
        elif flag>2:
            flag=100
            break
        else:
            flag=101
            break
    return flag,a,b,c,form

def ddchecker(list1):
    """
    iterate through wholelist to see in int only string which is month and which date
    """
    global formatr
    i=0
    flag1,fl=0,0
    a1,b1,c1,form='','','',''
    for n in list1:
        i+=1 #row count
        flag1,a1,b1,c1,form=ddloop(n)
        a1int=int(a1)
        b1int=int(b1)
        if len(a1)==2 and flag1==2: #all int only formats with year at last
            #if first part >12 then that is date
            if a1int>12 and len(c1)==2:
                formatr="%d"+form+"%m"+form+"%y"
                break
            elif a1int>12 and len(c1)==4:
                formatr="%d"+form+"%m"+form+"%Y"
                break
            #if second part >12 then that is date
            elif b1int>12 and len(c1)==2 :
                formatr="%m"+form+"%d"+form+"%y"
                break
            elif b1int>12 and len(c1)==4 :
                formatr="%m"+form+"%d"+form+"%Y"
                break
            #if none >12 then could be anything so keeping %d/%m/%y 
            #as default until some entry comes and if not then default
            elif a1int<=12 and len(c1)==2 :
                formatr="%d"+form+"%m"+form+"%y"
            elif a1int<=12 and len(c1)==4 :
                formatr="%d"+form+"%m"+form+"%Y"
            else:
                print("error 1")
        elif len(a1)==4 and b1.isdigit() and len(b1)==2 and c1.isdigit() and len(c1)==2:
            #if year in first part of 4 digits
            formatr='%Y' + form + "%m" +form+ "%d"
        else:
            print('format unknown or mixed format')
            #logger.error('Format unknown of ',n,' at row ',i)
            formatr=0
    return formatr

def ddf(din,column_name):
    """
    dd format checker and converts string into datetime object
    """
    a,b,c="",'',''
    a1,b1,c1="",'',''
    flag,flag1=0,0
    form="" #the symbol used to seperate d m and y

    """
    loop to seperate string into 3 parts
    """
    for i in din:
        if i.isdigit() and flag==0:
            a=a+str(i)
        elif i.isdigit() and flag==1:
            b=b+str(i)
        elif i.isdigit() and flag==2:
            c=c+str(i)
        elif i=="-" or i=="/" or i=="\\" or i==".":
            flag+=1
        elif flag>2:
            print("error2")
            #logger.error('Error in format of ',din,' row ',i)
            flag=100
            break
        else:
            print("error3")
            #logger.error('Error in format of ',din,' row ',i)
            flag=101
            break
    
    print(a,b,c,'-ddf1') #active feedback

    if a.isdigit() and b.isdigit() and c.isdigit() and flag==2 and len(a)==2:
        global count
        if count==0:#count global variable to run the ddchecker once only
            global formatr
            formatr=ddchecker(df[column_name].tolist())
            count=1
        else:
            pass
        try:
            if formatr==0:
                print('format unknown1')
                #logger.error("format unknown")
            else:
                print(formatr," on ",din) #active feedback
                #the following statement replaces string of date with datetime object
                df[column_name] = pd.to_datetime(df[column_name], format=formatr)
                #the statements below are for outputting python datetime object
                #date1=datetime.strptime(din,formatr)
                #return date1
        except :  #how to catch any error
            print("not able to parse date time")
            #logger.exception("not able to parse datetime") #to log the exception
            return None
    elif a.isdigit() and c.isdigit() and flag==2:
        if len(b)==3 and b.isalpha() and len(c)==2:
            formatr="%d"+form+"%M"+form+"%y"
        elif len(b)==3 and b.isalpha() and len(c)==4:
            formatr="%d"+form+"%M"+form+"%Y"
        else:
            print("format not known")
        try:
            print(formatr," on ",a+b+c)
            df[column_name] = pd.to_datetime(df[column_name], format=formatr)
            # date1=datetime.strptime(din,formatr)
            # return date1
        except:
            print("not able to parse date time")
            #logger.exception("not able to parse datetime")
            print('not able to parse into date object')
            return None
    elif  b.isdigit() and c.isdigit() and flag==2:
        if len(a)==3 and a.isalpha() and len(c)==4:
            formatr="%M"+form+"%d"+form+"%Y"
        elif len(a)==3 and a.isalpha() and len(c)==2:
            formatr="%M"+form+"%d"+form+"%y"
        else:
            print('format unknown3')
            formatr=0
            return None
        try:
            print(formatr," on ",a+b+c)
            df[column_name] = pd.to_datetime(df[column_name], format=formatr)
            # date1=datetime.strptime(din,formatr)
            # return date1
        except:
            print("not able to parse date time")
            #logger.exception("not able to parse datetime")
            print('not able to parse into date object')
            return None
    else:
        print('format unknown4')
        formatr=0
        return None

"""
time functions start
"""

def dtloop(tin):
    """
    breaks tin into parts on : or .
    """
    a,b,c,d="",'','',''
    for i in tin:
        if i.isdigit() and flag==0:
            a=a+str(i)
        elif i.isdigit() and flag==1:
            b=b+str(i)
        elif i.isdigit() and flag==2:
            c=c+str(i)
        elif i.isdigit() and flag==3:
            d=d+str(i)
        elif i==":":
            flag+=1
        elif i==".":
            flag+=1
        else:
            print("error")       
    return flag,a,b,c,d

def dtchecker(list1):
    """ checks for hh:mm or mm:ss based on hh time being less than 24 always or even for hour in 12format """
    counta,countb=0,0
    flag1=0
    a1,b1,c1="",'',''
    for i in list1:
        flag1,a1,b1,c1=dtloop(list1)         #>>>>///////???????
        try:
            a1int=int(a1)
            if a1int<=12:
                pass
            elif a1int<=24:
                counta+=1
            elif a1int>24:
                countb+=1
        except:
            print("error format-time")
    if countb==0 and counta==0:
        formatr=1
        return formatr
    elif countb==0:
        formatr=2
        return formatr
    elif counta>0 and countb>0:
        formatr=3
        return formatr
    else:
        print("format mixed can't identify")
        logger.error("format mixed can't identify")
        formatr=0


def dtf(tin,column_name):
    if tin!="":
        pass
    else:
        return 0
    a,b,c,d,a1,b1,c1,d1='','','','','','','',''
    flag,flag1=0,0
    flag,a,b,c,d=dtloop(tin)
    global count
    global formatr
    count=0
    if flag==1 :
        if count==0:    
            formatr=dtchecker(df[column_name].tolist())
            count=1
        else:
            pass
        if formatr==1:
            formatr="%h:%m"
            df[column_name] = pd.to_datetime(df[column_name], format=formatr)
        elif formatr==2:
            formatr="%H:%m"
            df[column_name] = pd.to_datetime(df[column_name], format=formatr)
        elif formatr==3:
            formatr="%m:%s"
            df[column_name] = pd.to_datetime(df[column_name], format=formatr)
    elif flag==2:
        formatr=4
        try:
            formatr="%h:%m:%s"
            df[column_name] = pd.to_datetime(df[column_name], format=formatr)
            #datetime.date.strptime(tin,formatr)
        except:
            logger.exception("not able to parse datetime")
    else:
        print('format unknown')

def main():
    listi=['23/01/2021','21/12/2021','3/12/2021']
    listr=[]
    df=[]
    for i in listi:
        print("loop ",i)
        ddf(i,df[column_name])
    print(listr)

if __name__=="__main__":
    main()
