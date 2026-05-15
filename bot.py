import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os

# ==================== CONFIG ====================
BOT_TOKEN = "8686967610:AAFE1B_hTR6JMljJQbnntitty842ZclQN1g"  # @BotFather ከ ያወጣኸውን Token እዚህ ያስቀምጥ
CHANNEL_USERNAME = "@unlimited_datas"  # የ Channel username እዚህ ያስቀምጥ
ADMIN_ID = 123456789  # የ Admin Telegram ID እዚህ ያስቀምጥ

bot = telebot.TeleBot8686967610:AAFE1B_hTR6JMljJQbnntitty842ZclQN1g

# ==================== DATABASE (JSON) ====================
DB_FILE = "users.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(user_id):
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"balance": 0, "usdt": 0, "gmail_balance": 0}
        save_db(db)
    return db[uid]

def update_user(user_id, data):
    db = load_db()
    uid = str(user_id)
    db[uid] = data
    save_db(db)

# ==================== CHANNEL CHECK ====================
def check_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def join_required_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Channel Join አድርግ", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
    markup.add(InlineKeyboardButton("🔄 Join አደረግሁ - ቀጥል", callback_data="check_join"))
    return markup

# ==================== MAIN MENU ====================
def main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🐝 Gmail Farm Withdraw 🐝"),
        KeyboardButton("🐝 USDT Buy/Sell 🐝"),
        KeyboardButton("📢 ማስታወቂያ ለማሰራት 📢"),
        KeyboardButton("📚 Fx Course"),
        KeyboardButton("🔱 Premium File (7Day's) 🔱"),
        KeyboardButton("🐱 ጥያቄ እና ሂሳብ መስጫ 📧"),
        KeyboardButton("🔱 Tutorial 🔱"),
        KeyboardButton("🔱 Donate 🔱")
    )
    return markup

# ==================== START ====================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not check_joined(user_id):
        bot.send_message(
            user_id,
            f"👋 ሰላም {first_name}!\n\n🔱 MR Crypto Bot ን ለመጠቀም ቅድሚያ Channel ን Join አድርግ 👇",
            reply_markup=join_required_markup()
        )
        return

    get_user(user_id)  # Initialize user
    bot.send_message(
        user_id,
        f"👋 ሰላም {first_name}! እንኳን ወደ MR Crypto Bot ደህና መጣህ! 🎉\n\n⬇️ ከታች ያለውን Menu ተጠቀም:",
        reply_markup=main_menu_markup()
    )

# ==================== CHECK JOIN CALLBACK ====================
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    user_id = call.from_user.id
    first_name = call.from_user.first_name
    if check_joined(user_id):
        get_user(user_id)
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=f"✅ አመሰግናለሁ! እንኳን ደህና መጣህ {first_name}!"
        )
        bot.send_message(user_id, "⬇️ ከታች ያለውን Menu ተጠቀም:", reply_markup=main_menu_markup())
    else:
        bot.answer_callback_query(call.id, "❌ Channel አልተቀላቀልክም! እባክህ Join አድርግ።", show_alert=True)

