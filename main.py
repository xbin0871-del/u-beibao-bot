from flask import Flask, request
import telebot # 或 python-telegram-bot

TOKEN = "你的Token"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return 'ok', 200

@app.route('/set', methods=['GET'])
def set_webhook():
    # 部署后访问一次 /set 完成绑定
    bot.set_webhook(url="https://serp-worker.onrender.com")
    return 'webhook set'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
