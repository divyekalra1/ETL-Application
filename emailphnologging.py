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
                logger.info("Invalid email present in this row (details): -> " + f"{df.loc[new_email.index(i)]}")     #print out the faulty column index for the particular email
                
                
                
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
                logger.info("Invalid phone number present in this row (details): -> " + f"{df.loc[new_df.index(i)]}") #print the faulty column index corresponding to the phone numbers 
        else:
            logger.info("Invalid phone number in this row (details): -> " + f"{df.loc[new_df.index(i)]}")                
