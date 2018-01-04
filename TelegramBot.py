#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bot to send timed Telegram messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import pyspeedtest
import random
import configparser
import subprocess
import urllib.request
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(bot, update, job_queue, chat_data):
    update.message.reply_text('Hi! Started!')
    chat_id = update.message.chat_id
    if 'job' in chat_data:
        update.message.reply_text('you already have an active timer')
        return
    try:
        chat_data['job']
        return
    except Exception:
        job_queue.run_once(alarm, 86400, context=chat_id)
    sendStatus(bot, chat_id)


def alarm(bot, job):
    """Send the alarm message."""
    sendStatus(bot, job.context)


def getimage(bot, update):
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    if __debug__:
        print("trafficimage")
    chat_id = update.message.chat_id
    if __debug__:
        print(chat_id)
    addresses = configParser.get('BOTCONFIG', 'urls').split(',')
    if __debug__:
        print(addresses)
    imagename = 'getImg.jpg'
    for address in addresses:
        if __debug__:
            print(address)
        urllib.request.urlretrieve(address, imagename)
        if __debug__:
            print("requestDone")
        bot.send_photo(chat_id=chat_id, photo=open(imagename, 'rb'))
        if __debug__:
            print("photo sended")
        os.remove(imagename)


def gethighwayvid(bot, update):
    if __debug__:
        print("autostrada")
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    addresses = configParser.get('BOTCONFIG', 'urlsHighway').split(',')
    if __debug__:
        print(addresses)
    name = "666Devil.mp4"
    if __debug__:
        print("prima di ciclo adress")
    for address in addresses:
        if __debug__:
            print(address)
        r = requests.get(address)
        f = open(name, 'wb')
        for chunk in r.iter_content(chunk_size=255):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
        f.close()
        bot.send_video(chat_id=update.message.chat_id,
                       video=open(name, 'rb'), supports_streaming=True)
        os.remove(name)


def getstatus(bot, update):
    chat_id = update.message.chat_id
    sendStatus(bot, chat_id)


def makecoffe(bot, update):
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    if __debug__:
        print("config parser readed")
    chat_id = update.message.chat_id
    insults = configParser.get('BOTCONFIG', 'insults').split(',')
    rand = random.randint(0, len(insults) - 1)
    user = update.message.from_user
    name = user.first_name
    surname = user.last_name
    completiinsult = "scolta {} {}, {}".format(name, surname, insults[rand])
    bot.send_message(chat_id, completiinsult)


def sendStatus(bot, chat_id):
    if __debug__:
        print("sendstatus")
    if __debug__:
        print('before sending')
    ip = subprocess.check_output(["hostname", "-I"]).decode('utf-8')
    if __debug__:
        print(ip)
    temp = os.popen("vcgencmd measure_temp").readline()
    if __debug__:
        print(temp)
    uptime = subprocess.check_output(['uptime']).decode('utf-8')
    if __debug__:
        print(uptime)
    bot.send_message(chat_id, 'Ip={}{}Uptime={}'.format(ip, temp, uptime))


def networkstats(bot, update):
    chat_id = update.message.chat_id
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    st = pyspeedtest.SpeedTest(configParser.get('BOTCONFIG', 'speedtestUrl'))
    if __debug__:
        print('speedtest initialized')
    try:
        ping = "{0:.2f}".format(st.ping())
        if __debug__:
            print(ping)
    except Exception:
        ping = "error on ping"
        if __debug__:
            print("error ping")
    try:
        download = "{0:.2f}".format(st.download())
        if __debug__:
            print(download)
    except Exception:
        download = "error on download"
        if __debug__:
            print("error download")
    try:
        upload = "{0:.2f}".format(st.upload())
        if __debug__:
            print(upload)
    except Exception:
        upload = "error on upload"
        if __debug__:
            print("error upload")
    bot.send_message(chat_id, "Ping={}DW={}UP={}".format(
        ping, download, upload))


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    update.message.reply_text('Timer successfully unset!')


def main():
    """Run bot."""
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    if __debug__:
        print("config parser readed")
    updater = Updater(configParser.get('BOTCONFIG', 'botId'))
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler(
        "start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("getstatus", getstatus))
    dp.add_handler(CommandHandler("networkstats", networkstats))
    dp.add_handler(CommandHandler("makecoffe", makecoffe))
    dp.add_handler(CommandHandler("getimage", getimage))
    dp.add_handler(CommandHandler("gethighwayvid", gethighwayvid))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    # Start the Bot
    updater.start_polling(5)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT.  This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
