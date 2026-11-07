import os
import requests
from flask import Flask, request

TOKEN = os.getenv("TOKEN")
TG = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)

def send(chat_id, text):
    try:
        requests.post(f"{TG}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=5)
    except Exception as e:
        print(f"Send error: {e}")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    u = request.json
    if not u:
        return "ok"
    
    # 兼容所有更新类型，防止 KeyError 崩溃
    msg = u.get("message") or u.get("edited_message") or u.get("channel_post")
    
    if msg:
        chat_id = msg.get("chat", {}).get("id")
        user = msg.get("from", {})
        user_id = user.get("id")
        text = msg.get("text", "").strip()
        
        if not chat_id:
            return "ok"
            
        if text == "/start":
            send(chat_id, "皇冠")
        elif text == "/verify":
            send(chat_id, "✅ 服务正常")
        # 这里保留你原来的 @xxx 业务逻辑入口
        elif text.startswith("@"):
            send(chat_id, "已收到指令")
            
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
