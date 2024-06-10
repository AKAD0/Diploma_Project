# https://www.youtube.com/watch?v=3vfum74ggHE

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests, json

# --- App object
app = Flask(__name__)
app.app_context().push()        # flask_sqlalchemy troubleshooting



# --- Database
# setup DB files for the app & create DB object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'topic_db': 'sqlite:///topic_db.sqlite'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# define DB models //table of 2 columns
class History( db.Model):
    id = db.Column( db.Integer, primary_key=True)
    message = db.Column( db.String(2000))
class Topic( db.Model):
    __bind_key__ = 'topic_db'
    topic_id = db.Column( db.Integer, primary_key=True)
    topic_message = db.Column( db.String(2000))

# create and init DBs
db.create_all(bind_key=[None, 'topic_db'])



# -- Endpoints //interface
# 1. Homepage endpoint
@app.get("/")
def home():
    history_list = db.session.query(History).all()                    # load the DB
    return render_template( "base.html", history_list=history_list)   # render html using the loaded DB


# 2. Send button endpoint
@app.post("/button")                            #} This send button endpoint does 3 things:
                                                #} 1) Sends prompt & saves response
                                                #} 2) Adds prompt & response to 'History' DB
                                                #} 3) Creates another topic for 'Topic' DB
                                                #} 4) Refreshes page
def button():
    # Loading 5 last topics from 'Topic' DB                                                
    topic = ''
    topic_temp = db.session.query(Topic).order_by(Topic.topic_id.desc()).limit(5).all()
    for entry in topic_temp:
        topic = topic+entry.topic_message+'; '
    input = topic


    # 1) Send prompt & save response
    prompt = request.form.get("prompt")     #} get contents of <input> named "prompt"
                                            #} from <form>
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


    # 2) Add prompt & response to 'History' DB
    new_history = History( message=prompt)      # declare prompt DB sample
    db.session.add( new_history)                #} add&commit new sample to DB
    db.session.commit()                         #}
    new_history = History( message=response)    # declare prompt DB sample
    db.session.add( new_history)                #} add&commit new sample to DB
    db.session.commit()                         #}


    # 3) Create another topic for 'Topic' DB
    prompt = ''
    prompt_temp = db.session.query(History).order_by(History.id.desc()).limit(2).all()
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
    
    new_topic = Topic( topic_message=response)                # declare prompt DB sample
    db.session.add( new_topic)     #} add&commit new sample to DB
    db.session.commit()            #}


    # 4) Refresh page
    return redirect( url_for( "home"))          # redirect to home page


# 3. Delete button endpoint
@app.get("/delete/<int:history_id>")
def delete(history_id):
    history = db.session.query(History).filter(History.id == history_id).first()
    db.session.delete(history)
    db.session.commit()
    return redirect( url_for( "home"))

