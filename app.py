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
class History( db.Model):
    id = db.Column( db.Integer, primary_key=True)
    title = db.Column( db.String(2000))

# create and init the DB
db.create_all()



# -- Endpoints //interface
@app.get("/")
def home():
    History_list = db.session.query(History).all()                    # load the DB
    return render_template( "base.html", History_list=History_list)   # render html using the loaded DB

@app.post("/button")
def button():
    title = request.form.get("title")               #} get contents of <input> named "title"
                                                    #} from <form>
    new_History = History( title=title)                   # declare new DB sample
    db.session.add( new_History)                       #} add&commit new sample to DB
    db.session.commit()                             #}
    return redirect( url_for( "home"))              # once done redirect to home page

@app.get("/delete/<int:History_id>")
def delete(History_id):
    History = db.session.query(History).filter(History.id == History_id).first()
    db.session.delete(History)
    db.session.commit()
    return redirect( url_for( "home"))

