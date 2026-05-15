import telebot
from telebot import types
import os

# 1. መረጃዎችን ከ Railway Variables መሳብ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')  # የአንተ የቴሌግራም ID (በቁጥር)
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

bot = telebot.TeleBot(TOKEN)

# በጊዜያዊነት የዶላር ዋጋ እዚህ ይቀመጣል 
CURRENT_DOLLAR_RATE = 120.0 

# የተጠቃሚዎችን የግብይት ሂደት ለመያዝ
user_sessions = {}

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton("🔥 JOIN CHANNEL 🔥", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        btn_check = types.InlineKeyboardButton("🔄 አረጋግጥ", callback_data="check_sub")
        markup.add(btn_join)
        markup.add(btn_check)
        bot.send_message(message.chat.id, f"እንኳን መጡ! ቦቱን ለመጠቀም መጀመሪያ ቻናላችንን ይቀላቀሉ፦ {CHANNEL_USERNAME}", reply_markup=markup)
        return
    
    send_main_menu(message.chat.id)

# ለአድሚን ብቻ የዶላር ዋጋ መለወጫ (/setrate 125.5)
@bot.message_handler(commands=['setrate'])
def set_rate(message):
    global CURRENT_DOLLAR_RATE
    if str(message.from_user.id) == str(ADMIN_ID):
        try:
            new_rate = float(message.text.split()[1])
            CURRENT_DOLLAR_RATE = new_rate
            bot.reply_to(message, f"✅ የዶላር ዋጋ በተሳካ ሁኔታ ተቀይሯል!\n💵 የአሁኑ ዋጋ፦ `{CURRENT_DOLLAR_RATE} ETB`", parse_mode="Markdown")
        except:
            bot.reply_to(message, "❌ እባክዎ በትክክል ያስገቡ። ምሳሌ፦ `/setrate 120.5`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ ይህንን ለማድረግ ፈቃድ የለዎት跻።")

def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("💸 USDT መግዛት/መሸጥ (P2P)")
    btn2 = types.KeyboardButton("📣 ማስታወቂያ ለማሰራት")
    btn3 = types.KeyboardButton("🔱 Tutorial & Info")
    btn4 = types.KeyboardButton("🌟 Donate (Stars/TON)")
    btn5 = types.KeyboardButton("🙋‍♂️ ጥያቄና ሀሳብ")

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)

    welcome_text = "እንኳን ወደ **Ethio Free Server** በደህና መጡ! 🚀\n\nእባክዎ ከታች ካሉት አማራጮች የሚፈልጉትን ይምረጡ።"
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
