def title_case(columns):
    num = 0
    for i in df[columns]:
        if type(i) == str:
            df.loc[num,columns] = df.loc[num,columns].title()
        num = num + 1    
        
        
        
def upper_case(columns):
    n = 0
    for i in df[columns]:
        if type(i) == str:
            df.loc[n,columns] = df.loc[n,columns].upper()
        n = n + 1  
        
        
        
        
def strip_spaces(columns):
    n = 0
    for i in df[columns]:
        if type(i) == str:
            df.loc[n,columns] = df.loc[n,columns].strip()
        n = n + 1   
        
        
        
def lower_case(columns):
    n = 0
    for i in df[columns]:
        if type(i) == str:
            df.loc[n,columns] = df.loc[n,columns].lower()
        n = n + 1 
        
        
        
        
