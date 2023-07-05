#!/usr/bin/env python3
"""
Goddess Themis Telegram bot
Serving justice to the world
(c) ????
"""

import os
import sys
from datetime import datetime
import ai1
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
    print("Reading credentials...")
    with open(".credentials.txt", "r") as f:
        print("File opened")
        TELEGRAM_TOKEN = f.readline().strip()
        print("Token read")


"""
Telegram bot answer to /hello command
"""
def hello_command(update: Update, context: CallbackContext) -> None:
    print(f'User {update.effective_user.first_name} called /hello')
    update.message.reply_text(f'Hello {update.effective_user.first_name}!')

"""
Command /time =)
"""
def time_command(update: Update, context: CallbackContext) -> None:
    print(f'User {update.effective_user.first_name} called /time')
    the_datetime = datetime.now()
    currnet_time = the_datetime.time()
    update.message.reply_text(f'Current time is {currnet_time.strftime("%H:%M:%S")}')

"""
Command /datetime
"""
def datetime_command(update: Update, context: CallbackContext) -> None:
    print(f'User {update.effective_user.first_name} called /datetime')
    today = datetime.now()
    current_time = today.time()
    update.message.reply_text(f'Today is {today.strftime("%A")}, the {today.strftime("%d")} of {today.strftime("%B")}, {today.strftime("%Y")}, {current_time.strftime("%H:%M:%S")}')


"""
Make it speak
"""
def tellme_command(update: Update, context: CallbackContext) -> None:
    print(f'User {update.effective_user.first_name} called /tellme')
    text = update.effective_message.text
    answer = ai1.ask_gpt3(text)
    print(f'User sent us: {update.effective_message.text}')
    update.message.reply_text(answer)
    
"""
Main body of Telegram bot handling loop
"""
def telegram_func():
    global TELEGRAM_TOKEN

    print("Entered function telegram_func()")
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    print("Updater created")
    dispatcher = updater.dispatcher
    print("Dispatcher created")

    dispatcher.add_handler(CommandHandler("hello", hello_command))
    print("Command /hello handler added")
    dispatcher.add_handler(CommandHandler("time", time_command))
    print("Command /time handler added")
    print("Command /time handler added")
    dispatcher.add_handler(CommandHandler("datetime", datetime_command))
    print("Command /datetime handler added")
    dispatcher.add_handler(CommandHandler("tellme", tellme_command))
    print("Command /tellme handler added")

    updater.start_polling()
    print("Polling started, going into loop")
    updater.idle()

"""
Main function, entry point of the program
"""
def main():
    print("Bot is starting..")    
    read_credentials()
    telegram_func()

if __name__ == "__main__":
    main()
