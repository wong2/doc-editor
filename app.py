#-*-coding:utf-8-*-
from flask import Flask, request, render_template, g, abort
import sqlite3, json

DATABASE = "db.sqlite"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/documents", methods=["GET", "POST"])
def documents():
    if request.method == "GET":
        return json.dumps(query_db("select id, title from documents"))
    elif request.method == "POST":
        cursor = g.db.cursor()
        cursor.execute("insert into documents (title, content) values (?, ?)", [request.json["title"], request.json["content"]])
        g.db.commit()
        row = g.db.execute("select * from documents where id=?", (cursor.lastrowid,)).fetchone()
        return json.dumps(dict(id=row[0], title=row[1], content=row[2]))
        
@app.route("/documents/<int:document_id>", methods=["GET", "PUT", "DELETE"])
def handleDocumentById(document_id):
    if request.method == "GET":
        return json.dumps(query_db("select * from documents where id=?", (document_id,), one=True))
    elif request.method == "PUT":
        new_title, new_content = request.json["title"], request.json["content"]
        g.db.execute("update documents set title=?, content=? where id=?", (new_title, new_content, document_id))
        g.db.commit()
        return json.dumps(request.json)
    elif request.method == "DELETE":
        result = query_db("select * from documents where id=?", (document_id,), one=True)
        g.db.execute("delete from documents where id=?", (document_id,))
        g.db.commit()
        return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True)
