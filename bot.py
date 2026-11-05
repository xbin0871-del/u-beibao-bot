import os, json, re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x]
DATA_FILE = "data.json"
EXPIRE_HOURS = 24

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"orders": [], "deposit": 0}
    return json.load(open(DATA_FILE, "r", encoding="utf-8"))

def save_data(data):
    json.dump(data, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def parse_order(text):
    order = {}
    m = re.search(r"订单交易号[:：]\s*(T\w+)", text)
    if m: order["tx"] = m.group(1)
    m = re.search(r"交易金额[:：]\s*([\d.]+)\s*U", text)
    if m: order["amount"] = m.group(1)
    m = re.search(r"交易方用户名/ID[:：]\s*(@\w+|\S+)", text)
    if m: order["trader"] = m.group(1)
    m = re.search(r"公群方[:：]\s*(@\w+|\S+)", text)
    if m: order["group"] = m.group(1)
    m = re.search(r"报备有效期[:：](\d+)小时", text)
    if m: order["expire_h"] = int(m.group(1))
    order["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order["done"] = "已完成" in text or "完成" in text
    return order

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("报备机器人已启动。发订单文本即存档。")

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    try:
        amt = float(context.args[0])
        data = load_data()
        data["deposit"] = amt
        save_data(data)
        await update.message.reply_text(f"✅ 押金设为 {amt}U")
    except:
        await update.message.reply_text("用法: /deposit 80")

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    order = parse_order(text)
    if not order.get("tx"):
        return
    data = load_data()
    data["orders"].append(order)
    save_data(data)
    msg = (f"✅ 新单已存档｜{order.get('tx','')}｜金额 {order.get('amount','?')}U｜"
           f"交易方 {order.get('trader','')}｜公群方 {order.get('group','')}｜"
           f"有效期 → {'已完成' if order['done'] else '进行中'}")
    kb = [[InlineKeyboardButton("🔍 本群查询", callback_data="q_group"),
           InlineKeyboardButton("📂 我的报备", callback_data="q_mine")]]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

async def expire_job(app):
    data = load_data()
    now = datetime.now()
    data["orders"] = [o for o in data["orders"] if
                      (now - datetime.strptime(o["time"], "%Y-%m-%d %H:%M:%S")).total_seconds()
                      < (o.get("expire_h", EXPIRE_HOURS) * 3600) and not o.get("done")]
    save_data(data)

def main():
    a = Application.builder().token(TOKEN).build()
    a.add_handler(CommandHandler("start", start))
    a.add_handler(CommandHandler("deposit", deposit))
    a.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_msg))
    a.run_polling()

if __name__ == "__main__":
    main()
