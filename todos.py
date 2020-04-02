# from random import randrange
# from datetime import timedelta
from tech import v2Q


def todoInsert(db, value):
    cursor = db.cursor()
    query = "INSERT into todos (value) VALUES ("+ v2Q(value) +")"
    cursor.execute(query)
    db.commit()
    cursor.close()

def getTodos(db):
    cursor = db.cursor()
    query = "SELECT value FROM todos"
    cursor.execute(query)
    todosList = []
    for (value) in cursor:
        todosList.append(value[0])
    cursor.close()

    return todosList

def todoDelete(db, value):
    cursor = db.cursor()
    query = "DELETE FROM todos WHERE value = " + v2Q(value)
    cursor.execute(query)
    db.commit()
    cursor.close()

def todoUpdate(db, old, new):
    cursor = db.cursor()
    query = "UPDATE todos SET value=" + v2Q(new) + " WHERE value=" + v2Q(old)
    cursor.execute(query)
    db.commit()
    cursor.close()