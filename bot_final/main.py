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
        return "⚠️ عذراً، حدث خطأ في الاتصال بالقاعدة."

async def handle_message(update, context):
    query = update.message.text
    # نجرب البحث في الجنود أولاً
    result = get_data(query, TROOPS_URL)
    # إذا لم يجد، نجرب البحث في المباني
    if "❌" in result:
        result = get_data(query, BUILDINGS_URL)
    await update.message.reply_text(result)

def main():
    # سحب التوكن من إعدادات السحابة لاحقاً
    TOKEN = os.environ.get('BOT_TOKEN')
    if not TOKEN:
        print("خطأ: لم يتم العثور على BOT_TOKEN")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 البوت انطلق بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