# ==================== GMAIL FARM WITHDRAW ====================
@bot.message_handler(func=lambda m: m.text == "🐝 Gmail Farm Withdraw 🐝")
def gmail_withdraw(message):
    user_id = message.from_user.id
    if not check_joined(user_id):
        bot.send_message(user_id, "❌ Channel Join አድርግ!", reply_markup=join_required_markup())
        return
    user = get_user(user_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💰 ቀሪ ሂሳብ አሳይ", callback_data="gmail_balance"))
    markup.add(InlineKeyboardButton("📤 Withdraw ጠይቅ", callback_data="gmail_withdraw_req"))
    bot.send_message(
        user_id,
        f"🐝 Gmail Farm Withdraw\n\n"
        f"💰 የአሁኑ ሂሳብ: {user.get('gmail_balance', 0)} ETB\n\n"
        f"ምን ማድረግ ትፈልጋለህ?",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "gmail_balance")
def gmail_balance(call):
    user = get_user(call.from_user.id)
    bot.answer_callback_query(call.id, f"💰 ሂሳብህ: {user.get('gmail_balance', 0)} ETB", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "gmail_withdraw_req")
def gmail_withdraw_req(call):
    user = get_user(call.from_user.id)
    if user.get("gmail_balance", 0) <= 0:
        bot.answer_callback_query(call.id, "❌ በቂ ሂሳብ የለህም!", show_alert=True)
        return
    bot.send_message(call.from_user.id, "📤 Withdraw ለ Admin ተልኳል! በቅርቡ ይደርስሃል። ✅")
    bot.send_message(ADMIN_ID, f"⚠️ Withdraw Request!\nUser: {call.from_user.first_name}\nID: {call.from_user.id}\nGmail Balance: {user.get('gmail_balance', 0)} ETB")

# ==================== USDT BUY/SELL ====================
@bot.message_handler(func=lambda m: m.text == "🐝 USDT Buy/Sell 🐝")
def usdt_menu(message):
    user_id = message.from_user.id
    if not check_joined(user_id):
        bot.send_message(user_id, "❌ Channel Join አድርግ!", reply_markup=join_required_markup())
        return
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🟢 Buy USDT", callback_data="usdt_buy"),
        InlineKeyboardButton("🔴 Sell USDT", callback_data="usdt_sell")
    )
    markup.add(InlineKeyboardButton("💰 ሂሳብ አሳይ", callback_data="usdt_balance"))
    bot.send_message(
        user_id,
        "🐝 USDT Buy/Sell\n\n💱 አሁናዊ ዋጋ:\n🟢 Buy: 1 USDT = 125 ETB\n🔴 Sell: 1 USDT = 123 ETB",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "usdt_buy")
def usdt_buy(call):
    msg = bot.send_message(call.from_user.id, "💰 ስንት USDT መግዛት ትፈልጋለህ? (ቁጥር ተፃፍ):")
    bot.register_next_step_handler(msg, process_usdt_buy)

def process_usdt_buy(message):
    try:
        amount = float(message.text)
        total = amount * 125
        user = get_user(message.from_user.id)
        user["usdt"] = user.get("usdt", 0) + amount
        update_user(message.from_user.id, user)
        bot.send_message(message.chat.id, f"✅ {amount} USDT ለ {total} ETB ለመግዛት ጥያቄህ ተልኳል!\nAdmin ያረጋግጣል።")
        bot.send_message(ADMIN_ID, f"💰 USDT Buy Request!\nUser: {message.from_user.first_name}\nID: {message.from_user.id}\nAmount: {amount} USDT = {total} ETB")
    except:
        bot.send_message(message.chat.id, "❌ ቁጥር ብቻ ተፃፍ!")

@bot.callback_query_handler(func=lambda call: call.data == "usdt_sell")
def usdt_sell(call):
    msg = bot.send_message(call.from_user.id, "💰 ስንት USDT መሸጥ ትፈልጋለህ? (ቁጥር ተፃፍ):")
    bot.register_next_step_handler(msg, process_usdt_sell)

def process_usdt_sell(message):
    try:
        amount = float(message.text)
        user = get_user(message.from_user.id)
        if user.get("usdt", 0) < amount:
            bot.send_message(message.chat.id, "❌ በቂ USDT የለህም!")
            return
        total = amount * 123
        user["usdt"] -= amount
        update_user(message.from_user.id, user)
        bot.send_message(message.chat.id, f"✅ {amount} USDT ለ {total} ETB ለመሸጥ ጥያቄህ ተልኳል!")
        bot.send_message(ADMIN_ID, f"💰 USDT Sell Request!\nUser: {message.from_user.first_name}\nID: {message.from_user.id}\nAmount: {amount} USDT = {total} ETB")
    except:
        bot.send_message(message.chat.id, "❌ ቁጥር ብቻ ተፃፍ!")

@bot.callback_query_handler(func=lambda call: call.data == "usdt_balance")
def usdt_balance(call):
    user = get_user(call.from_user.id)
    bot.answer_callback_query(call.id, f"💰 USDT ሂሳብ: {user.get('usdt', 0)} USDT", show_alert=True)

