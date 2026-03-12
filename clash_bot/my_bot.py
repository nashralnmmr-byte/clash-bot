from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await update.message.reply_text("مرحباً بك! البوت جاهز للاستخدام.")

if __name__ == '__main__':
    TOKEN = '8305222145:AAGaZItCfuTBiCcwO8gjX4E0jny3Hvx7j5I'
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 البوت يعمل الآن.. بانتظار أوامرك!")
    app.run_polling()
