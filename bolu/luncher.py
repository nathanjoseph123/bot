from flask import Flask, request, jsonify, render_template
import threading, time,os
from bot import custom_bot

app = Flask(__name__)

bot_running = False
bot_starter = None
bot_number = custom_bot.counter
bot_timer = 2

@app.route("/")
def form():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global bot_running, bot_thread, bot_number, bot_timer
    if bot_running:
        return jsonify({"status": "Bot already running"})

    data = request.json
    url = data.get("url")
    auth = data.get("auth")
    api_key = data.get("api")
    special_id = data.get("special")
    idv = data.get("idv")
    user_prompt = data.get("user_prompt")
    bot_timer = max(1, min(60, data.get("timer", 2)))

    bot_running = True
    try:
        bot_starter = threading.Thread(
            target=custom_bot,
            args=(str(url), str(api_key), str(auth), str(user_prompt), str(idv), int(bot_timer), str(special_id))
        )
        bot_starter.start()
    except Exception as e:
        pass

    bot_number = custom_bot.counter
    return jsonify({"status": f"Bot started with timer {bot_timer}s!\n"})

@app.route("/stop", methods=["POST"])
def stop():
    global bot_running
    if not bot_running:
        return jsonify({"status": "Bot is not running"})
    bot_running = False
    bot_number=0
    return jsonify({"status": "Bot stopped"})

@app.route("/number")
def get_number():
    bot_number = custom_bot.get_number()
    return jsonify({"number": bot_number})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)







