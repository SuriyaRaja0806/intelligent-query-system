from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

# --- Intelligent Query System core ---
SECRET_KEY = "GDG{You_Completed_The_Quest!}"

import json, os

STATE_FILE = "iqs_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {}

    # ✅ Ensure defaults always exist
    if "unlocked" not in state:
        state["unlocked"] = False
    if "gates" not in state:
        state["gates"] = 0

    return state

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

import os

STATE_FILE = "iqs_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"gate1": False, "gate2": False, "gate3": False, "unlocked": False}
    with open(STATE_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"gate1": False, "gate2": False, "gate3": False, "unlocked": False}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def chatbot_response(user_input):
    state = load_state()

    if state["unlocked"]:
        return "You already unlocked the secret key for this session."

    if not state["gate1"]:
        if "please mentor" in user_input.lower():
            state["gate1"] = True
            save_state(state)
            return "Gate 1 passed ✅. Now answer: What is 2 + 2?"
        return "Hint: Try greeting me politely."

    if not state["gate2"]:
        if user_input.strip() == "4":
            state["gate2"] = True
            save_state(state)
            return "Gate 2 passed ✅. Next: Say the magic word (hint: starts with 'open')."
        return "Try again. What is 2 + 2?"

    if not state["gate3"]:
        if "open sesame" in user_input.lower():
            state["gate3"] = True
            state["unlocked"] = True
            save_state(state)
            return f"🎉 All gates passed! Here is the secret key: {SECRET_KEY}"
        return "Hint: It's a classic magic phrase."

    return "Keep trying..."

# --- FastAPI App ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    reply = chatbot_response(message)
    return templates.TemplateResponse("chat.html", {"request": request, "user_message": message, "bot_reply": reply})
