# https://www.youtube.com/watch?v=3vfum74ggHE

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests, json

# --- App object
app = Flask(__name__)
app.app_context().push()        # flask_sqlalchemy troubleshooting



# --- Database
# setup DB files for the app & create DB object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qna_db.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'thesis_db': 'sqlite:///thesis_db.sqlite'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# define DB models //table of 2 columns
class QNA( db.Model):
    id = db.Column( db.Integer, primary_key=True)
    message = db.Column( db.String(2000))
class Thesis( db.Model):
    __bind_key__ = 'thesis_db'
    thesis_id = db.Column( db.Integer, primary_key=True)
    thesis_message = db.Column( db.String(2000))

# create and init DBs
db.create_all(bind_key=[None, 'thesis_db'])



# -- Endpoints //interface
# 1. Homepage endpoint
@app.get("/")
def home():
    qna_list = db.session.query(QNA).all()                    # load the DB
    return render_template( "base.html", qna_list=qna_list)   # render html using the loaded DB


# 2. Send button endpoint
@app.post("/button")                            #} This send button endpoint does 3 things:
                                                #} 1) Builds, Sends prompt & saves response
                                                #} 2) Adds prompt & response to 'QNA' DB
                                                #} 3) Creates another thesis for 'Thesis' DB
                                                #} 4) Refreshes page
def button():
    # 1) Send prompt & save response
    # Building prompt: Loading 5 last theses from 'Thesis' DB                                                
    thesis = ''
    thesis_temp = db.session.query(Thesis).order_by(Thesis.thesis_id.desc()).limit(5).all()
    for entry in thesis_temp:
        thesis = thesis+entry.thesis_message+'; '
    input = thesis

    # Building prompt: Get contents of <input> named "prompt" from <form>
    prompt = request.form.get("prompt")     

    # Sending built prompt & saving model response
    response_json = requests.post(
                            "http://127.0.0.1:8000/predict", 
                            json={"prompt": prompt,
                                  "input": input}
                            )
    response_str = response_json.json()["output"]
    print( '######### RESPONSE PROMPT #########')
    print( response_str)
    cut = response_str.split("### Response:")
    response = cut[1]


    # 2) Add prompt & response to 'QNA' DB
    new_qna = QNA( message=prompt)              # declare prompt DB sample
    db.session.add( new_qna)                    #} add&commit new sample to DB
    db.session.commit()                         #}
    new_qna = QNA( message=response)            # declare prompt DB sample
    db.session.add( new_qna)                    #} add&commit new sample to DB
    db.session.commit()                         #}


    # 3) Create another thesis for 'Thesis' DB
    prompt = ''
    prompt_temp = db.session.query(QNA).order_by(QNA.id.desc()).limit(2).all()
    prompt = 'In less than exactly 5 words explain what was this dialogue about: me: ' + prompt_temp[1].message + ' you: ' + prompt_temp[0].message
    response_json = requests.post(
                            "http://127.0.0.1:8000/predict", 
                            json={"prompt": prompt,
                                  "input": ''}
                            )
    response_str = response_json.json()["output"]
    print( '######### TOPIC PROMPT #########')
    print( response_str)
    cut = response_str.split("### Response:")
    response = cut[1]
    response = response[:100]                           # Truncating string to save context capacity 
    
    new_thesis = Thesis( thesis_message=response)       # declare prompt DB sample
    db.session.add( new_thesis)                         #} add&commit new sample to DB
    db.session.commit()                                 #}


    # 4) Refresh page
    return redirect( url_for( "home"))          # redirect to home page


# 3. Delete button endpoint
@app.get("/delete/<int:qna_id>")
def delete(qna_id):
    qna = db.session.query(QNA).filter(QNA.id == qna_id).first()
    db.session.delete(qna)
    db.session.commit()
    return redirect( url_for( "home"))

