import asyncio
from datetime import datetime, time, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
from sheet_utils import log_task, get_daily_summary, get_weekly_summary, get_all_user_ids
from roasts import get_roast_for_task, get_roast_for_summary

#Command Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome Akhil!\n"
        "Use the following commands to log your tasks:\n"
        "/done <task> ✅\n"
        "/progress <task> 🟡\n"
        "/missed <task> ❌\n"
        "/weekly 📊 See your last 7-day report\n"
        "/myid 📲 Get your Telegram ID"
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 Your Telegram ID is: `{update.effective_user.id}`",
        parse_mode='Markdown'
    )

async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE, status: str):
    user_id = str(update.effective_user.id)
    task = " ".join(context.args).strip()

    if not task:
        await update.message.reply_text("⚠️ Please include a task description.")
        return

    # Log the task to Google Sheet
    log_task(user_id, status, task)

    # Send confirmation + roast
    emojis = {"done": "✅", "progress": "🟡", "missed": "❌"}
    status_msg = f"{emojis[status]} {status.upper()} logged: {task}"
    roast = get_roast_for_task(status)

    await update.message.reply_text(f"{status_msg}\n\n{roast}")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_task(update, context, "done")

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_task(update, context, "progress")

async def missed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_task(update, context, "missed")

async def weekly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    summary, streak = get_weekly_summary(user_id)

    msg = "📆 *Your Weekly Summary (Last 7 Days)*\n\n"
    for day, data in sorted(summary.items(), reverse=True):
        msg += (
            f"🗓️ {day}:\n"
            f"  ✅ Done: {data['done']}\n"
            f"  🟡 Progress: {data['progress']}\n"
            f"  ❌ Missed: {data['missed']}\n\n"
        )
    msg += f"🔥 *Current Streak:* {streak} day(s) with at least 1 task done!"
    await update.message.reply_text(msg, parse_mode='Markdown')

#Daily Summary Scheduler

async def send_daily_summary(app):
    for user_id in get_all_user_ids():
        try:
            summary = get_daily_summary(user_id)
            if summary:
                roast = get_roast_for_summary(summary)
                full_msg = f"📊 *Your Daily Summary*\n\n{summary}\n\n{roast}"
                await app.bot.send_message(chat_id=user_id, text=full_msg, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ Error sending summary to {user_id}: {e}")

async def schedule_daily_summary(app):
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(22, 0))  # 10:00 PM
        if now >= target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        print(f"⏰ Waiting {int(wait_seconds)} seconds until next summary...")
        await asyncio.sleep(wait_seconds)
        await send_daily_summary(app)

#Main Function

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("progress", progress))
    app.add_handler(CommandHandler("missed", missed))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("myid", myid))

    asyncio.create_task(schedule_daily_summary(app))

    print("🤖 AkhilBot Phase 4 running with instant roasts + summary + streaks...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
