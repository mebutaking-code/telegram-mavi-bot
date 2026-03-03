import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI
import os

# Bot ve API anahtarları
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Manus ortamında OpenAI istemcisi otomatik olarak yapılandırılmıştır.
# client = OpenAI() çağrısı gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash modellerine erişim sağlar.
# Render.com'da ise OPENAI_API_KEY ortam değişkeni otomatik olarak kullanılacaktır.
client = OpenAI()

# Günlükleme ayarları
logging.basicConfig(
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def is_arabic(text):
    """Metinde Arapça karakter olup olmadığını kontrol eder."""
    # Arapça Unicode aralığı: U+0600–U+06FF
    return bool(re.search(r\'[\\u0600-\\u06FF]\', text))

def is_just_emojis_or_punctuation(text):
    """Metnin sadece emoji veya noktalama işaretlerinden oluşup oluşmadığını kontrol eder."""
    # Python\'un standart re kütüphanesi \p{P} gibi Unicode kategorilerini desteklemez.
    # Bunun yerine basit bir kontrol yapalım: Harf veya rakam var mı?
    # Eğer metinde hiç harf (A-Z, a-z, Arapça harfler) veya rakam yoksa sadece emoji/noktalama kabul edelim.
    has_content = bool(re.search(r\'[\\w\\u0600-\\u06FF]\', text))
    return not has_content

async def translate_text(text, target_lang):
    """Ücretsiz API kullanarak metni çevirir."""
    system_prompt = "Sen bir çeviri asistanısın. Sana verilen metni sadece çevir, başka hiçbir şey ekleme. Türkçe metni Suriye Arapçasına, Arapça metni Türkiye Türkçesine çevir. Sadece çeviri sonucunu döndür."
    try:
        # Manus ortamında gemini-2.5-flash modelini kullanıyoruz.
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
             temperature=0.3, # Daha tutarlı çeviri için temperature düşürüldü 
 maks_tokens=1000, 
         ) 
 return response.choices[0].message.content.strip () 
 Exception e olarak hariç: 
         logger.error(f"Çeviri hatası: {e}") 
         return f"Çeviri sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin." 

async def message_handler (güncel: Güncelleme, içerik: Bağlam. Default_type:
     """Gelen mesajları işler ve çevirir.""" 
 eğer update.message ve update.message.text: 
 original_text = update.message.text 
 chat_id = update.message.chat_id 
 message_id = update.message.message_id 
        
 Kullanıcı = update.message.from_user 
 sender_username = user.username if user.username else f"{user.first_name} {user.last_name if user.last_name else \'\'}".strip() 

         # Emoji/noktalama kontrolü 
 is_just_emojis_or_punctuation (original_text): 
             logger.info(f"Sadece emoji/noktalama içeren mesaj atlandı: {original_text}") 
 Dönüş (film) 

         # \"Hey Mavi\" komutunu kontrol et 
 Eğer original_text.lower ().startswith ("hey mavi"): 
 Bekleyin context.bot.send_message (İngilizce) 
 chat_id=chat_id, 
 reply_to_message_id=message_id, 
                 text=f"Merhaba @{sender_username}! Ben Mavi. Gruptaki mesajları otomatik olarak Türkçe <-> Suriye Arapçası arasında çeviriyorum. Başka bir komuta ihtiyacım yok, sadece yazmanız yeterli!" 
             ) 
 Dönüş (film) 

         # Çeviri işlemi 
 is_arabic (original_text): 
 logger.info (f"Arapça mesaj algılandı: {original_text}") 
 translated_text = translated_text'i bekliyor (original_text, "tr") 
 Diğer: 
             logger.info(f"Türkçe mesaj algılandı: {original_text}") 
 translated_text = translated_text'i bekliyor (original_text, "ar-SY") 

 Eğer translated_text: 
 Bekleyin context.bot.send_message (İngilizce) 
 chat_id=chat_id, 
 reply_to_message_id=message_id, 
 text=f"@{sender_username}:\n{translated_text}" 
             ) 

def main ():
     """Botu çalıştırır.""" 
     logger.info("Bot başlatılıyor...") 
 application = ApplicationBuilder ().token (TELEGRAM_BOT_TOKEN).build() 

     # Mesaj işleyiciyi ekle 
     # Sadece metin mesajlarını işle, komutları (~filters.COMMAND) hariç tut (isteğe bağlı) 
 application.add_handler (MessageHandler) (filters. TEXT & (~filters) . KOMAND | filtreler. Regex (re.compile) (r\'^hey mavi\', re. IGNORECASE))), message_handler)) 

     # Botu polling modunda başlat 
 Application.run_polling 

Eğer __name__ == "__main__":
 Ana madde: 
