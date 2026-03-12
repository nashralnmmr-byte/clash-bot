import os
import requests
from telegram.ext import Application, MessageHandler, filters

# روابط البيانات
TROOPS_URL = "https://raw.githubusercontent.com/warden-sh/clash-data/main/json/troops.json"
BUILDINGS_URL = "https://raw.githubusercontent.com/warden-sh/clash-data/main/json/buildings.json"

def get_data(name, url):
    try:
        response = requests.get(url).json()
        for item in response:
            if item['name'].lower() == name.lower():
                return f"🔍 الاسم: {item['name']}\n❤️ الصحة: {item.get('hp', 'غير متوفر')}\n⚔️ الضرر: {item.get('dps', 'غير متوفر')}"
        return "❌ لم أجد هذا الاسم."
    except:
        return "⚠️ خطأ في الاتصال بالقاعدة."

async def handle_message(update, context):
    query = update.message.text
    result = get_data(query, TROOPS_URL)
    if "❌" in result:
        result = get_data(query, BUILDINGS_URL)
    await update.message.reply_text(result)

def main():
    # استخدام التوكن الذي أرسلته
    TOKEN = "8305222145:AAESW75-Aj3uF4ETCPDgslqiu41l2V7Qn_8"
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🚀 البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
