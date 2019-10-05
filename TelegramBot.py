#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bot to send timed Telegram messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import time
import pyspeedtest
import random
import configparser
import subprocess
import urllib.request
import requests
import Client 
from subprocess import call
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

clientInstance = Client.Client('127.0.0.1')
# Define a few command handlers.  These usually take the two arguments bot and
# update.  Error handlers also receive the raised TelegramError object in
# error.
def start(bot, update, job_queue, chat_data):
    update.message.reply_text('Hi! Started!')
    chat_id = update.message.chat_id
    if 'job' in chat_data:
        update.message.reply_text('you already have an active timer')
        return
    try:
        job = chat_data['job']
        return
    except:
        job = job_queue.run_once(alarm, 86400, context=chat_id)
    sendStatus(bot, chat_id)


def alarm(bot, job):
    """Send the alarm message."""
    sendStatus(bot, job.context)

def getimage(bot,update):
    printsenderonlcd(update)
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    print("trafficimage")
    chat_id = update.message.chat_id
    print(chat_id)
    addresses = configParser.get('BOTCONFIG', 'urls').split(',')
    print(addresses)
    imagename = 'getImg.jpg'
    for address in addresses:
        print(address)
        urllib.request.urlretrieve(address, imagename)
        print("requestDone")
        bot.send_photo(chat_id=chat_id, photo=open(imagename, 'rb'))
        print("photo sended")
        os.remove(imagename)


def gethighwayvid(bot,update):
    print("autostrada")
    printsenderonlcd(update)
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    addresses = configParser.get('BOTCONFIG', 'urlsHighway').split(',')
    print(addresses)
    name = "666Devil.mp4"
    print("prima di ciclo adress")
    for address in addresses:
        print(address)
        r = requests.get(address)
        f = open(name,'wb')
        for chunk in r.iter_content(chunk_size=255):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        f.close()
        bot.send_video(chat_id=update.message.chat_id, video=open(name, 'rb'), supports_streaming=True)
        os.remove(name)


def getstatus(bot, update):
    printsenderonlcd(update)
    chat_id = update.message.chat_id
    #call(["fswebcam", "-d", "/dev/video0", "-F 200", "-r", "1280x720",
    #"666.jpg"])
    #bot.send_photo(chat_id=chat_id, photo=open('666.jpg', 'rb'))
    #os.remove('666.jpg') 
    sendStatus(bot, chat_id)

def makecoffe(bot,update):
    printsenderonlcd(update)
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    print("config parser readed")
    chat_id = update.message.chat_id
    insults = configParser.get('BOTCONFIG', 'insults').split(',')
    rand = random.randint(0,len(insults) - 1)
    user = update.message.from_user
    name = user.first_name
    surname = user.last_name
    completiinsult = "scolta {} {}, {}".format(name,surname,insults[rand])
    notToInsult = configParser.get('BOTCONFIG', 'noToInsult').split(',')
    if any(notToInsult in name for notToInsult in a):
        completiinsult = "certo capo! lo faccio subito!"
    bot.send_message(chat_id,completiinsult)

def sendStatus(bot, chat_id):
    print("sendstatus")
    print('before sending')
    ip = subprocess.check_output(["hostname", "-I"]).decode('utf-8')
    print(ip)
    temp = os.popen("vcgencmd measure_temp").readline()
    print(temp)
    uptime = subprocess.check_output(['uptime']).decode('utf-8')
    print(uptime)
    bot.send_message(chat_id, 'Ip={}{}Uptime={}'.format(ip,temp,uptime))


def networkstats(bot, update):
     printsenderonlcd(update)
     configParser = configparser.RawConfigParser()
     configFilePath = r'TelegramBot.config'
     configParser.read(configFilePath)
     st = pyspeedtest.SpeedTest(configParser.get('BOTCONFIG', 'speedtestUrl'))
     print('speedtest initialized')
     try:
        ping = "{0:.2f}".format(st.ping())
        print(ping)
     except:
        ping = "error on ping"
        print("error ping")
     try:
        download = "{0:.2f}".format(st.download())
        print(download)
     except:
        download = "error on download"
        print("error download")
     try:
        upload = "{0:.2f}".format(st.upload())
        print(upload)
     except:
        upload = "error on upload"
        print("error upload")
     bot.send_message(chat_id, 'Ping={}DW={}UP={}'.format(uptime,ping,download,upload))

def printsenderonlcd(update):
    user = update.message.from_user
    messagefrom = "messaggio da".center(16)
    sender = "{}".format(user.username).center(16)
    clientInstance.sendMessage(messagefrom,sender)


def textmessagerecieved(bot,update):
    user = update.message.from_user
    print("ricevuto:{}".format(update.message.text))
    outputMessage = "{}:\n".format(user.username).center(16)
    recivedText = update.message.text
    clientInstance.sendMessage(outputMessage,recivedText)


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
    print("config parser readed")
    updater = Updater(configParser.get('BOTCONFIG', 'botId'))
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("getstatus", getstatus))
    dp.add_handler(CommandHandler("networkstats", networkstats))
    dp.add_handler(CommandHandler("makecoffe", makecoffe))
    dp.add_handler(CommandHandler("getimage", getimage))
    dp.add_handler(CommandHandler("gethighwayvid", gethighwayvid))
    echo_handler = MessageHandler(Filters.text, textmessagerecieved)
    dp.add_handler(echo_handler)
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    # Start the Bot
    updater.start_polling(5)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT.  This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()