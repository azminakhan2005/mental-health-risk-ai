import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from flask_pymongo import PyMongo
import bcrypt
from model import analyze_text
from chatbot import chat_response
from dotenv import load_dotenv
import re
import matplotlib.pyplot as plt
import io
from datetime import datetime
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["MONGO_URI"] = "mongodb://localhost:27017/mentalhealth"
mongo = PyMongo(app)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():

    error=None

    if request.method=='POST':

        name=request.form['name']
        email=request.form['email']
        password=request.form['password']

        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            error="Invalid email format"

        elif len(password)<6:
            error="Password must be at least 6 characters"

        else:

            users=mongo.db.users
            existing_user=users.find_one({'email':email})

            if existing_user:
                error="Email already registered"

            else:

                hashpass=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

                users.insert_one({
                    "name":name,
                    "email":email,
                    "password":hashpass
                })

                return redirect('/login')

    return render_template('register.html',error=error)


# ---------------- LOGIN ----------------
@app.route('/login',methods=['GET','POST'])
def login():

    error=None

    if request.method=='POST':

        email=request.form['email']
        password=request.form['password']

        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            error="Invalid email format"

        else:

            users=mongo.db.users
            login_user=users.find_one({'email':email})

            if login_user and bcrypt.checkpw(password.encode('utf-8'),login_user['password']):

                session['email']=email
                return redirect('/dashboard')

            else:
                error="Invalid email or password"

    return render_template('login.html',error=error)


# ---------------- DASHBOARD ----------------
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():

    if 'email' not in session:
        return redirect('/login')

    email=session['email']

    emotion=None
    risk=None
    support=None
    journal=""
    emotion_scores=None

    # ---------- LOAD HISTORY ENTRY ----------

    selected_entry=request.args.get("entry")

    if selected_entry:

        entry=mongo.db.entries.find_one({"_id":ObjectId(selected_entry)})

        if entry:

            emotion=entry.get("emotion")
            risk=entry.get("risk")
            journal=entry.get("text")
            support=entry.get("suggestions")
            emotion_scores=entry.get("emotions")


    # ---------- NEW JOURNAL ----------

    if request.method=='POST':

        journal=request.form['journal']

        result=analyze_text(journal)

        emotion_scores=result["emotions"]
        risk=result["risk"]
        suggestions=result["suggestions"]

        # dominant emotion
        emotion=max(emotion_scores,key=emotion_scores.get)

        mongo.db.entries.insert_one({

            "email":email,
            "text":journal,
            "emotion":emotion,
            "emotions":emotion_scores,
            "risk":risk,
            "risk_score":risk,
            "suggestions":suggestions,
            "date":datetime.now()

        })

        support=suggestions


    # ---------- HISTORY ----------

    history=list(

        mongo.db.entries
        .find({"email":email})
        .sort("date",-1)
        .limit(20)

    )

    return render_template(

        "dashboard.html",

        emotion=emotion,
        emotion_scores=emotion_scores,
        risk=risk,
        support=support,
        journal=journal,
        history=history

    )


# ---------------- CHATBOT ----------------
@app.route('/chat',methods=['POST'])
def chat():

    if 'email' not in session:
        return jsonify({"reply":"Please login first."})

    user_message=request.json['message']
    email=session['email']

    past_entries=list(

        mongo.db.entries
        .find({"email":email})
        .sort("date",-1)
        .limit(5)

    )

    history_text="\n".join([e["text"] for e in past_entries])

    if "chat_history" not in session:
        session["chat_history"]=[]

    session["chat_history"].append({"role":"user","content":user_message})

    reply=chat_response(user_message,history_text,session["chat_history"])

    session["chat_history"].append({"role":"assistant","content":reply})

    return jsonify({"reply":reply})


# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():

    entries=mongo.db.entries.find()

    return render_template("admin.html",entries=entries)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('email',None)

    return redirect('/')


# ---------------- RISK GRAPH ----------------
@app.route("/risk_graph")
def risk_graph():

    if 'email' not in session:
        return redirect('/login')

    data=list(

        mongo.db.entries
        .find({"email":session['email']})
        .sort("date",-1)
        .limit(5)

    )

    risks=[entry["risk_score"] for entry in data if "risk_score" in entry]

    if not risks:
        risks=[0]

    x_vals=list(range(1,len(risks)+1))

    plt.figure(figsize=(6,3))

    plt.plot(x_vals,risks,marker='o')

    plt.xlabel("Last Entries")
    plt.ylabel("Risk Level")

    plt.ylim(0,1)

    plt.grid(True)

    img=io.BytesIO()

    plt.tight_layout()
    plt.savefig(img,format="png")
    plt.close()

    img.seek(0)

    return send_file(img,mimetype="image/png")


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("home.html")


# ---------------- RUN ----------------
if __name__=="__main__":
    app.run(debug=True)