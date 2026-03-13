import os
import requests
from flask import Flask
from threading import Thread
from telegram.ext import Application, MessageHandler, filters

# --- 1. جزء الـ Flask لإبقاء البوت مستيقظاً على Render ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "البوت يعمل الآن بنجاح!"

def run():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. بيانات البوت (Clash of Clans Data) ---
TROOPS_URL = "https://raw.githubusercontent.com/warden-clash/clash-data/main/troops.json"
BUILDINGS_URL = "https://raw.githubusercontent.com/warden-clash/clash-data/main/buildings.json"

def get_data(name, url):
    try:
        response = requests.get(url).json()
        for item in response:
            if item['name'].lower() == name.lower():
                # جلب البيانات بناءً على الصيغة الموجودة في ملفات الـ JSON
                return f"🔍 الاسم: {item['name']}\n❤️ الصحة: {item.get('hp', 'غير معروف')}\n⚔️ الضرر: {item.get('dps', 'غير معروف')}"
        return "❌ لم أجد معلومات حول هذا الاسم."
    except Exception as e:
        return "⚠️ حدث خطأ في جلب البيانات."

async def handle_message(update, context):
    query = update.message.text
    result = get_data(query, TROOPS_URL)
    # إذا لم يجد في القوات، يبحث في المباني
    if "❌" in result:
        result = get_data(query, BUILDINGS_URL)
    await update.message.reply_text(result)

# --- 3. تشغيل البوت ---
def main():
    # سيحاول قراءة التوكن من Render أولاً، وإذا لم يجده سيستخدم التوكن الذي أرسلته
    TOKEN = os.getenv('BOT_TOKEN') or "8305222145:AAESW75-Aj3uF4ETCPDgslqiu41l2V7Qn_8"
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 البوت بدأ العمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    keep_alive() # تشغيل خادم الويب المصغر
    main()       # تشغيل البوت
	
