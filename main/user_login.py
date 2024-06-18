import sqlite3
import csv

db_path = "C:/Users/jeelv/Downloads/Assignmentpython/DB Browser for SQLite/abcd.db"
csv_path = "C:/Users/jeelv/Downloads/Assignmentpython/DB Browser for SQLite/abcdBackup.csv"
cypher_dict = {
    "A": "T",
    "B": "I",
    "C": "M",
    "D": "E",
    "E": "O",
    "F": "D",
    "G": "A",
    "H": "N",
    "I": "S",
    "J": "F",
    "K": "R",
    "L": "B",
    "M": "C",
    "N": "G",
    "O": "H",
    "P": "J",
    "Q": "K",
    "R": "L",
    "S": "P",
    "T": "Q",
    "U": "U",
    "V": "V",
    "W": "W",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
    "0": "9",
    "1": "8",
    "2": "7",
    "3": "6",
    "4": "5",
    "5": "4",
    "6": "3",
    "7": "2",
    "8": "1",
    "9": "0"}

def encryptpass(password):
    # password : input password will be all capital letters
    # loop over password , Each word is converted to the relative word given in cypher_dict
    # then the list of characters will be joined with '' - join eadch characters with no space
    return ''.join([cypher_dict[word] for word in password])

# Execution start here.
try:
    conn = sqlite3.connect(db_path) #Create conn with db_path database
    try:
        # Create table
        # If already Exists then ,will give error , except part will pass it.
        conn.execute('''CREATE TABLE TB_USER 
                        (USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        LOGIN CHARACTER VARYING NOT NULL,
                        PASSWORD CHARACTER VARYING,
                        ACCESS_COUNT INT DEFAULT 0);''')
        conn.commit() #Commit the transactions of "conn" connection.
    except Exception as e:
        pass

    username = input('Username : ').strip()
    if not username:
        print('Username is required !')
        raise Exception()
    password = input('Password : ').strip()
    password = password.upper()
    if not password:
        print('Password is required !')
        raise Exception()
    
    if username and password:
        encrypted_password = encryptpass(password)
        cr = conn.cursor() # cursor object to execute and fetch result of queries
        try:
            # select query to check record with same user name exists
            cr.execute("select USER_ID from TB_USER where LOGIN = '{}';".format(username))
            exist_user_res = cr.fetchone()
            if exist_user_res: #if result is give, then user same login exists
                user_id = exist_user_res[0]
                #query to increase the access_count with 1, query will return the new access_count
                cr.execute("update TB_USER set ACCESS_COUNT = ACCESS_COUNT + 1 where USER_ID = {};".format(user_id))
                cr.execute('select ACCESS_COUNT from  TB_USER where USER_ID ={};'.format(user_id))
                access_count = cr.fetchone()
                if access_count:
                    access_count = access_count[0]
                conn.commit() # commit the connection to secure the data changed.
                if access_count:
                    print(username +' - ' +str(access_count))

            else:
                # Create the user with username,encrypted password
                cr.execute("INSERT INTO TB_USER (LOGIN,PASSWORD) VALUES('{}','{}');".format(username,encrypted_password))
                conn.commit() # after creating user commit the connection to secure the data entered.
            
            cr.execute('SELECT * FROM TB_USER;') # return all user data to write in csv.
            all_users = cr.fetchall()
            if all_users:
                with open(csv_path,'w') as f:
                    f.seek(0)
                    writer = csv.writer(f)
                    writer.writerow(['USER_ID','LOGIN','PASSWORD','ACCESS_COUNT'])
                    writer.writerows(all_users)
            
        except Exception as e:
            cr.close()
            raise Exception()
        cr.close()
    ################################
    # this query will remove the table from database.
    conn.execute("drop table TB_USER;")
    # Clear csv file
    with open(csv_path,'w') as f:
        f.flush()
    ################################
    conn.close() #Close connection
except Exception as e:
    conn.close()

