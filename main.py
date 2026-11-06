import os
import requests
from serpapi import GoogleSearch

TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = "-1004466833723"
SERPAPI_KEY = os.getenv("SERPAPI_A")

params = {"q": "芭提雅 海景 咖啡厅 推荐", "hl": "zh-tw", "gl": "th", "api_key": SERPAPI_KEY}
res = GoogleSearch(params).get_dict()
items = res.get("organic_results", [])

msg = "☕ 芭提雅海景咖啡厅推荐\n\n"
for i, r in enumerate(items[:3], 1):
    title = (r.get("title") or "").replace("<b>", "").replace("</b>", "")
    snippet = (r.get("snippet") or "").replace("<b>", "").replace("</b>", "")
    msg += f"{i}. {title}\n{snippet}\n{r.get('link')}\n\n"

buttons = {"inline_keyboard": [[
    {"text": "👍 有用", "callback_data": "like"},
    {"text": "👎 没用", "callback_data": "dislike"},
    {"text": "🔗 更多", "url": "https://taotailailangblog.com/pattaya-photo-cafe001/"}
]]}

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
r = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": msg,
    "parse_mode": "HTML",
    "reply_markup": buttons
}, timeout=30)

print("TG状态码:", r.status_code)
print("TG返回:", r.text)
