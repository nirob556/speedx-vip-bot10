import os
import sqlite3
import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Configuration
API_ID = 26840974
API_HASH = "7f0ca9899acec0ddd2fa752ee348f717"
BOT_TOKEN = "7820837146:AAHanZ1qy-86DKl-iBzEjjgxGIzBpDdkE_k"
OWNER = "@NIROB_BBZ"
GROUP_LINK = "https://t.me/SPEED_X_OFFICIAL"
VIP_PASSWORD = "fire123"  # Change if needed

# Logging Setup
logging.basicConfig(
    filename="speedx_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client("SPEEDX_ULTIMATE", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Database Setup
conn = sqlite3.connect("speedx.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    language TEXT DEFAULT 'english',
    join_date TEXT,
    last_command TEXT,
    is_vip INTEGER DEFAULT 0
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_users INTEGER DEFAULT 0,
    total_commands INTEGER DEFAULT 0
)
""")
cursor.execute("INSERT OR IGNORE INTO stats (stat_id, total_users, total_commands) VALUES (1, 0, 0)")
conn.commit()

# Language Texts
LANGUAGES = {
    'english': {
        'welcome': "🔥 **Welcome to SPEED_X Bot!** 🔥 \n**The Ultimate Group Management Bot** 🚀\nJoin our group and vibe with us! 🌟",
        'group_welcome': "🔥 **SPEED_X Bot added to the group!** 🔥 \n**The Ultimate Group Management Bot** 🚀\nUse /help to see all commands! 🎶",
        'member_welcome': "🎉 Welcome {username} to the group! Let's vibe with SPEED_X Bot! 🔥 Use /help to get started!",
        'help': """🎧 **SPEED_X BOT COMMANDS (English)** 🔥:
/start - Start the bot
/help - Show this help message
/language - Change bot language
/join - Join our awesome group
/stats - Show bot usage stats
/vip [password] - Unlock VIP features
/broadcast [message] - Send broadcast message (Admins only)
/admin - Check bot status (Admins only)""",
        'group_joined': "🎉 Thanks for joining our group! Let's vibe together! 😎",
        'error': "⚠️ Oops! Something went wrong: {}",
        'stats': "📊 **Bot Stats** 🔥\nTotal Users: {}\nTotal Commands: {}",
        'admin_status': "🛠 **Bot Status** 🔥\nActive: Yes\nUsers: {}\nCommands: {}\nUptime: {}",
        'vip_success': "🎉 VIP unlocked! You can now use premium features! 🔥",
        'vip_error': "⚠️ Invalid VIP password! Contact @NIROB_BBZ to get it. 🔥",
        'not_vip': "⚠️ This command is for VIP users only! Unlock with /vip [password] 🔥",
        'broadcast_success': "📢 Broadcast sent successfully! 🔥"
    },
    'bangla': {
        'welcome': "🔥 **SPEED_X বটে স্বাগতম!** 🔥 \n**আলটিমেট গ্রুপ ম্যানেজমেন্ট বট** 🚀\nগ্রুপে যোগ দাও আর মজা শুরু কর! 🌟",
        'group_welcome': "🔥 **SPEED_X বট গ্রুপে যোগ দেওয়া হয়েছে!** 🔥 \n**আলটিমেট গ্রুপ ম্যানেজমেন্ট বট** 🚀\nকমান্ড দেখতে /help ব্যবহার কর! 🎶",
        'member_welcome': "🎉 {username} গ্রুপে স্বাগতম! SPEED_X বটের সাথে মজা কর! 🔥 /help দিয়ে শুরু কর!",
        'help': """🎧 **SPEED_X বট কমান্ড (বাংলা)** 🔥:
/start - বট শুরু কর
/help - এই হেল্প মেসেজ দেখাও
/language - বটের ভাষা পরিবর্তন কর
/join - আমাদের দারুণ গ্রুপে যোগ দাও
/stats - বটের ব্যবহার পরিসংখ্যান দেখাও
/vip [পাসওয়ার্ড] - VIP ফিচার আনলক কর
/broadcast [মেসেজ] - ব্রডকাস্ট মেসেজ পাঠাও (শুধু অ্যাডমিন)
/admin - বটের স্ট্যাটাস চেক কর (শুধু অ্যাডমিন)""",
        'group_joined': "🎉 গ্রুপে যোগ দেওয়ার জন্য ধন্যবাদ! এখন মজা করি! 😎",
        'error': "⚠️ ওহো! কিছু ভুল হয়েছে: {}",
        'stats': "📊 **বটের পরিসংখ্যান** 🔥\nমোট ইউজার: {}\nমোট কমান্ড: {}",
        'admin_status': "🛠 **বটের স্ট্যাটাস** 🔥\nসক্রিয়: হ্যাঁ\nইউজার: {}\nকমান্ড: {}\nআপটাইম: {}",
        'vip_success': "🎉 VIP আনলক হয়েছে! এখন প্রিমিয়াম ফিচার ব্যবহার করতে পারবে! 🔥",
        'vip_error': "⚠️ ভুল VIP পাসওয়ার্ড! @NIROB_BBZ এর সাথে যোগাযোগ কর। 🔥",
        'not_vip': "⚠️ এই কমান্ড শুধু VIP ইউজারদের জন্য! /vip [পাসওয়ার্ড] দিয়ে আনলক কর 🔥",
        'broadcast_success': "📢 ব্রডকাস্ট সফলভাবে পাঠানো হয়েছে! 🔥"
    },
    'hindi': {
        'welcome': "🔥 **SPEED_X बॉट में स्वागत है!** 🔥 \n**अल्टीमेट ग्रुप मैनेजमेंट बॉट** 🚀\nहमारे ग्रुप में शामिल हों और मस्ती शुरू करें! 🌟",
        'group_welcome': "🔥 **SPEED_X बॉट ग्रुप में जोड़ा गया!** 🔥 \n**अल्टीमेट ग्रुप मैनेजमेंट बॉट** 🚀\nकमांड देखने के लिए /help का उपयोग करें! 🎶",
        'member_welcome': "🎉 {username} ग्रुप में स्वागत है! SPEED_X बॉट के साथ मस्ती करें! 🔥 /help से शुरू करें!",
        'help': """🎧 **SPEED_X बॉट कमांड (हिंदी)** 🔥:
/start - बॉट शुरू करें
/help - यह मदद संदेश दिखाएं
/language - बॉट भाषा बदलें
/join - हमारे शानदार ग्रुप में शामिल हों
/stats - बॉट उपयोग आँकड़े देखें
/vip [पासवर्ड] - VIP फीचर्स अनलॉक करें
/broadcast [मैसेज] - ब्रॉडकास्ट मैसेज भेजें (केवल एडमिन)
/admin - बॉट स्टेटस चेक करें (केवल एडमिन)""",
        'group_joined': "🎉 ग्रुप में शामिल होने के लिए धन्यवाद! चलो मस्ती करें! 😎",
        'error': "⚠️ ओहो! कुछ गलत हुआ: {}",
        'stats': "📊 **बॉट आँकड़े** 🔥\nकुल उपयोगकर्ता: {}\nकुल कमांड: {}",
        'admin_status': "🛠 **बॉट स्टेटस** 🔥\nसक्रिय: हाँ\nउपयोगकर्ता: {}\nकमांड: {}\nअपटाइम: {}",
        'vip_success': "🎉 VIP अनलॉक हुआ! अब आप प्रीमियम फीचर्स का उपयोग कर सकते हैं! 🔥",
        'vip_error': "⚠️ गलत VIP पासवर्ड! @NIROB_BBZ से संपर्क करें। 🔥",
        'not_vip': "⚠️ यह कमांड केवल VIP उपयोगकर्ताओं के लिए है! /vip [पासवर्ड] से अनलॉक करें 🔥",
        'broadcast_success': "📢 ब्रॉडकास्ट सफलतापूर्वक भेजा गया! 🔥"
    }
}

# Get User Language
def get_lang(user_id):
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    lang = cursor.fetchone()
    return lang[0] if lang else 'english'

# Check VIP Status
def is_vip(user_id):
    cursor.execute("SELECT is_vip FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Save User Info
def save_user(user_id, username, lang='english', command=None, is_vip=0):
    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, username, language, join_date, last_command, is_vip)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, lang, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command, is_vip))
    cursor.execute("UPDATE stats SET total_users = (SELECT COUNT(*) FROM users) WHERE stat_id = 1")
    cursor.execute("UPDATE stats SET total_commands = total_commands + 1 WHERE stat_id = 1")
    conn.commit()
    logger.info(f"User {user_id} ({username}) saved with language {lang}, command {command}, vip {is_vip}")

# Get Stats
def get_stats():
    cursor.execute("SELECT total_users, total_commands FROM stats WHERE stat_id = 1")
    return cursor.fetchone()

# Bot Added to Group
@app.on_message(filters.new_chat_members)
async def group_welcome(_, m: Message):
    try:
        bot_id = (await app.get_me()).id
        if bot_id in [member.id for member in m.new_chat_members]:
            lang = 'english'
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Our Group 🔥", url=GROUP_LINK)]
            ])
            await m.reply(LANGUAGES[lang]['group_welcome'], reply_markup=buttons)
            logger.info(f"Bot added to group {m.chat.id}")
    except Exception as e:
        logger.error(f"Error in group_welcome: {str(e)}")

# New Member Welcome
@app.on_message(filters.new_chat_members & ~filters.bot)
async def member_welcome(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        for member in m.new_chat_members:
            await m.reply(LANGUAGES[lang]['member_welcome'].format(username=member.username or member.first_name))
            logger.info(f"New member {member.id} welcomed in group {m.chat.id}")
    except Exception as e:
        logger.error(f"Error in member_welcome: {str(e)}")

# Start Command
@app.on_message(filters.command("start") & filters.private)
async def start_command(_, m: Message):
    try:
        user_id = m.from_user.id
        username = m.from_user.username or m.from_user.first_name
        lang = get_lang(user_id)
        save_user(user_id, username, lang, "start")
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Our Group 🔥", url=GROUP_LINK)],
            [InlineKeyboardButton("English", callback_data="lang_english"),
             InlineKeyboardButton("বাংলা", callback_data="lang_bangla"),
             InlineKeyboardButton("हिंदी", callback_data="lang_hindi")]
        ])
        await m.reply(LANGUAGES[lang]['welcome'], reply_markup=buttons)
        logger.info(f"User {user_id} started the bot")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in start_command: {str(e)}")

# Help Command
@app.on_message(filters.command("help") & filters.group)
async def help_command(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        save_user(m.from_user.id, m.from_user.username or m.from_user.first_name, lang, "help")
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Group 🔥", url=GROUP_LINK)]
        ])
        await m.reply(LANGUAGES[lang]['help'], reply_markup=buttons)
        logger.info(f"User {m.from_user.id} used help command in group {m.chat.id}")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in help_command: {str(e)}")

# Join Group Command
@app.on_message(filters.command("join"))
async def join_command(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        save_user(m.from_user.id, m.from_user.username or m.from_user.first_name, lang, "join")
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Now 🔥", url=GROUP_LINK)]
        ])
        await m.reply(LANGUAGES[lang]['group_joined'], reply_markup=buttons)
        logger.info(f"User {m.from_user.id} used join command")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in join_command: {str(e)}")

# Language Selector
@app.on_message(filters.command("language"))
async def language_command(_, m: Message):
    try:
        save_user(m.from_user.id, m.from_user.username or m.from_user.first_name, get_lang(m.from_user.id), "language")
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("English", callback_data="lang_english"),
             InlineKeyboardButton("বাংলা", callback_data="lang_bangla"),
             InlineKeyboardButton("हिंदी", callback_data="lang_hindi")]
        ])
        await m.reply("🔥 **Select Language / ভাষা বাছাই করুন / भाषा चुनें:** 🔥", reply_markup=buttons)
        logger.info(f"User {m.from_user.id} used language command")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in language_command: {str(e)}")

# Language Callback Handler
@app.on_callback_query(filters.regex(r"^lang_"))
async def language_callback(_, query):
    try:
        lang = query.data.split("_")[1]
        user_id = query.from_user.id
        username = query.from_user.username or query.from_user.first_name
        save_user(user_id, username, lang, "language_callback")
        await query.message.edit_text(f"Language set to {lang.capitalize()}! / ভাষা {lang} এ সেট করা হয়েছে! / भाषा {lang} में सेट की गई! 🔥")
        await query.answer()
        logger.info(f"User {user_id} changed language to {lang}")
    except Exception as e:
        lang = get_lang(query.from_user.id)
        await query.message.edit_text(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in language_callback: {str(e)}")

# VIP Command
@app.on_message(filters.command("vip"))
async def vip_command(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        user_id = m.from_user.id
        username = m.from_user.username or m.from_user.first_name
        if len(m.text.split()) < 2:
            await m.reply(LANGUAGES[lang]['error'].format("Please provide the VIP password"))
            return
        password = m.text.split(maxsplit=1)[1]
        if password == VIP_PASSWORD:
            save_user(user_id, username, lang, "vip", is_vip=1)
            await m.reply(LANGUAGES[lang]['vip_success'])
            logger.info(f"User {user_id} unlocked VIP")
        else:
            await m.reply(LANGUAGES[lang]['vip_error'])
            logger.warning(f"User {user_id} failed VIP unlock attempt")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in vip_command: {str(e)}")

# Broadcast Command
@app.on_message(filters.command("broadcast") & filters.group)
async def broadcast_command(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        user_id = m.from_user.id
        member = await app.get_chat_member(m.chat.id, user_id)
        if member.status not in ["creator", "administrator"]:
            await m.reply(LANGUAGES[lang]['error'].format("Only admins can use this command"))
            return
        save_user(user_id, m.from_user.username or m.from_user.first_name, lang, "broadcast")
        if len(m.text.split()) < 2:
            await m.reply(LANGUAGES[lang]['error'].format("Please provide a broadcast message"))
            return
        message = m.text.split(maxsplit=1)[1]
        await m.reply(f"📢 {message} 🔥")
        await m.reply(LANGUAGES[lang]['broadcast_success'])
        logger.info(f"Admin {user_id} sent broadcast in group {m.chat.id}: {message}")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in broadcast_command: {str(e)}")

# Admin Command
@app.on_message(filters.command("admin") & filters.group)
async def admin_command(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        save_user(m.from_user.id, m.from_user.username or m.from_user.first_name, lang, "admin")
        
        # Check if user is admin
        member = await app.get_chat_member(m.chat.id, m.from_user.id)
        if member.status not in ["creator", "administrator"]:
            await m.reply(LANGUAGES[lang]['error'].format("Only admins can use this command"))
            return
        
        total_users, total_commands = get_stats()
        uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await m.reply(LANGUAGES[lang]['admin_status'].format(total_users, total_commands, uptime))
        logger.info(f"Admin {m.from_user.id} checked bot status in group {m.chat.id}")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in admin_command: {str(e)}")

# Stats Command
@app.on_message(filters.command("stats"))
async def stats_command(_, m: Message):
    try:
        lang = get_lang(m.from_user.id)
        save_user(m.from_user.id, m.from_user.username or m.from_user.first_name, lang, "stats")
        total_users, total_commands = get_stats()
        await m.reply(LANGUAGES[lang]['stats'].format(total_users, total_commands))
        logger.info(f"User {m.from_user.id} checked stats")
    except Exception as e:
        lang = get_lang(m.from_user.id)
        await m.reply(LANGUAGES[lang]['error'].format(str(e)))
        logger.error(f"Error in stats_command: {str(e)}")

# Run the Bot
if __name__ == "__main__":
    print("🔥 SPEED_X BOT STARTED! 🚀")
    logger.info("Bot started")
    try:
        app.run()
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
