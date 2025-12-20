from flask import Flask, request, jsonify, render_template
import os
from bot import custom_bot
app = Flask(__name__)
bot_running = False
bot_thread = None
bot = None
bot_number = 0
@app.route("/")
def form():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    #global bot_running, bot_thread, bot_number,bot
    data = request.json
    url = data.get("url")
    auth = data.get("auth")
    api_key = data.get("api")
    special_id = data.get("special")
    idv = data.get("idv")
    user_prompt = data.get("user_prompt")
    bot_timer = max(1, min(60, data.get("timer", 2)))


    # create bot instance
    bot_running = True
    bot = custom_bot(str(url), str(api_key), str(auth), str(user_prompt), str(idv), int(bot_timer), str(special_id))
    bot_number = bot.get_number()

    return jsonify({"status": f"Bot started with timer {bot_timer}s!"})

@app.route("/stop", methods=["POST"])
def stop():
    #global bot_running,bot_number,bot

    if not bot_running:
        return jsonify({"status": "Bot is not running"})

      # signal the bot to stop
    bot_running = False
    bot_number = 0
    bot.end()
    return jsonify({"status": "Bot stopped","number": bot_number})

@app.route("/number")
def getnumber():
    #global bot_number,bot
    if bot:
        bot_number = bot.get_number()
    return jsonify({"number": bot_number})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

