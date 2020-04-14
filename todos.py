from tech import v2Q
from flask import session
from flask_mysqldb import MySQL, MySQLdb

def todoInsert(value, mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "INSERT INTO todos (id_user, value) VALUES (%s,%s)" % (session['id_user'],v2Q(value))
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    
def getTodos(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT value FROM todos WHERE id_user=%s" % (session['id_user'])
    cur.execute(query)
    todosList = []
    for (value) in cur:
        todosList.append(value['value'])
    mysql.connection.commit()
    cur.close()

    return todosList

def todoDelete(value, mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "DELETE FROM todos WHERE value=%s AND id_user=%s;" % (v2Q(value),session['id_user'])
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

def todoUpdate(old, new, mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "UPDATE todos SET value=%s WHERE value=%s AND id_user=%s" % (v2Q(new),v2Q(old),session['id_user'])
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
