"""
This is an experimental bot for our project Themis.

"""
import os
import sys
from datetime import datetime

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

TELEGRAM_TOKEN = ""

"""
Reading the file with token. It is needed for safety. 
Safety is the number-one priority!
"""
def read_token():
    global TELEGRAM_TOKEN
    print("Reading token...")
    with open(".code.txt", "r") as f:
        print("File opened")
        TELEGRAM_TOKEN = f.readline().strip()
        print("Token read")

"""
Command /hello
"""
def hello_command(update: Update, context: CallbackContext) -> None:
    print(f'User {update.effective_user.first_name} called /hello')
    update.message.reply_text(f'Hello, {update.effective_user.first_name}!')

"""
Command /time
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
Function that is the main body of July
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
    dispatcher.add_handler(CommandHandler("datetime", datetime_command))
    print("Command /datetime handler added")

    updater.start_polling()
    print("Polling started, going into loop")
    updater.idle()

"""
The main function
"""
def main():
    print("Bot is starting...")
    read_token()
    telegram_func()

if __name__ == "__main__":
    main()
