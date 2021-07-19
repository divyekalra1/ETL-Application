from datetime import datetime
import logging

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
    i=0
    flag1,fl=0,0
    a1,b1,c1,form='','','',''
    for n in list1:
        i+=1 #row count
        flag1,a1,b1,c1,form=ddloop(n)
        a1int=int(a1)
        b1int=int(b1)
        if len(a1)==2 and flag1==2: #all int only formats with year at last
            if a1int>12 and len(c1)==2:
                formatr="%m"+form+"%d"+form+"%y"
                break
            elif a1int>12 and len(c1)==4:
                formatr="%m"+form+"%d"+form+"%Y"
                break
            elif b1int>12 and len(c1)==2 :
                formatr="%m"+form+"%d"+form+"%y"
                break
            elif b1int>12 and len(c1)==4 :
                formatr="%m"+form+"%d"+form+"%Y"
                break
            elif a1int<=12 and len(c1)==2 :
                formatr="%d"+form+"%m"+form+"%y"
            elif a1int<=12 and len(c1)==4 :
                formatr="%d"+form+"%m"+form+"%Y"
            else:
                print("error 1")
        elif len(a1)==4 and b1.isdigit() and len(b1)==2 and c1.isdigit() and len(c1)==2:
            formatr='%Y' + form + "%m" +form+ "%d"
        else:
            print('format unknown or mixed format')
            #logger.error('Format unknown of ',n,' at row ',i)
            formatr=0
    return formatr

def ddf(din,list1):
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
            formatr=ddchecker(list1)
            count=1
        else:
            pass
        try:
            if formatr==0:
                print('format unknown1')
                #logger.error("format unknown")
            else:
                print(formatr," on ",din) #active feedback
                date1=datetime.strptime(din,formatr)
                return date1
        except e:
            print(e)
            #logger.exception("not able to parse datetime")
            return None
    elif a.isdigit() and c.isdigit() and flag==2:
        if len(b)==3 and b.isalpha() and len(c)==2:
            formatr="%d"+form+"%M"+form+"%y"
        elif len(b)==3 and b.isalpha() and len(c)==4:
            formatr="%d"+form+"%M"+form+"%Y"
        try:
            print(formatr," on ",a+b+c)
            date1=datetime.strptime(a+b+c,formatr)
            return date1
        except:
            #logger.exception("not able to parse datetime")
            print('error5')
            return None
    elif a.isdigit() and b.isdigit() and c.isdigit() and flag==2:
        if len(a)==4:
            formatr="%Y"+form+"%M"+form+"%d"
        elif len(a)==2:
            formatr="%y"+form+"%M"+form+"%d"
        else:
            print('format unknown2')
            return None
        try:
            print(formatr," on ",din)
            date1=datetime.strptime(din,formatr)
            return date1
        except:
            #logger.exception("not able to parse datetime")
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

    else:
        print('format unknown4')
        formatr=0
        return None

# def dtloop(tin):
#     for i in tin:
#         if i.isdigit() and flag==0:
#             a=a+str(i)
#         elif i.isdigit() and flag==1:
#             b=b+str(i)
#         elif i.isdigit() and flag==2:
#             c=c+str(i)
#         elif i.isdigit() and flag==3:
#             d=d+str(i)
#         elif i==":" :
#             flag+=1
#         elif i==".":
#             flag+=1
#         else:
#             print("error")       
#     return flag,a,b,c

# def dtchecker(list1):
#     for i in list1:
#         flag1,a1,b1,c1,form1=df(tin)
#         try:
#             a1int=int(a1)
#             if a1int<=24:
#                 pass
#             elif a1int>24:
#                 count+=1
#         except:
#             print("error format-time")
#     if count==0:
#         formatr=1
#         return formatr
#     elif count==list1.len():
#         formatr=2
#         return formatr
#     else:
#         print("format mixed can't identify")
#         logger.error("format mixed can't identify")


# def dtf(tin,list1):
#     if tin!=None:
#         pass
#     else:
#         return 0
#     a,b,c,a1,b1,c1=""
#     flag,flag1=0
#     form,form1=0
#     flag,a,b,c,form=df(tin)
#     if flag==1:
#         if count==0:
#             formatr=dtchecker(list1)
#         if form==1:
#             pass
#         else:
#             print('format unknown')
#         #for i in list1:
#             #read for a to be mm or dd according to m being 1-12
#         date1=datetime.date.strptime(a+b+c,format)
#     elif flag==2:
#         formatr=3
#         try:
#             datetime.date.strptime(a+b+c,formatr)
#         except:
#             logger.exception("not able to parse datetime")
#     else:
#         print('format unknown')

def main():
    listi=['12/23/2021','11/12/2021','12/12/2021']
    listr=[]
    for i in listi:
        print("loop ",i)
        listr.append(ddf(i,listi))
    print(listr)

if __name__=="__main__":
    main()
