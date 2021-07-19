def checkNull(column_name):                  
    # INPUT WILL BE FROM CONFIG FILE
    try:
        
        '''
         This list contains a series of boolean values if the datavalue is NaN it will have True in its corresponding 'i'th 
         position or it wll have False in its corresponding 'i'th position
        '''
        
        li = df[column_name].isnull().tolist() 
        num = 0 
        lis=[] 
        '''empty list which will contain the idices of all the rows which have NaN values '''
        for i in li:
            if i == True:
                lis.append(num)
                logger.info("Error on line " + f"{num+1}\n" + f"{df.iloc[num]}")
            num = num + 1
#         print('indices found with null values', lis)
        lis.reverse()
        ''' reverses the list'''
        for j in lis:
            df.drop(index = j, inplace = True)
        
        logger.info('Sucessfully removed the rows that had NaN in ' + f"{column_name}")    
    except:
        
        '''
        if the column name provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.exception('Column heading specified not present in the table')  
        

        
        
def upper_better(columns):
    '''
    So if the argumenet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,columns]) == str:    
                df.loc[i,columns] = df.loc[i,columns].upper() 
                '''converts the element into upper case'''
        logger.info('Successfully converted all the elements in the '+ f"{columns}" ' to upper case')   
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.exception('Column heading specified not present in the table')
        
        
        
def lower_better(columns):
    '''
    So if the argumnet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,columns]) == str:    
                df.loc[i,columns] = df.loc[i,columns].lower() 
                '''converts the element into lower case'''
        logger.info('Successfully converted all the elements in the '+ f"{columns}" ' to lower case')        
           
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.exception('Column heading specified not present in the table')
        
        
        
def title_better(columns):
    '''
    So if the argumnet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,columns]) == str:    
                df.loc[i,columns] = df.loc[i,columns].title() 
                '''converts the element into title case'''
        logger.info('Successfully converted all the elements in the '+ f"{columns}" ' to title case')
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.exception('Column heading specified not present in the table')
        
        
        
        
def strip_better(columns):
    '''
    So if the argumnet provided to the function is a vaild column name in the dataframe then the flow of code will go thorugh
    TRY part and neglect the except part
    '''
    try:
        '''
        So df.index is a pandas command which returns the series of index of the dataframe. Index is unique to each and every row
        present in the table. .tolist() function is used to convert the data type returned by .index commmand to list so that it
        can be iterated easily
        '''    
        for i in df.index.tolist():
            ''' 
            Checks whether the data type of elements present in specified column
            is string or not
            '''

            if type(df.loc[i,columns]) == str:    
                df.loc[i,columns] = df.loc[i,columns].strip() 
                '''strips the element for empty spaces'''
        logger.info('Successfully stripped for spaces all the elements in the '+ f"{columns}")  
    except:
        
        '''
        if the argument provided is not the column heading then this part of code will be executed. It will be logged
        in a seperate logging file
        '''
        
        logger.exception('Column heading specified not present in the table')        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
