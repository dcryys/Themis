#!/usr/bin/env python3
"""
Goddess Themis Telegram bot
Serving justice to the world
(c) ????
"""

import os
import sys
#  pip install python-telegram-bot --upgrade
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = ""

"""
Read telegram token from .credentials.txt
Keep this file secret, never add confidential information to programs or git
Attention on file .credentials.txt, it should be in .gitignore
"""
def read_credentials():
    global TELEGRAM_TOKEN
    with open(".credentials.txt", "r") as f:
        TELEGRAM_TOKEN = f.readline().strip()
"""
Telegram bot answer to /hello command
"""
def hello_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}!')

"""
Main body of Telegram bot handling loop
"""
def telegram_func():
    global TELEGRAM_TOKEN

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hello", hello_command))

    updater.start_polling()
    updater.idle()

"""
Main function, entry point of the program
"""
def main():
    read_credentials()
    telegram_func()

if __name__ == "__main__":
    main()
