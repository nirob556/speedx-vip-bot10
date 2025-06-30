import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown

TOKEN = "8124758296:AAEaOk9xOPqUyP4dOyrB8D6zjOpCowbma0s"
VIP_PASSWORD = "SPEED_X_VIP"
GROUP_CHAT_ID = -1002611442542  # তোমার গ্রুপ আইডি বসাও
BOT_USERNAME = "dhcjcjn_hdjd101_bot"  # বট ইউজারনেম (বিনা @)

BD_TZ = pytz.timezone("Asia/Dhaka")

user_data = {
    "logged_in": False,
    "send_time": "08:00",
    "daily_message": "🔔 This is your daily VIP message from SPEED_X!",
    "last_sent": None
}

WELCOME_TEXT = (
    "*✨ 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝘁𝗼 𝗩𝗜𝗣 𝗕𝗼𝘁 𝘄𝗶𝘁𝗵 𝗦𝗣𝗘𝗘𝗗_𝗫 ✨*\n\n"
    "╭━━━━━━━★━━━━━━━╮\n"
    "┃   ⚡ 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 𝗦𝗣𝗘𝗘𝗗_𝗫 ⚡\n"
    "╰━━━━━━━★━━━━━━━╯\n\n"
    "🎯 𝗩𝗜𝗣 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦:\n"
    "➤ 𝗔𝘂𝘁𝗼 𝗗𝗮𝗶𝗹𝘆 𝗠𝗲𝘀𝘀𝗮𝗴𝗲\n"
    "➤ 𝗖𝘂𝘀𝘁𝗼𝗺 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗖𝗼𝗻𝘁𝗿𝗼𝗹\n"
    "➤ 𝗦𝘁𝘆𝗹𝗶𝘀𝗵 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆\n"
    "➤ 𝗚𝗿𝗼𝘂𝗽 𝗠𝗲𝘀𝘀𝗮𝗴𝗶𝗻𝗴 𝗦𝘂𝗽𝗽𝗼𝗿𝘁\n\n"
    "🔑 𝗟𝗼𝗴𝗶𝗻: /login SPEED_X_VIP\n"
    "ℹ️ 𝗨𝘀𝗲 /help 𝘁𝗼 𝘃𝗶𝗲𝘄 𝗮𝗹𝗹 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀\n\n"
    "👑 *𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗯𝘆* `SPEED_X`"
)

HELP_TEXT = (
    "*🧭 VIP Bot Commands:*\n\n"
    "`/login password` – Login as VIP\n"
    "`/settime HH:MM` – Set daily time (Bangladesh time)\n"
    "`/setmessage your_message` – Set daily message\n"
    "`/sendmessage your_message` – Send custom message now\n"
    "`/status` – Show last message time"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Add Me To Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    ]])
    safe_text = escape_markdown(WELCOME_TEXT, version=2)
    await update.message.reply_text(
        safe_text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    safe_text = escape_markdown(HELP_TEXT, version=2)
    await update.message.reply_text(safe_text, parse_mode=ParseMode.MARKDOWN_V2)

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Use: /login PASSWORD")
        return
    if context.args[0] == VIP_PASSWORD:
        user_data["logged_in"] = True
        await update.message.reply_text("✅ VIP Access Granted.")
    else:
        await update.message.reply_text("❌ Wrong password.")

async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data["logged_in"]:
        await update.message.reply_text("❌ Please login first.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("❌ Usage: /settime HH:MM (Bangladesh time)")
        return
    time_str = context.args[0]
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        user_data["send_time"] = time_str
        await update.message.reply_text(f"✅ Time set to {time_str} (Bangladesh time)")
        await schedule_daily_message(update, context)
    except:
        await update.message.reply_text("❌ Invalid time format! Use HH:MM (24-hour)")

async def setmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data["logged_in"]:
        await update.message.reply_text("❌ Please login first.")
        return
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("❌ Usage: /setmessage your_message")
        return
    user_data["daily_message"] = msg
    await update.message.reply_text("✅ Daily message updated!")

async def sendmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data["logged_in"]:
        await update.message.reply_text("❌ Please login first.")
        return
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("❌ Usage: /sendmessage your_message")
        return
    now = datetime.datetime.now(BD_TZ)
    user_data["last_sent"] = now
    safe_msg = escape_markdown(msg, version=2)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=safe_msg, parse_mode=ParseMode.MARKDOWN_V2)
    await update.message.reply_text("✅ Sent to group!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last = user_data["last_sent"]
    if last:
        await update.message.reply_text(f"📅 Last message: {last.strftime('%Y-%m-%d')} ⏰ {last.strftime('%H:%M:%S')}")
    else:
        await update.message.reply_text("ℹ️ No message sent yet.")

async def scheduled_daily_message(context: ContextTypes.DEFAULT_TYPE):
    if not user_data["logged_in"]:
        return
    safe_msg = escape_markdown(user_data["daily_message"], version=2)
    now = datetime.datetime.now(BD_TZ)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=safe_msg, parse_mode=ParseMode.MARKDOWN_V2)
    user_data["last_sent"] = now

async def schedule_daily_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job_queue = context.job_queue
    current_jobs = job_queue.get_jobs_by_name("daily_message_job")
    for job in current_jobs:
        job.schedule_removal()

    hour, minute = map(int, user_data["send_time"].split(":"))

    job_queue.run_daily(
        scheduled_daily_message,
        time=datetime.time(hour=hour, minute=minute, tzinfo=BD_TZ),
        name="daily_message_job",
        context=None
    )
    await update.message.reply_text(f"✅ Scheduled daily message at {user_data['send_time']} Bangladesh time.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("settime", settime))
    app.add_handler(CommandHandler("setmessage", setmessage))
    app.add_handler(CommandHandler("sendmessage", sendmessage))
    app.add_handler(CommandHandler("status", status))

    print("🚀 SPEED_X VIP Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()