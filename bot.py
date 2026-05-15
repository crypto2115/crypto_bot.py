import telebot
from telebot import types
import os

# 1. መረጃዎችን ከ Railway Variables መሳብ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')  # የአንተ የቴሌግራም ID (በቁጥር)
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

bot = telebot.TeleBot(TOKEN)

# በጊዜያዊነት የዶላር ዋጋ እዚህ ይቀመጣል (ቦቱ ሪስታርት ሲያደርግ ወደ መጀመሪያው ይመለሳል)
# በቋሚነት ለመቀየር እዚሁ ላይ መለወጥ ትችላለህ
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
        bot.reply_to(message, "❌ ይህንን ለማድረግ ፈቃድ የለዎትም።")

def send_main_menu(chat_id):
    # ከታይፒንግ ስር የሚመጣው Reply Keyboard
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
    chat_id = message.chat.id
    user_id = message.from_user.id

    if message.text == "💸 USDT መግዛት/መሸጥ (P2P)":
        # መጀመሪያ መግዛት ወይስ መሸጥ እንደሆነ መምረጥ አለበት
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_buy = types.KeyboardButton("🟢 USDT መግዛት እፈልጋለሁ")
        btn_sell = types.KeyboardButton("🔴 USDT መሸጥ እፈልጋለሁ")
        btn_back = types.KeyboardButton("🔙 ወደ ዋናው ማውጫ")
        markup.add(btn_buy, btn_sell)
        markup.add(btn_back)
        
        bot.send_message(chat_id, f"💰 **የአሁኑ የUSDT ዋጋ፦** `{CURRENT_DOLLAR_RATE} ETB`\n\nምን ማድረግ ይፈልጋሉ?", reply_markup=markup, parse_mode="Markdown")

    elif message.text in ["🟢 USDT መግዛት እፈልጋለሁ", "🔴 USDT መሸጥ እፈልጋለሁ"]:
        action = "BUY" if "መግዛት" in message.text else "SELL"
        user_sessions[user_id] = {"action": action}
        
        # ወደ ዋናው ማውጫ ለመመለስ እንዲያመች ሪፕላይ ኪቦርዱን እናቆየዋለን
        msg = bot.send_message(chat_id, "🔢 እባክዎ የሚፈልጉትን የUSDT መጠን በቁጥር ብቻ ያስገቡ፦\n*(ለምሳሌ፦ 50)*")
        bot.register_next_step_handler(msg, calculate_p2p)

    elif message.text == "🔱 Tutorial & Info":
        tutorial_text = (
            "🔱 **ስለ Ethio Free Server ቦት** 🔱\n\n"
            "ይህ ቦት የተመሰረተው የክሪፕቶ ግብይትን (P2P) ለኢትዮጵያውያን ለማቅለል እና ለማገዝ ነው።\n\n"
            "📖 **መመሪያዎች፦**\n"
            "1️⃣ **P2P ግብይት:** እዚህ ጋር USDT መግዛትና መሸጥ ይችላሉ። ቦቱ አሁን ያለውን የገበያ ዋጋ ተጠቅሞ በብር ስንት እንደሚመጣ ያሰላልዎታል።\n"
            "2️⃣ **Ads (ማስታወቂያ):** የእርስዎን ምርት ወይም አገልግሎት በቻናላችን ላይ ማስተዋወቅ ሲፈልጉ የሚጠቀሙበት ነው።\n"
            "3️⃣ **ደህንነት:** ማንኛውም ግብይት በአድሚኑ @crypto_2115 አማካኝነት በታማኝነት የሚፈጸም ይሆናል።\n\n"
            "ቦቱን ስለተጠቀሙ እናመሰግናለን!"
        )
        bot.send_message(chat_id, tutorial_text, parse_mode="Markdown")

    elif message.text == "📣 ማስታወቂያ ለማሰራት":
        msg = bot.send_message(chat_id, "📣 የማስታወቂያውን ዝርዝር ጽፈው ይላኩ። አድሚን አይቶ ያነጋግርዎታል።")
        bot.register_next_step_handler(msg, process_ads)

    elif message.text == "🌟 Donate (Stars/TON)":
        donate_text = (
            "🌟 **ቦቱን ይደግፉ** 🌟\n\n"
            "የቦቱን አገልግሎት ይበልጥ ለማሳደግ በቴሌግራም ስታርስ (Stars) ወይም በቶን (TON) ልገሳ ማድረግ ይችላሉ።\n\n"
            "💎 **TON Wallet Address:**\n`EQB... (እዚህ ጋር የቶን አድራሻህን አስገባ)`\n\n"
            "⭐ **Telegram Stars:**\nበቀጥታ አድሚኑን @crypto_2115 በማነጋገር በስጦታ መልክ መላክ ይችላሉ።\n\n"
            "ለሚያደርጉት ድጋፍ ከልብ እናመሰግናለን! 🙏"
        )
        bot.send_message(chat_id, donate_text, parse_mode="Markdown")

    elif message.text == "🙋‍♂️ ጥያቄና ሀሳብ":
        bot.send_message(chat_id, "ለማንኛውም ጥያቄ አድሚኑን እዚህ ያግኙ፦ @crypto_2115")

    elif message.text == "🔙 ወደ ዋናው ማውጫ":
        send_main_menu(chat_id)

