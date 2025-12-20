from flask import Flask, request, jsonify, render_template, session
import os
from threading import Thread, Event
from bot import custom_bot

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key')   # needed for session

# a simple in‑memory store for demo purposes
_bots = {}   # session_id -> (bot_instance, timer)

@app.route("/")
def form():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    # generate a per‑session identifier if not present
    sid = session.sid
    if sid not in _bots:
        url = data["url"]
        auth = data["auth"]
        api_key = data["api"]
        special_id = data["special"]
        idv = data["idv"]
        user_prompt = data["user_prompt"]
        bot_timer = max(1, min(60, data.get("timer", 2)))

        bot = custom_bot(str(url), str(api_key), str(auth),
                         str(user_prompt), str(idv), int(bot_timer),
                         str(special_id))
        _bots[sid] = (bot, bot_timer)
        return jsonify({"status": f"Bot started with timer {bot_timer}s!"})
    else:
        return jsonify({"status": "Bot already running for this session"}), 400

@app.route("/stop", methods=["POST"])
def stop():
    sid = session.sid
    if sid in _bots:
        bot, _ = _bots.pop(sid)
        bot.end()
        return jsonify({"status": "Bot stopped"})
    return jsonify({"status": "No bot running for this session"}), 400

@app.route("/number")
def getnumber():
    sid = session.sid
    if sid in _bots:
        bot, _ = _bots[sid]
        return jsonify({"number": bot.get_number()})
    return jsonify({"number": None}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
