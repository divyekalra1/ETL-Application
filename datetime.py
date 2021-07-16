import datetime

def dtsep(in):
    pa,pb=''
    a,b=""
    flag=0
    for i in in:
        if i==" " and flag==0:
            pa=a
            flag=1
        elif flag==1:
            b=b+str(i)
        else:
            a = a + str(i)
    pb=b
    dd,dt=""
    if ":" in pa:
        dt=pa
        dd=pb
    else:
        dt=pb
        dd=pa
    return dt,dd

def dd(din,list1):
    a,b,c=""
    flag=0
    for i in din:
        if i.isdigit() and flag==0:
            a=a+str(i)
        elif i.isdigit() and flag==1:
            b=b+str(i)
        elif i.isdigit() and flag==2:
            c=c+str(i)
        elif i=="-" or i=="/" or i=="\\" or " ":
            flag+=1
        elif flag>2:
            print("error")
        else:
            print("error")            
    if a.isdigit() and b.isdigit() and c.isdigit():
        format=1
        for 
        datetime.date.strptime(a+b+c,'-type fomat in strptime docum-')
    elif a.isdigit() and c.isdigit():
        format=2
        datetime.date.strptime(a+b+c,'-type fomat in strptime docum-')
    elif b.isdigit() and c.isdigit():
        format=3
        datetime.date.strptime(a+b+c,'-type fomat in strptime docum-')
    else:
        print('format unknown')
        

def ft(tin,list1):
    a,b,c=""
    flag=0
    for i in tin:
        if i.isdigit() and flag==0:
            a=a+str(i)
        elif i.isdigit() and flag==1:
            b=b+str(i)
        elif i.isdigit() and flag==2:
            c=c+str(i)
        elif i.isdigit() and flag==3:
            d=d+str(i)
        elif i==":" or ".":
            flag+=1
        else:
            print("error")            
    if c!="" and d!="":
        format=1
        for i in list1:
            #read for a to be mm or dd according to m being 1-12
        datetime.date.strptime(a+b+c,'-type fomat in strptime docum-')
    elif d!="":
        format=2
        datetime.date.strptime(a+b+c,'-type fomat in strptime docum-')
    else:
        print('format unknown')
        

def main():
