import telebot
from telebot import types
import os

# 1. መረጃዎችን ከ Railway Variables መሳብ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

# --- እዚህ ጋር የዶላር ዋጋውን በየቀኑ መቀየር ትችላለህ ---
CURRENT_DOLLAR_RATE = 120.5  # ለምሳሌ 1 ዶላር 120.5 ብር ከሆነ
# -----------------------------------------------

bot = telebot.TeleBot(TOKEN)

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

def send_main_menu(chat_id):
    # Reply Keyboard (ከታች ከታይፒንግ ስር የሚመጣ)
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
    if message.text == "💸 USDT መግዛት/መሸጥ (P2P)":
        text = f"💰 **የአሁኑ የUSDT ዋጋ፦** `{CURRENT_DOLLAR_RATE} ETB`\n\nለመግዛት ወይስ ለመሸጥ ይፈልጋሉ? እባክዎ የሚፈልጉትን የUSDT መጠን በቁጥር ብቻ ይላኩ።\n\n*(ለምሳሌ፦ 50)*"
        msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, calculate_p2p)

    elif message.text == "🔱 Tutorial & Info":
        tutorial_text = (
            "🔱 **ስለ Ethio Free Server ቦት** 🔱\n\n"
            "ይህ ቦት የተመሰረተው የክሪፕቶ ግብይትን (P2P) ለኢትዮጵያውያን ለማቅለል ነው።\n\n"
            "📖 **መመሪያዎች፦**\n"
            "1️⃣ **P2P:** እዚህ ጋር USDT መግዛትና መሸጥ ይችላሉ። ቦቱ አሁን ያለውን የገበያ ዋጋ ተጠቅሞ በብር ስንት እንደሚመጣ ያሰላልዎታል።\n"
            "2️⃣ **Ads:** የእርስዎን ምርት ወይም አገልግሎት በቻናላችን ላይ ማስተዋወቅ ሲፈልጉ የሚጠቀሙበት ነው።\n"
            "3️⃣ **ደህንነት:** ማንኛውም ግብይት በአድሚኑ @semir_yusuf አማካኝነት በታማኝነት የሚፈጸም ይሆናል።\n\n"
            "ቦቱን ስለተጠቀሙ እናመሰግናለን!"
        )
        bot.send_message(message.chat.id, tutorial_text, parse_mode="Markdown")

    elif message.text == "📣 ማስታወቂያ ለማሰራት":
        msg = bot.send_message(message.chat.id, "📣 የማስታወቂያውን ዝርዝር ይጻፉ። አድሚን አይቶ ያነጋግርዎታል።")
        bot.register_next_step_handler(msg, process_ads)

    elif message.text == "🌟 Donate (Stars/TON)":
        donate_text = (
            "🌟 **ቦቱን ይደግፉ** 🌟\n\n"
            "የቦቱን አገልግሎት ለማሻሻል በቴሌግራም ስታርስ (Stars) ወይም በቶን (TON) ልገሳ ማድረግ ይችላሉ።\n\n"
            "💎 **TON Address:** `የአንተ_የቶን_አድራሻ_እዚህ_ይግባ`\n"
            "⭐ **Stars:** አድሚኑን @semir_yusuf በማነጋገር ስጦታ መላክ ይችላሉ።"
        )
        bot.send_message(message.chat.id, donate_text, parse_mode="Markdown")

    elif message.text == "🙋‍♂️ ጥያቄና ሀሳብ":
        bot.send_message(message.chat.id, "ለማንኛውም ጥያቄ አድሚኑን እዚህ ያግኙ፦ @semir_yusuf")

# የP2P ስሌት መስሪያ
def calculate_p2p(message):
    try:
        amount = float(message.text)
        total_etb = amount * CURRENT_DOLLAR_RATE
        response = (
            f"📊 **የስሌት ውጤት**\n\n"
            f"🔹 የUSDT መጠን: `{amount} USDT`\n"
            f"🔹 የአሁኑ ዋጋ: `{CURRENT_DOLLAR_RATE} ETB`\n"
            f"👉 **ጠቅላላ ክፍያ: `{total_etb:,.2f} ETB`**\n\n"
            "ለመቀጠልና ግብይቱን ለመፈጸም እርግጠኛ ነዎት?"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ አዎ! መግዛት/መሸጥ እፈልጋለሁ", callback_data=f"confirm_p2p_{amount}"))
        bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode="Markdown")
    except ValueError:
        bot.send_message(message.chat.id, "❌ እባክዎ መጠንን በቁጥር ብቻ ያስገቡ! (ለምሳሌ፦ 10)")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "ተሳክቷል!")
            send_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "አሁንም ቻናሉን አልተቀላቀሉም!", show_alert=True)
    
    elif call.data.startswith("confirm_p2p_"):
        amount = call.data.split("_")[-1]
        bot.send_message(ADMIN_ID, f"🔔 **አዲስ የP2P ጥያቄ!**\n\n👤 @{call.from_user.username}\n💰 መጠን: {amount} USDT\n💵 ብር: {float(amount)*CURRENT_DOLLAR_RATE:,.2f} ETB")
        bot.send_message(call.message.chat.id, "✅ ጥያቄዎ ለአድሚን ደርሷል። አድሚኑ በውስጥ መስመር ያነጋግርዎታል።")

def process_ads(message):
    bot.send_message(ADMIN_ID, f"📣 **የማስታወቂያ ጥያቄ፦**\n\nከ @{message.from_user.username}\nመልእክት፦ {message.text}")
    bot.send_message(message.chat.id, "✅ የማስታወቂያ ጥያቄዎ ደርሷል።")

if __name__ == "__main__":
    bot.infinity_polling()
