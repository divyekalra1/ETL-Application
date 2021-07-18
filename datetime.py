import datetime

def ddt(inp):
    pa,pb=''
    a,b=""
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
    dd,dt=""
    if ":" in pa:
        dt=pa
        dd=pb
    else:
        dt=pb
        dd=pa
    return dt,dd

def dd(din):
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



def ddf(din,list1):
    a,b,c=""
    a1,b1,c1=""
    flag,flag1=0

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
            print("error")
            logger.error('Error in format of ',din,' row ',i)
            flag=100
            break
        else:
            print("error")
            logger.error('Error in format of ',din,' row ',i)
            flag=101
            break

    if a.isdigit() and b.isdigit() and c.isdigit():
        for n in list1:
            flag1,a1,b1,c1,form=dd(n)
            if a1.len()==2:
                if a1>12 and c1.len()==2 and fl==1:
                    formatr="%d"+form+"%m"+form+"%y"
                    fl=1
                elif a1>12 and c1.len()==4 and fl==2:
                    formatr="%d"+form+"%m"+form+"%Y"                
                    fl=2
                elif b1>12 and c1.len()==2 and fl==3:
                    formatr="%m"+form+"%d"+form+"%y"
                    fl=3
                elif a1>12 and c1.len()==4 and fl==4:
                    formatr="%d"+form+"%m"+form+"%Y"
                    fl=4
                else:
                    print('error')
                    flag=100
            elif a1.len()==4:
                formatr='%Y' + form + "%m" +form+ "%d"
            else:
                print('format unknown')
        datetime.date.strptime(a+b+c,format)
    elif a.isdigit() and c.isdigit():
        if c.len()==4:
            formatr="%d"+form+"%M"+form+"%Y"
        elif c.len()==2:
            formatr="%d"+form+"%M"+form+"%y"
        datetime.date.strptime(a+b+c,format)
    elif b.isdigit() and c.isdigit():
        if a.len()==4:
            formatr="%Y"+form+"%M"+form+"%d"
        elif a.len()==2:
            formatr="%y"+form+"%M"+form+"%d"
        else:
            print('format unknown')
        datetime.date.strptime(a+b+c,format)
    else:
        print('format unknown')
    
    return formatr

def df(tin):
    for i in tin:
        if i.isdigit() and flag==0:
            a=a+str(i)
        elif i.isdigit() and flag==1:
            b=b+str(i)
        elif i.isdigit() and flag==2:
            c=c+str(i)
        elif i.isdigit() and flag==3:
            d=d+str(i)
        elif i==":" :
            flag+=1
            form=1
        elif i==".":
            flag+=1
            form=2
        else:
            print("error")       
    return flag,a,b,c,form

def ft(tin,list1):
    a,b,c,a1,b1,c1=""
    flag,flag1=0
    form,form1=0
    flag,a,b,c,form=df(tin)
    if flag==1:
        if form=1:
            for i in list1:
                flag1,a1,b1,c1,form1=df(tin)
                if a1
            
            format=1

            format=2
        else:
            print('format unknown')
        for i in list1:
            #read for a to be mm or dd according to m being 1-12
        datetime.date.strptime(a+b+c,format)
    elif flag==2:
        if 
        datetime.date.strptime(a+b+c, format)
    else:
        print('format unknown')
        
