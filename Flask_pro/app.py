from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mysqldb import MySQL
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = 'root',
    database = 'flask',
    port = 3306,
    auth_plugin = 'mysql_native_password'
)

app = Flask(__name__)
sql=MySQL(app)



app.config['SQLALCHEMY_DATABASE_URI'] = ("sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200), nullable = False) 
    desc = db.Column(db.Integer, nullable = False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, sno=None, title=None, desc=None, date_create=None):
        self.sno = sno
        self.title = title
        self.desc = desc
        self.date_create = date_create

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} "

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    print(allTodo,"-------all todo-------")
    return render_template('index.html',allTodo=allTodo)
   
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# @app.route('/todo', methods=['POST', 'GET'])
# def hello_world():
#     if request.method == "POST":
#         data = request.get_json()
#         print(data,"----data")
#         title = data.get("title")
#         desc = data.get('desc')
#         print(title,desc,"0000000000000000")
#         todo = Todo(title =title, desc = desc)
#         db.session.add(todo)
#         db.session.commit()
#         return jsonify({"msg":"Data Add Successfully"})
#     # return 'Hello, World!'

@app.route('/show')
def product():
    allTodo = Todo.query.all()
    print(allTodo,"-------all todo-------")
    return 'this is product'

if __name__ == "__main__":
    app.run(debug=True, port=8000)