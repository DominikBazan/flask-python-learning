from flask import Flask, render_template, url_for, request, redirect
from database import dbConnection, truncateTableNamed, printTableNamed
from todos import todoInsert, getTodos, todoDelete, todoUpdate

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    db = dbConnection()
    if request.method == 'POST':
        value = request.form['content']
        try:
            if value:
                todoInsert(db, value)
            return redirect('/')
        except:
            return "SQL Error"
    else:
        todos = getTodos(db)
        return render_template('index.html', todos=todos)

@app.route('/delete/<string:value>')
def delete(value):
    print(">XXXX<")
    db = dbConnection()
    try:
        todoDelete(db, value)
        return redirect('/')
    except:
        return 'SQL Error'

@app.route('/update/<string:value>', methods=['GET', 'POST'])
def update(value):
    if request.method == 'POST':
        try:
            db = dbConnection()
            new = request.form['content']
            todoUpdate(db, value, new)
            return redirect('/')
        except:
            return 'SQL Error (update)'
    else:
        return render_template('update.html', todo=value)

if __name__ == "__main__":
    app.run(debug=True)
    