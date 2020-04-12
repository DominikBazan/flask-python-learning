from flask import Flask, render_template, url_for, request, redirect, session
from database import dbConnection, truncateTableNamed, printTableNamed
from todos import todoInsert, getTodos, todoDelete, todoUpdate
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from tech import v2Q

# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'IbliKndy1l'
app.config['MYSQL_PASSWORD'] = 'M8ENJ9wmy8'
app.config['MYSQL_DB'] = 'IbliKndy1l'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return  User.query.get(int(user_id))

@app.route('/', methods=['POST', 'GET'])
def index():
    if not session.get('login'):
        return redirect('/login')
    else:
        db = dbConnection()
        if request.method == 'POST':
            value = request.form['new-todo']
            try:
                if value:
                    todoInsert(db, value)
                return redirect('/')
            except:
                return "SQL Error"
        else:
            todos = getTodos(db)
            return render_template('index.html', todos=todos)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        login = request.form['login']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        # print("XXXXXXXXXXXXXXXXX:")
        # print(hash_password)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (login, pass) VALUES (%s,%s)",(login,hash_password,))
        mysql.connection.commit()
        session['login'] = login
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
    app.secret_key = "748fdmf**jnxhdelndf"
    app.run(debug=True)
    