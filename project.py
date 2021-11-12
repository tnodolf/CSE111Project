import sqlite3
from sqlite3 import Error

#Function to create DB file
def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

#Function to close DB
def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

#Function to create a table
def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")
    _conn.execute('''
    CREATE TABLE league(
        l_name  char(25, 0) not null,
        l_numTeams int(64, 0) not null,
    )''')
    print("++++++++++++++++++++++++++++++++++")

#Main function
def main():
    mainDB = r"cse111project.sqlite" #Creating database

    conn = openConnection(mainDB) #Setting conn as our Connection object to represent the database

    #Initializing DB
    with conn:
        createTable(conn)

    #Closing DB
    closeConnection(conn)

if __name__ == '__main__':
    main()