# ==================== ADVERTISEMENT ====================
@bot.message_handler(func=lambda m: m.text == "📢 ማስታወቂያ ለማሰራት 📢")
def advertisement(message):
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 ማስታወቂያ ላክ", callback_data="send_ad"))
    markup.add(InlineKeyboardButton("💰 ዋጋ ዝርዝር", callback_data="ad_price"))
    bot.send_message(
        user_id,
        "📢 ማስታወቂያ ለማሰራት:\n\n"
        "💰 ዋጋዎች:\n"
        "• 1 ቀን - 50 ETB\n"
        "• 3 ቀን - 120 ETB\n"
        "• 7 ቀን - 250 ETB\n\n"
        "Admin ያስተናግዳል።",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "send_ad")
def send_ad(call):
    msg = bot.send_message(call.from_user.id, "📢 ማስታወቂያህን ፃፍ (ጽሁፍ፣ ፎቶ፣ ወዘተ ልካ):")
    bot.register_next_step_handler(msg, process_ad)

def process_ad(message):
    bot.send_message(message.chat.id, "✅ ማስታወቂያህ ለ Admin ተልኳል! በቅርቡ ይደርሳሃል።")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📢 Ad Request from:\nName: {message.from_user.first_name}\nID: {message.from_user.id}")

@bot.callback_query_handler(func=lambda call: call.data == "ad_price")
def ad_price(call):
    bot.answer_callback_query(call.id, "1 ቀን=50 ETB | 3 ቀን=120 ETB | 7 ቀን=250 ETB", show_alert=True)

