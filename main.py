import os, requests
from flask import Flask, request

TOKEN = os.getenv("TOKEN")
TG = "https://api.telegram.org/bot" + TOKEN
app = Flask(__name__)

@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    u = request.get_json(silent=True) or {}
    m = u.get("message") or {}
    c = m.get("chat", {})
    cid = c.get("id")
    txt = (m.get("text") or "").strip()
    if cid and txt == "/verify":
        requests.post(TG + "/sendMessage", json={"chat_id": cid, "text": "✅ 活了，开工"}, timeout=10)
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
