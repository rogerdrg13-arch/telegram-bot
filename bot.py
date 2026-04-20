import requests
import os
import time

TOKEN = "8691585057:AAE1fmJCorL2zuXIHU0-Mt16JZh0BHBpVYs"
DEEPSEEK_KEY = "sk-f4d2443efd0c47d8b1f22172aedadf57"

last_id = 0

def get_updates():
    global last_id
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}&timeout=10"
    try:
        r = requests.get(url, timeout=15)
        return r.json().get("result", [])
    except:
        return []

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except:
        pass

def ask_deepseek(question):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": f"Посоветуй фильм: {question}"}]}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Ошибка. Попробуйте еще раз."

print("Бот запущен!")

while True:
    updates = get_updates()
    for update in updates:
        last_id = update["update_id"]
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            if text == "/start":
                send_message(chat_id, "🎬 Привет! Напиши, какой фильм хочешь посмотреть.")
            else:
                send_message(chat_id, "🔍 Ищу фильм...")
                answer = ask_deepseek(text)
                send_message(chat_id, answer)
    time.sleep(1)
