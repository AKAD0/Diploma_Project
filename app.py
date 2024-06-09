# https://www.youtube.com/watch?v=3vfum74ggHE

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests, json

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
    message = db.Column( db.String(2000))

# create and init the DB
db.create_all()



# -- Endpoints //interface
# 1. Homepage endpoint
@app.get("/")
def home():
    history_list = db.session.query(History).all()                    # load the DB
    return render_template( "base.html", history_list=history_list)   # render html using the loaded DB


# 2. Send button endpoint
@app.post("/button")                            #} This send button endpoint does 3 things:
                                                #} 1) Sends prompt & saves response
                                                #} 2) Adds prompt & response to DB
                                                #} 3) Refreshes page
def button():
    prompt = request.form.get("prompt")             #} get contents of <input> named "prompt"
                                                    #} from <form>
    input = 'User name is Akado'                    # PLACEHOLDER
    # Getting history from DB
    input_temp = db.session.query(History).order_by(History.id.desc()).limit(10).all()
    for entry in input_temp:
        print( entry.message)
    # 1) Send prompt & save response
    response_json = requests.post(
                            "http://127.0.0.1:8000/predict", 
                            json={"prompt": prompt,
                                  "input": input}
                            )
    response_str = response_json.json()["output"]
    cut = response_str.split("### Response:")
    print( type(response_str))
    print(response_str)
    response = cut[1]


    # 2) Add prompt & response to DB
    new_history = History( message=prompt)     # declare prompt DB sample
    db.session.add( new_history)                #} add&commit new sample to DB
    db.session.commit()                         #}
    ########### PLACEHOLDER <add response to DB> ###########
    new_history = History( message=response)     # declare prompt DB sample
    db.session.add( new_history)                #} add&commit new sample to DB
    db.session.commit()                         #}
    ########### PLACEHOLDER <add response to DB> ###########

    # 3) Refresh page
    return redirect( url_for( "home"))          # redirect to home page


# 3. Delete button endpoint
@app.get("/delete/<int:history_id>")
def delete(history_id):
    history = db.session.query(History).filter(History.id == history_id).first()
    db.session.delete(history)
    db.session.commit()
    return redirect( url_for( "home"))

