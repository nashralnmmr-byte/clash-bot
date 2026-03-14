
import os
import requests
import google.generativeai as genai
from flask import Flask
from threading import Thread
from telegram.ext import Application, MessageHandler, filters
import io

# --- 1. إعداد سيرفر Flask للبقاء حياً على Render ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "Strategic Oracle is Live!"

def run(): app_flask.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- 2. إعداد ذكاء Gemini (نسخة Flash لدعم الصور) ---
genai.configure(api_key=os.getenv("GEMINI_KEY")
# نستخدم gemini-1.5-flash لأنه الأسرع والأفضل في تحليل الصور
model = genai.GenerativeModel('gemini-pro')

# دالة ذكية لتحليل النصوص والصور معاً
async def get_strategic_reply(user_text, photo_bytes=None):
    system_prompt = (
        "أنت 'المستشار الاستراتيجي' لخبير كلاش أوف كلانس. "
        "قواعدك: 1. إذا أرسل المستخدم صورة لقرية، حلل نقاط الضعف (موقع الدفاعات الجوية، الثغرات) واقترح جيشاً وخطه هجوم. "
        "2. إذا سأل عن أرقام (DPS, HP)، أعطه أدق البيانات المتاحة للنسخة العالمية، وإذا سأل بالصينية ركز على نسخة Tencent. "
        "3. كن لبقاً جداً ومحفزاً وافتح نقاشات حول 'الميتا' الحالية. "
        "4. لا تقدم روابط مخططات دفاعية حالياً بناءً على رغبة القائد."
    )
    
    try:
        if photo_bytes:
            # تحليل الصورة مع النص
            content = [system_prompt, {"mime_type": "image/jpeg", "data": photo_bytes}, user_text]
            response = model.generate_content(content)
        else:
            # تحليل النص فقط
            response = model.generate_content(f"{system_prompt}\n\nالمستخدم يسأل: {user_text}")
        
        return response.text
    except Exception as e:
        return f"عذراً يا قائد، سجلاتي تعرضت لتشويش بسيط. حاول مجدداً! (Error: {str(e)})"

# --- 3. معالجة الرسائل (نصوص وصور) ---
async def handle_message(update, context):
    user_text = update.message.text or update.message.caption or "حلل هذه الصورة يا مستشار"
    waiting_msg = await update.message.reply_text("🔎 جاري فحص البيانات الاستراتيجية...")
    
    photo_bytes = None
    if update.message.photo:
        # إذا أرسل المستخدم صورة، نقوم بتحميلها ومعالجتها
        photo_file = await update.message.photo[-1].get_file()
        img_buffer = io.BytesIO()
        await photo_file.download_to_memory(img_buffer)
        photo_bytes = img_buffer.getvalue()

    reply = await get_strategic_reply(user_text, photo_bytes)
    await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=waiting_msg.message_id, text=reply)

# --- 4. التشغيل الرئيسي ---
def main():
    TOKEN = os.getenv('BOT_TOKEN')
    if not TOKEN: return print("Missing BOT_TOKEN!")

    app = Application.builder().token(TOKEN).build()
    
    # معالجة النصوص والصور
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    
    print("🚀 المستشار الاستراتيجي جاهز للغزو!")
    app.run_polling()

if __name__ == '__main__':
    keep_alive()
    main()
