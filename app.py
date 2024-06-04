# https://www.youtube.com/watch?v=3vfum74ggHE

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- App object
app = Flask(__name__)
app.app_context().push()        # flask_sqlalchemy troubleshooting



# --- Database
# setup DB file for the app & create DB object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# define DB model //table of 3 columns
class Todo( db.Model):
    id = db.Column( db.Integer, primary_key=True)
    title = db.Column( db.String(2000))

# create and init the DB
db.create_all()



# -- Endpoints //interface
@app.get("/")
def home():
    todo_list = db.session.query(Todo).all()                    # load the DB
    return render_template( "base.html", todo_list=todo_list)   # render html using the loaded DB

@app.post("/button")
def button():
    title = request.form.get("title")               #} get contents of <input> named "title"
                                                    #} from <form>
    new_todo = Todo( title=title)                   # declare new DB sample
    db.session.add( new_todo)                       #} add&commit new sample to DB
    db.session.commit()                             #}
    return redirect( url_for( "home"))              # once done redirect to home page

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect( url_for( "home"))

