print ("Login // Sign up Script")

# sql connection is going to go here

def Sign_up():
    
    username = info.form['username'] 
    password = info.form['password']

    hashed_password = generate_password_hash(password, method='sha256') # hash method for encrpting the password for safety of user info 

    # sql check if username is already inside the database

    # sql create a new user and save it into the database

    return 'user signup success!'

# might try add in a check to see if a user name already exit inside the data base 
#this would stop errors when users are trying to log in 

def login():

    if info.form == 'POST': # here im going to use a method called post which is made to interact with sql 

    username = info.form['username'] 
    password = info.form['password']

    
# sql connection for vault goes here
def add_to_vault():

    detail_lable = vault.form  # the name of password 
    
    username = vault.form

    password = vault.form

    #sql check if inputed informantion is already inside the vault 

    hashed_password = generate_password_hash(password, method='sha256') # hash password 

    return 'details added to your vault!'

     