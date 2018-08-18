#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to send timed Telegram messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import pyspeedtest
import random
import configparser
import subprocess
from subprocess import call
from telegram.ext import Updater, CommandHandler
""""from paramiko import client"""""


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

def getTrafficImage(bot,update):
    addresses = configParser.get('BOTCONFIG', 'urls').split('\n')
    #for address in addresses



def getstatus(bot, update):
    chat_id = update.message.chat_id
    call(["fswebcam", "-d", "/dev/video0", "-F 200", "-r", "1280x720", "666.jpg"])
    bot.send_photo(chat_id=chat_id, photo=open('666.jpg', 'rb'))
    os.remove('666.jpg')
    sendStatus(bot, chat_id)


def makecoffe(bot,update):
    chat_id = update.message.chat_id
    insults =configParser.get('BOTCONFIG', 'insults').split(',') 
    rand = random.randint(0,len(insults) - 1)
    user = update.message.from_user
    name = user.first_name
    surname = user.last_name
    completiinsult = "scolta {} {}, {}".format(name,surname,insults[rand])
    notToInsult=configParser.get('BOTCONFIG', 'noToInsult').split(',')
    if any(notToInsult in name for notToInsult in a):
        completiinsult="certo capo! lo faccio subito!"
    bot.send_message(chat_id,completiinsult)


def sendStatus(bot, chat_id):
    print("sendstatus")
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
    print('before sending')
    ip=subprocess.check_output(["hostname", "-I"]).decode('utf-8')
    print(ip)
    temp="error"
    print(temp)
    uptime=subprocess.check_output(['uptime']).decode('utf-8')
    print(uptime)
    bot.send_message(chat_id, 'Ip={}{}Uptime={}Ping={}DW={}UP={}'.format(ip,temp,uptime,ping,download,upload))



def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    update.message.reply_text('Timer successfully unset!')


#def revive(bot, update, chat_data):
#    ssh = paramiko.SSHClient()
#    ssh.connect(server, username=username, password=password)
#    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("psql -U factory -d
#    factory -f /tmp/data.sql")
def main():
    """Run bot."""
    configParser = configparser.RawConfigParser()
    configFilePath = r'TelegramBot.config'
    configParser.read(configFilePath)
    updater = Updater(configParser.get('TELEGRAM', 'botId')) 
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("getstatus", getstatus))
    dp.add_handler(CommandHandler("makecoffe", makecoffe))
    dp.add_handler(CommandHandler("getTrafficImage", getTrafficImage))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    # Start the Bot
    updater.start_polling()
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT.  This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
