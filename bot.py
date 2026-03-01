import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 123456789  # <-- put your real Telegram ID

if not TOKEN:
    raise RuntimeError("TOKEN not set in environment variables!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    # Auto reply in private chat
    if update.message.chat.type == "private":
        await update.message.reply_text("Thanks for messaging me!")

    # Forward everything to admin
    try:
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )
    except Exception as e:
        logging.error(f"Forward error: {e}")


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await update.message.reply_text(f"Welcome {member.first_name} 🎉")
            try:
                await context.bot.send_message(
                    chat_id=member.id,
                    text="Welcome to the group! Please read the rules."
                )
            except Exception as e:
                logging.error(f"Private welcome error: {e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    app.run_polling()


if __name__ == "__main__":
    main()
