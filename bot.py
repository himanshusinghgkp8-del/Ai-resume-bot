import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me your details (Name, Skills, Experience) and I will create a professional resume for you.")

async def generate_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": user_text}
        ]
    )

    resume = response['choices'][0]['message']['content']
    await update.message.reply_text(resume)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_resume))

app.run_polling()
