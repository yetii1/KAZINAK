import os
import json
import urllib.request
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def api_call(method, data):
    url = f"{API}/{method}"
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    api_call("sendMessage", data)

def handle_update(update):
    msg = update.get("message")
    if not msg:
        return
    text = msg.get("text", "")
    chat_id = msg["chat"]["id"]
    if text == "/start":
        keyboard = {
            "inline_keyboard": [[{
                "text": "🎰 Открыть Roulette Engine",
                "web_app": {"url": WEBAPP_URL}
            }]]
        }
        send_message(chat_id, "🎡 *Roulette Engine*\n\nАналитическая система европейской рулетки.\nНажми кнопку ниже:", keyboard)

def main():
    print("Бот запущен...")
    offset = 0
    while True:
        try:
            url = f"{API}/getUpdates?timeout=30&offset={offset}"
            with urllib.request.urlopen(url, timeout=35) as r:
                data = json.loads(r.read())
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                handle_update(update)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
