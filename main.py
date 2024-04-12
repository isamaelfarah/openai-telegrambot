#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ForceReply, Update
import logging
import api.ai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_API = os.getenv("BOT_API")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}! Nice to meet you.",
        reply_markup=ForceReply(selective=True),
    )
    help_command(update, context)


def help_command(update: Update, context) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Reply to my message to get started!")


def image_command(update: Update, context) -> None:
    if len(update.message.text) <= 6:
        update.message.reply_markdown_v2("Correct syntax to generate an image is,\n`/image a sweet cat is eating a pumpkin`")
    else:
        update.message.reply_text("Generating an image...")
        ai_reply = api.ai.ai_img_generation(update.message.text[7:], update.message.chat.type)
        update.message.reply_markdown_v2(f"Here's your [image]({ai_reply}).")


def echo(update: Update, context) -> None:
    """Echo the user message."""
    ai_reply_text_message = api.ai.ai_completion(update.message.text, update.message.chat.type).strip("\n")
    update.message.reply_text(ai_reply_text_message)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_API)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("image", image_command))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()


if __name__ == "__main__":
    main()
