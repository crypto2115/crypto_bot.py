import telebot
from telebot import types
import os

# በ Railway Variables ላይ ያስገባሃቸውን መረጃዎች መሳብ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

bot = telebot.TeleBot(TOKEN)

# ቻናል Join ማድረጋቸውን ቼክ የሚያደርግ ተግባር
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Subscription check error: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton("🔥 JOIN CHANNEL 🔥", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        btn_check = types.InlineKeyboardButton("🔄 አረጋግጥና ቀጥል", callback_data="check_sub")
        markup.add(btn_join)
        markup.add(btn_check)
        
        bot.send_message(message.chat.id, 
                         f"ሰላም! ቦቱን ለመጠቀም መጀመሪያ የቴሌግራም ቻናላችንን መቀላቀል አለብዎት።\n\nቻናል፦ {CHANNEL_USERNAME}", 
                         reply_markup=markup)
        return

    main_menu(message.chat.id)

def main_menu(chat_id):
    text = "እንኳን ወደ Ethio Free server በደህና መጣችሁ! 🚀\n\nከታች ያሉትን አማራጮች በመጠቀም አገልግሎታችንን ማግኘት ይችላሉ።"
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_p2p = types.InlineKeyboardButton("💸 USDT Buy/Sell (P2P) 💸", callback_data="p2p_trade")
    btn_ads = types.InlineKeyboardButton("📣 ማስታወቂያ ለማሰራት 📣", callback_data="post_ads")
    btn_tutorial = types.InlineKeyboardButton("🔱 Tutorial 🔱", callback_data="tutorial")
    btn_contact = types.InlineKeyboardButton("ጥያቄና ሀሳብ ✉️", callback_data="contact_admin")
    btn_donate = types.InlineKeyboardButton("🔱 Donate 🔱", callback_data="donate")

    markup.add(btn_p2p)
    markup.add(btn_ads, btn_tutorial)
    markup.add(btn_contact, btn_donate)

    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "እባክዎ መጀመሪያ ቻናሉን ይቀላቀሉ!", show_alert=True)

    elif call.data == "p2p_trade":
        msg = bot.send_message(call.message.chat.id, "💰 **የP2P ንግድ**\n\nUSDT መግዛት ወይስ መሸጥ ይፈልጋሉ? የሚፈልጉትን መጠንና አይነት (ለምሳሌ፦ 50 USDT መግዛት እፈልጋለሁ) ብለው እዚህ ይጻፉ።")
        bot.register_next_step_handler(msg, process_trade_request)

    elif call.data == "post_ads":
        msg = bot.send_message(call.message.chat.id, "📣 **ማስታወቂያ**\n\nየማስታወቂያውን ዝርዝር እዚህ ይጻፉ። አድሚን አይቶ ያነጋግርዎታል።")
        bot.register_next_step_handler(msg, process_ads_request)

    elif call.data == "tutorial":
        bot.send_message(call.message.chat.id, "🔱 **Tutorial Section** 🔱\n\nበቅርቡ ጠቃሚ የሆኑ ቲቶሪያሎች እዚህ ይጫናሉ! ይጠብቁን።")

    elif call.data == "contact_admin":
        bot.send_message(call.message.chat.id, "ለማንኛውም ጥያቄ አድሚኑን እዚህ ያግኙ፦ @semir_yusuf")

    elif call.data == "donate":
        bot.send_message(call.message.chat.id, "🙏 ቦቱን ለመርዳት ስለፈለጉ እናመሰግናለን!\n\nየባንክ አካውንት (CBE): `1000...` \n(ቁጥሩን ተጭነው ኮፒ ማድረግ ይችላሉ)")

def process_trade_request(message):
    user = message.from_user
    info = f"🔔 **አዲስ የP2P ጥያቄ!**\n\n👤 ተጠቃሚ: {user.first_name} (@{user.username})\n🆔 ID: `{user.id}`\n💬 መልእክት: {message.text}"
    bot.send_message(ADMIN_ID, info, parse_mode="Markdown")
    bot.reply_to(message, "✅ ጥያቄዎ ለአድሚን ደርሷል። በቅርቡ እናነጋግርዎታለን!")

def process_ads_request(message):
    user = message.from_user
    info = f"🔔 **አዲስ የማስታወቂያ ጥያቄ!**\n\n👤 ተጠቃሚ: {user.first_name} (@{user.username})\n💬 ዝርዝር: {message.text}"
    bot.send_message(ADMIN_ID, info, parse_mode="Markdown")
    bot.reply_to(message, "✅ የማስታወቂያ ጥያቄዎ ደርሷል። እናመሰግናለን!")

if __name__ == "__main__":
    print("ቦቱ በተሳካ ሁኔታ ስራ ጀምሯል...")
    bot.infinity_polling()
