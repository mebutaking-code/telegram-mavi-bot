import os
import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TR_TO_AR_PROMPT = """Sen profesyonel bir Türkçe-Arapça çeviri uzmanısın. Görevin:
- Sana verilen Türkçe metni Suriye Arapçasına (Şam lehçesi) çevir.
- Suriye'de günlük konuşmada kullanılan doğal ve akıcı ifadeleri tercih et.
- Resmi/yazı dili (Fusha) yerine Suriye halk dilini kullan.
- Deyimleri ve kalıp ifadeleri birebir çevirme, Suriye Arapçasındaki karşılıklarını kullan.
- Sadece çeviri sonucunu döndür, açıklama veya not ekleme.
- Kısa mesajlarda bile doğal ve samimi bir ton kullan."""

AR_TO_TR_PROMPT = """Sen profesyonel bir Arapça-Türkçe çeviri uzmanısın. Görevin:
- Sana verilen Arapça metni Türkiye Türkçesine çevir.
- Türkiye'de günlük konuşmada kullanılan doğal ve akıcı ifadeleri tercih et.
- Resmi dil yerine samimi ve anlaşılır günlük Türkçe kullan.
- Arapça deyimleri ve kalıp ifadeleri birebir çevirme, Türkçedeki karşılıklarını kullan.
- Sadece çeviri sonucunu döndür, açıklama veya not ekleme.
- Kısa mesajlarda bile doğal ve samimi bir ton kullan."""


def is_arabic(text):
    arabic_count = 0
    total_count = 0
    for char in text:
        if char.isalpha():
            total_count += 1
            if "\u0600" <= char <= "\u06FF" or "\u0750" <= char <= "\u077F" or "\u08A0" <= char <= "\u08FF":
                arabic_count += 1
    if total_count == 0:
        return False
    return (arabic_count / total_count) > 0.5


def is_only_emoji_or_punctuation(text):
    for char in text:
        if char.isalpha() or char.isdigit():
            return False
    return True


async def translate_text(text, source_lang, target_lang):
    try:
        if source_lang == "tr":
            system_msg = TR_TO_AR_PROMPT
        else:
            system_msg = AR_TO_TR_PROMPT

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ceviri hatasi: {e}")
        return None


async def handle_message(update: Update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user = update.effective_user
    username = user.username if user.username else user.first_name

    if is_only_emoji_or_punctuation(text):
        return

    if text.lower().startswith("hey mavi"):
        return

    if is_arabic(text):
        translated = await translate_text(text, "ar", "tr")
        if translated:
            reply = f"@{username}:\n{translated}"
            await update.message.reply_text(reply)
    else:
        translated = await translate_text(text, "tr", "ar")
        if translated:
            reply = f"@{username}:\n{translated}"
            await update.message.reply_text(reply)


async def start(update: Update, context):
    await update.message.reply_text("Merhaba! Ben Mavi, ceviri botuyum.")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
