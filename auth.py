import psycopg2
from datetime import datetime
from main import main
from connect import conn

try:
    # create a cursor
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


def reg():
    try:
        # execute a statement REGISTER
        print("Register".center(35, "*"))
        email = input("Email: ")
        if email == "/login":
            log()
        elif '@' not in email or "." not in email:
            print("Please enter a valid email address!")
            reg()
        password = input("Password: ")
        if password != None and email != None:
            insert_query = """ INSERT INTO accounts (EMAIL, PASSWORD, CREATED_ON) VALUES ('{}', '{}', '{}')""".format(email, password, datetime.now())
            cur.execute(insert_query) #should have hash a password here!
            conn.commit()
            cur.execute("SELECT * from accounts WHERE email='{}'".format(email))
            record = cur.fetchone()
            print("You registered successfully!")
            log()
        else:
            print("Plesae enter a valid Email and Password!")
            reg()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def log():
    try:
        # execute a statement LOGIN
        print("LOGIN".center(45, "-"))
        email = input("Login Email: ")
        if email == "/register":
            reg()
        password = input("Login Password: ")
        if password != None and email != None:
            check_query = """ select * from accounts where email='{}' and password='{}' """.format(email, password)
            cur.execute(check_query)
            conn.commit()
            record = cur.fetchone()
            if record:
                print("You logged in successfully!")
                main({'user_id':record[0],'email': record[2], "is_authenticated":True})
            else:
                print("Password|Email is not valid! to register write /register")
                log()
        else:
            print("Plesae enter Email and Password! to register write /register")
            log()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def authenticate():
    reg_or_log = input(" <Register:1 or Login:2> //:")
    if reg_or_log == '1':
        reg()
    elif reg_or_log == '2':
        log()
    else:
        print("Please choose <Register:1> or <Login:2> option!")
        authenticate()

if __name__ == '__main__':
    authenticate()

    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()
        cur.close()
