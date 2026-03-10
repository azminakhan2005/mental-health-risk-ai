import json
import os

FILE = "risk_history.json"

def load_history():

    if not os.path.exists(FILE):
        return []

    with open(FILE,"r") as f:
        return json.load(f)

def save_history(history):

    with open(FILE,"w") as f:
        json.dump(history,f)

def update_risk(current_risk):

    history = load_history()

    history.append(current_risk)

    if len(history) > 5:
        history = history[-5:]

    save_history(history)

    avg = sum(history)/len(history)

    final_risk = current_risk + avg*0.25

    return min(final_risk,1)