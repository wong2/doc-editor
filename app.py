#-*-coding:utf-8-*-
from flask import Flask, request, Response, render_template, g, abort
from flaskext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

####################SQLAlchemy########################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title 
        self.content = content 

    def __repr__(self):
        return '<Document %r>' % self.title

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content}

#######################################################

# jsonify response decorator
def jsonify(f):
    def wrapped(*args, **kwargs):
        return Response(json.dumps(f(*args, **kwargs)), mimetype='application/json')
    return wrapped


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/documents', methods=["GET", "POST"], defaults={"document_id": None})
@app.route("/documents/<int:document_id>", methods=["GET", "PUT", "DELETE"])
@jsonify
def document(document_id):
    if not document_id:
        if request.method == "GET":
            return [{"id": d.id, "title": d.title} for d in Document.query.all()]
        elif request.method == "POST":
            doc = Document(request.json["title"], request.json["content"])
            db.session.add(doc)
            db.session.commit()
            return doc.to_dict()
    else:
        doc = Document.query.filter_by(id=document_id).first()
        if request.method == "GET":
            return doc.to_dict()
        elif request.method == "PUT":
            doc.title = request.json["title"]
            doc.content = request.json["content"]
            db.session.commit()
            return doc.to_dict()
        elif request.method == "DELETE":
            result = doc.to_dict()
            db.session.delete(doc)
            db.session.commit()
            return result

if __name__ == "__main__":
    app.run(debug=True)
