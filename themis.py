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
import csv
# pip install python-telegram-bot --upgrade
# !!! Verify that you've installed the latest version of the Python Telegram Bot library 20+
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = ""
ST = 'storage.dbm'
RL = 'roles.dbm'
AR = 'airports.csv'

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
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /retrieve')
    try:
        key = str(update.effective_user.id)
        with dbm.open(ST, 'r') as db:
            answer_retrieve = bytes.decode(db[key], 'utf-8')
            await update.message.reply_text(answer_retrieve)
            logging.info(f'Bot answered: {answer_retrieve}')
    except KeyError:
        answer_wrong_retrieve = "Nothing there :("
        await update.message.reply_text(answer_wrong_retrieve)
        logging.info(f'Bot answered: {answer_wrong_retrieve}')
        
"""
Command /store
"""
async def store_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    str_text = update.effective_message.text
    str_text = str_text.replace("/store ","",1)
    key = str(update.effective_user.id) 
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /store: {str_text}')
    with dbm.open(ST, 'c') as db:
        db[key] = str_text

"""
Command /who
"""
async def who_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /who')
    roleid = str(update.effective_user.id)
    with dbm.open(RL, "c") as db:
        if roleid in db:
            role = bytes.decode(db[roleid], 'utf-8')
            answer_exist = f"You are a/an {role}"
            await update.message.reply_text(answer_exist)
            logging.info(f'Bot answered: {answer_exist}')
        else: 
            db[roleid] = 'user'
            answer_notexist = "You were not in our database. Now you've become a user"
            await update.message.reply_text(answer_notexist)
            logging.info(f'Bot answered: {answer_notexist}')

"""
Command /airport
"""
async def airport_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    countrycode = update.effective_message.text
    countrycode = countrycode.replace("/airport ","", 1)
    logging.info(f'User {update.effective_user.id} ({update.effective_user.username}) called /airport with country code: {countrycode}')
    with open(AR, "r", encoding = 'utf-8') as file:
        reader = csv.reader(file, delimiter =',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        airpsline = []
        counter = 0
        answer_airport = ''

        for row in reader:
            if row[8] == countrycode:
                airpsline.append(row)
                counter = counter + 1
            if counter == 5:
                break
        for counter_1 in range(0,counter):
            the_link = 'http://www.google.com/maps/place/' + airpsline[counter_1][4] + ','+ airpsline[counter_1][5]
            answer_airport = f'{answer_airport} \nThe name of the airport: {airpsline[counter_1][3]}. (There is the link to google maps: {the_link}). \n '

        if len(airpsline) > 0:
            await update.message.reply_text(answer_airport)
            logging.info(f'Bot answered: {answer_airport}')
        else:
            answer_nocode = "Sorry, I don't know this country code. Please, check it and try again."
            await update.message.reply_text(answer_nocode)
            logging.info(f'Bot answered: {answer_nocode}')
                
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
    app.add_handler(CommandHandler("who", who_command))
    app.add_handler(CommandHandler("airport", airport_command))
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
