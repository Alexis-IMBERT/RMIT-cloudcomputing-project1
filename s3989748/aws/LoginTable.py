import boto3

from ...variable import *

def create_login_table():
    """ Create the login table """

    
def generate_password():
    """ generate the password as asked in the assignement """
    password_base = "0123456789"
    password = []
    for i in range(10):
        if i<=4:
            password.append(password_base[i:i+6])
        else:
            password.append(password_base[i:i+6]+password_base[:i-4])
    return password


def fill_login_table():
    """ fill the login table as ask on the assignement """
    list_password = generate_password()
    for i in range(10):
        # generation of email, username and password
        email = STUDENT_ID+str(i)+END_MAIL
        user_name = FIRST_NAME+' '+LAST_NAME+str(i)
        password = list_password[i]
        
        value = {"email":email,"user_name":user_name,"password":password}
        
        # sending to the DynamoDB
        print(value)
        