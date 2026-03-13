import os
import requests
from flask import Flask
from threading import Thread
from telegram.ext import Application, MessageHandler, filters

# سيرفر خفيف لإبقاء البوت مستيقظاً
app_flask = Flask('')
@app_flask.route('/')
def home():
    return "Bot is alive!"

def run():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# دالة ذكية لجلب البيانات مع معالجة الأخطاء
def get_data(name):
    url = "https://raw.githubusercontent.com/warden-clash/clash-data/main/troops.json"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                # التحقق من وجود الاسم في البيانات
                if 'name' in item and item['name'].lower() == name.lower():
                    return f"اسم الجندي: {item['name']}\nالصحة: {item.get('hp', 'N/A')}\nالضرر: {item.get('dps', 'N/A')}"
            return "عذراً، لم أجد هذا الاسم في قاعدة البيانات."
        return f"فشل الاتصال بالمصدر (كود: {response.status_code})"
    except Exception as e:
        return f"خطأ تقني أثناء الجلب: {str(e)}"

async def handle_message(update, context):
    query = update.message.text.strip()
    result = get_data(query)
    await update.message.reply_text(result)

def main():
    # سحب التوكن من المتغير الذي أضفته في Render
    TOKEN = os.getenv('BOT_TOKEN')
    if not TOKEN:
        print("خطأ: لم يتم العثور على BOT_TOKEN في إعدادات Render!")
        return
        
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🚀 البوت بدأ العمل الآن بنجاح!")
    app.run_polling()

if __name__ == '__main__':
    keep_alive()
    main()