# ==================== FX COURSE ====================
@bot.message_handler(func=lambda m: m.text == "📚 Fx Course")
def fx_course(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📖 Course ይግዛ", callback_data="buy_course"))
    bot.send_message(
        message.chat.id,
        "📚 Fx Course\n\n"
        "✅ ምን ይማራሉ:\n"
        "• Forex Basics\n"
        "• Chart Reading\n"
        "• Risk Management\n"
        "• Live Trading Tips\n\n"
        "💰 ዋጋ: 500 ETB\n\n"
        "Admin ያስተናግዳል።",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "buy_course")
def buy_course(call):
    bot.send_message(call.from_user.id, "✅ Course ለመግዛት ጥያቄህ ለ Admin ተልኳል!")
    bot.send_message(ADMIN_ID, f"📚 Course Buy Request!\nUser: {call.from_user.first_name}\nID: {call.from_user.id}")

# ==================== PREMIUM FILE ====================
@bot.message_handler(func=lambda m: m.text == "🔱 Premium File (7Day's) 🔱")
def premium_file(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 Premium ግዛ", callback_data="buy_premium"))
    bot.send_message(
        message.chat.id,
        "🔱 Premium File (7 Days)\n\n"
        "✅ ምን ያካትታል:\n"
        "• Exclusive Trading Signals\n"
        "• Premium PDF Files\n"
        "• VIP Group Access\n"
        "• Daily Market Analysis\n\n"
        "💰 ዋጋ: 200 ETB / 7 ቀን\n\n"
        "Payment ካደረጉ በኋላ Admin ያረጋግጣል።",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "buy_premium")
def buy_premium(call):
    bot.send_message(call.from_user.id, "✅ Premium ጥያቄህ ለ Admin ተልኳል! Payment ካደረጉ Admin ያረጋግጣል።")
    bot.send_message(ADMIN_ID, f"💎 Premium Buy Request!\nUser: {call.from_user.first_name}\nID: {call.from_user.id}")

# ==================== Q&A / CONTACT ====================
@bot.message_handler(func=lambda m: m.text == "🐱 ጥያቄ እና ሂሳብ መስጫ 📧")
def qa_contact(message):
    msg = bot.send_message(message.chat.id, "❓ ጥያቄህን ወይም መልእክትህን ፃፍ - ለ Admin እንልካለን:")
    bot.register_next_step_handler(msg, process_question)

def process_question(message):
    bot.send_message(message.chat.id, "✅ ጥያቄህ ለ Admin ተልኳል! በቅርቡ ይመልሳሉ።")
    bot.send_message(ADMIN_ID, f"❓ Question from:\nName: {message.from_user.first_name}\nID: {message.from_user.id}\n\nMessage: {message.text}")

# ==================== TUTORIAL ====================
@bot.message_handler(func=lambda m: m.text == "🔱 Tutorial 🔱")
def tutorial(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("▶️ Tutorial 1 - መጀመሪያ", callback_data="tut_1"))
    markup.add(InlineKeyboardButton("▶️ Tutorial 2 - USDT", callback_data="tut_2"))
    markup.add(InlineKeyboardButton("▶️ Tutorial 3 - Gmail Farm", callback_data="tut_3"))
    bot.send_message(message.chat.id, "🔱 Tutorial ዝርዝር:\n\nየሚፈልጉትን ይምረጡ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tut_"))
def show_tutorial(call):
    tutorials = {
        "tut_1": "📖 Tutorial 1 - መጀመሪያ\n\n1. Bot ን /start ጀምር\n2. Channel Join አድርግ\n3. Menu ተጠቀም\n4. Admin ያስተናግዳል",
        "tut_2": "📖 Tutorial 2 - USDT\n\n1. USDT Buy/Sell ጫን\n2. Buy ወይም Sell ምረጥ\n3. መጠን ፃፍ\n4. Admin ያረጋግጣል\n5. Transfer ይደረጋል",
        "tut_3": "📖 Tutorial 3 - Gmail Farm\n\n1. Gmail Farm Withdraw ጫን\n2. ሂሳብ ይሳያል\n3. Withdraw ጠይቅ\n4. Admin ይልካል"
    }
    bot.answer_callback_query(call.id)
    bot.send_message(call.from_user.id, tutorials.get(call.data, "Tutorial አልተገኘም"))

# ==================== DONATE ====================
@bot.message_handler(func=lambda m: m.text == "🔱 Donate 🔱")
def donate(message):
    bot.send_message(
        message.chat.id,
        "🔱 Donate\n\n"
        "💙 Bot ን ለመደገፍ:\n\n"
        "📱 CBE: 1000XXXXXXXX\n"
        "📱 Telebirr: 09XXXXXXXX\n"
        "💱 USDT (TRC20): Txxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n"
        "አመሰግናለሁ! 🙏"
    )

# ==================== ADMIN PANEL ====================
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Admin ብቻ ነው!")
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📊 ተጠቃሚዎች ቁጥር", callback_data="admin_users"))
    markup.add(InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"))
    markup.add(InlineKeyboardButton("💰 ሂሳብ ጨምር", callback_data="admin_add_balance"))
    bot.send_message(message.chat.id, "👑 Admin Panel:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def admin_users(call):
    if call.from_user.id != ADMIN_ID:
        return
    db = load_db()
    bot.answer_callback_query(call.id, f"👥 ጠቅላላ ተጠቃሚዎች: {len(db)}", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def admin_broadcast(call):
    if call.from_user.id != ADMIN_ID:
        return
    msg = bot.send_message(call.from_user.id, "📢 ለሁሉም ልካ ለሚፈልጉት መልእክት ፃፍ:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    db = load_db()
    success = 0
    for uid in db.keys():
        try:
            bot.send_message(int(uid), f"📢 Admin Message:\n\n{message.text}")
            success += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ {success} ተጠቃሚዎች ደረሳቸው!")

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_balance")
def admin_add_balance(call):
    if call.from_user.id != ADMIN_ID:
        return
    msg = bot.send_message(call.from_user.id, "💰 User ID እና መጠን ፃፍ (format: 12345678 500):")
    bot.register_next_step_handler(msg, process_add_balance)

def process_add_balance(message):
    try:
        parts = message.text.split()
        uid = parts[0]
        amount = float(parts[1])
        user = get_user(uid)
        user["gmail_balance"] = user.get("gmail_balance", 0) + amount
        update_user(uid, user)
        bot.send_message(message.chat.id, f"✅ {amount} ETB ለ User {uid} ተጨምሯል!")
        bot.send_message(int(uid), f"💰 {amount} ETB ሂሳብህ ላይ ተጨምሯል! ✅")
    except:
        bot.send_message(message.chat.id, "❌ Format ስህተት! format: 12345678 500")

# ==================== RUN BOT ====================
print("🤖 MR Crypto Bot እየሰራ ነው...")
bot.polling(none_stop=True)
