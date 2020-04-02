import mysql.connector


def dbConnection():
    file = open("db_data.txt", "r")
    myHost = file.readline()
    myUser = file.readline()
    myPasswd = file.readline()[:10]
    myDatabase = file.readline()
    file.close()

    dataBase = mysql.connector.connect(
        host = myHost,
        user = myUser,
        passwd = myPasswd,
        database = myDatabase
    )
    return dataBase


def truncateTableNamed(db, tableName):
    cursor = db.cursor()
    cursor.execute("TRUNCATE " + tableName)
    db.commit()
    cursor.close()


def printTableNamed(db, tableName):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM " + tableName)
    rows = ""
    for x in cursor:
        rows += str(x) + "\n"
    print(rows)