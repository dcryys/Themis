#!/usr/bin/env python3
"""
Goddess Themis Telegram bot
Serving justice to the world
(c) ????
"""

import os
import sys
from datetime import datetime
import ephem
import ai1
import logging
import dbm
# pip install python-telegram-bot --upgrade
# !!! Verify that you've installed the latest version of the Python Telegram Bot library 20+
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = ""
ST = 'storage.dbm'
"""
Logging
"""
logging.basicConfig(level = logging.INFO, filename = 'journal.log')

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
async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /hello')
    answer_hello = f'Hello, {update.effective_user.first_name}!'
    await update.message.reply_text(answer_hello)
    logging.info(f'Bot answered: {answer_hello}')
    
"""
Command /time =)
"""
async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /time')
    the_datetime = datetime.now()
    currnet_time = the_datetime.time()
    answer_time = f'Current time is {currnet_time.strftime("%H:%M:%S")}'
    await update.message.reply_text(answer_time)
    logging.info(f'Bot answered: {answer_time}')

"""
Command /datetime
"""
async def datetime_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /datetime')
    today = datetime.now()
    current_time = today.time()
    observer = ephem.Observer()
    observer.lon = '0'
    observer.lat = '0'
    observer.date = ephem.now()
    moon = ephem.Moon()
    moon.compute(observer)
    phase = moon.phase / 100
    m_percent = round(moon.phase)
    new_m = ephem.next_new_moon(today)
    date_new_m = new_m.datetime()
    d_ans = date_new_m - today
    days_dif = d_ans.days
    if days_dif <= 15:
        if phase >= 0.97:
            ph_name = 'Full Moon'
        elif phase <= 0.03:
            ph_name = 'New Moon'
        elif phase > 0.03 and phase < 0.47:
            ph_name = "Waning Crescent"
        elif phase >= 0.47 and phase <= 0.53:
            ph_name = "Third Quater"
        elif phase > 0.53 and phase < 0.97:
            ph_name = "Waning Gibbous"
    else:
        if phase >= 0.97:
            ph_name = 'Full Moon'
        elif phase <= 0.03:
            ph_name = 'New Moon'
        elif phase > 0.03 and phase < 0.47:
            ph_name = "Waxing Crescent"
        elif phase >= 0.47 and phase <= 0.53:
            ph_name = "First Quater"
        elif phase > 0.53 and phase < 0.97:
            ph_name = "Waxing Gibbous"
    answer_datetime = f'Today is {today.strftime("%A")}, the {today.strftime("%d")} of {today.strftime("%B")}, {today.strftime("%Y")}, {current_time.strftime("%H:%M:%S")}. Current moon phase: {ph_name} ({m_percent}%)'
    await update.message.reply_text(answer_datetime)
    logging.info(f'Bot answered: {answer_datetime}')
    
"""
Make it speak!
"""
async def tellme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.effective_message.text
    text = text.replace("/tellme ","",1)
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /tellme: "{text}"')
    answer_tellme = ai1.ask_gpt3(text)
    await update.message.reply_text(answer_tellme)
    logging.info(f'Bot answered: {answer_tellme}')
    
"""
Command /retrieve
"""
async def retrieve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with dbm.open(ST, 'r') as db:
            await update.message.reply_text(db[update.effective_user.username])
    except KeyError:
        await update.message.reply_text("Nothing there :(")
        
"""
Command /store
"""
async def store_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    string = update.effective_message.text
    string = string.replace("/store ","",1)
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /store: {string}')
    with dbm.open(ST, 'c') as db:
        db[update.effective_user.id] = string

"""
Main body of Telegram bot handling loop
"""
def telegram_func():
    global TELEGRAM_TOKEN

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("hello", hello_command))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(CommandHandler("datetime", datetime_command))
    app.add_handler(CommandHandler("tellme", tellme_command))
    app.add_handler(CommandHandler("store", store_command))
    app.add_handler(CommandHandler("retrieve", retrieve_command))
    app.run_polling()

"""
Main function, entry point of the program
"""
def main():
    logging.info('Bot is starting.')   
    read_credentials()
    telegram_func()

if __name__ == "__main__":
    main()
