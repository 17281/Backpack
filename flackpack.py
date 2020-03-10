"""21/02/20 Harry C, Flask with BackPack Challenge""" 
from flask import Flask, render_template, request,g,redirect
import sqlite3



app = Flask(__name__)

DATABASE = 'BackPack.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    cursor = get_db().cursor()
    sql = "SELECT * FROM BacPac"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("contents.html", results=results)

@app.route('/add', methods=["GET","POST"])
def add(): 
    if request.method == "POST":
        cursor = get_db().cursor()
        new_name = request.form["item_name"]
        new_description = request.form["item_description"]
        sql = "INSERT INTO BacPac (Item,Description) VALUES (?,?)"
        cursor.execute(sql,(new_name,new_description))
        get_db().commit()
    return redirect ('/')

@app.route('/delete', methods=["GET","POST"])
def delete():
    if request.method == "POST":
        #get item and delete with data base
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM BacPac WHERE id=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)