# የP2P ስሌት መስሪያ
def calculate_p2p(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if message.text == "🔙 ወደ ዋናው ማውጫ":
        send_main_menu(chat_id)
        return

    try:
        amount = float(message.text)
        total_etb = amount * CURRENT_DOLLAR_RATE
        
        # የተጠቃሚውን ምርጫ ማግኘት (መግዛት ወይም መሸጥ)
        session = user_sessions.get(user_id, {"action": "ግብይት"})
        action_text = "🟢 መግዛት" if session["action"] == "BUY" else "🔴 መሸጥ"
        
        response = (
            f"📊 **የስሌት ውጤት ({action_text})**\n\n"
            f"🔹 የUSDT መጠን: `{amount} USDT`\n"
            f"🔹 የአሁኑ ዋጋ: `{CURRENT_DOLLAR_RATE} ETB`\n"
            f"👉 **ጠቅላላ ክፍያ: `{total_etb:,.2f} ETB`**\n\n"
            "ለመቀጠልና ግብይቱን ለመጀመር እርግጠኛ ነዎት?"
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ አዎ! እርግጠኛ ነኝ", callback_data=f"confirm_{session['action']}_{amount}"))
        bot.send_message(chat_id, response, reply_markup=markup, parse_mode="Markdown")
        
    except ValueError:
        msg = bot.send_message(chat_id, "❌ እባክዎ መጠንን በቁጥር ብቻ ያስገቡ! (ለምሳሌ፦ 50)\nድጋሚ ይሞክሩ፦")
        bot.register_next_step_handler(msg, calculate_p2p)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "ተሳክቷል!")
            send_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "አሁንም ቻናሉን አልተቀላቀሉም!", show_alert=True)
    
    elif call.data.startswith("confirm_"):
        parts = call.data.split("_")
        action = parts[1] # BUY ወይም SELL
        amount = parts[2]
        total_etb = float(amount) * CURRENT_DOLLAR_RATE
        
        action_title = "🟢 መግዛት" if action == "BUY" else "🔴 መሸጥ"
        
        # ለአድሚን የሚላክ መረጃ
        admin_msg = (
            f"🔔 **አዲስ የP2P ጥያቄ መጥቷል!**\n\n"
            f"👤 ተጠቃሚ፦ @{call.from_user.username if call.from_user.username else 'የለውም'}\n"
            f"🆔 ID: `{call.from_user.id}`\n"
            f"የተመረጠው፦ {action_title}\n"
            f"💰 መጠን፦ `{amount} USDT`\n"
            f"💵 ጠቅላላ ብር፦ `{total_etb:,.2f} ETB`"
        )
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        
        # ለደንበኛው የሚላክ
        bot.send_message(call.message.chat.id, "✅ ምርጫዎ ተመዝግቧል! አድሚኑ @crypto_2115 በውስጥ መስመር ያነጋግርዎታል።")

def process_ads(message):
    if message.text == "🔙 ወደ ዋናው ማውጫ":
        send_main_menu(message.chat.id)
        return
        
    bot.send_message(ADMIN_ID, f"📣 **የማስታወቂያ ጥያቄ፦**\n\nከ @{message.from_user.username}\nመልእክት፦ {message.text}")
    bot.send_message(message.chat.id, "✅ የማስታወቂያ ጥያቄዎ ደርሷል። አድሚን ያነጋግርዎታል።")

if __name__ == "__main__":
    bot.infinity_polling()
