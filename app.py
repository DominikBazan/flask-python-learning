import bcrypt
from flask import Flask, render_template, url_for, request, redirect, session
from todos import todoInsert, getTodos, todoDelete, todoUpdate
from flask_mysqldb import MySQL, MySQLdb
from tech import v2Q

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'IbliKndy1l'
app.config['MYSQL_PASSWORD'] = 'M8ENJ9wmy8'
app.config['MYSQL_DB'] = 'IbliKndy1l'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.secret_key = '748fdmf**jnxhdelndf'

@app.route('/', methods=['POST', 'GET'])
def index():
    if not session.get('login'):
        return redirect('/login')
    else:
        if request.method == 'POST':
            value = request.form['new-todo']
            try:
                if value:
                    todoInsert(value, mysql)
                return redirect('/')
            except:
                return "SQL Error"
        else:
            todos = getTodos(mysql)
            return render_template('index.html', todos=todos)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        login = request.form['login']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (login, pass) VALUES (%s,%s)",(login,hash_password,))
        mysql.connection.commit()
        cur.execute("SELECT * FROM users WHERE login=%s",(login,))
        user = cur.fetchone()
        cur.close()
        session['login'] = login
        session['id_user'] = user['id_user']
        return redirect('/')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE login=%s",(login,))
        user = cur.fetchone()
        cur.close()
        if user:
            if bcrypt.checkpw(password, user['pass'].encode('utf-8')):
                session['login'] = user['login']
                session['id_user'] = user['id_user']
                return redirect("/")
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route('/delete/<string:value>')
def delete(value):
    try:
        todoDelete(value, mysql)
        return redirect('/')
    except:
        return 'SQL Error'

@app.route('/update/<string:value>', methods=['GET', 'POST'])
def update(value):
    if request.method == 'POST':
        try:
            new = request.form['content']
            todoUpdate(value, new, mysql)
            return redirect('/')
        except:
            return 'SQL Error (update)'
    else:
        return render_template('update.html', old=value)

if __name__ == "__main__":
    app.run(debug=True)
    