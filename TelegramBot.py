#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to send timed Telegram messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram.ext import Updater, CommandHandler
from subprocess import call
import commands
import os
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update,job_queue,chat_data):
    update.message.reply_text('Hi! Started!')
    chat_id = update.message.chat_id
    if 'job' in chat_data:
         update.message.reply_text('you already have an active timer')
         return
    try:
         job = chat_data['job']
         return
    except:
         job = job_queue.run_once(alarm,86400, context=chat_id)
	 sendStatus(bot,chat_id)

def alarm(bot, job):
    """Send the alarm message."""
    sendStatus(bot,job.context)

def getstatus(bot, update):
     chat_id = update.message.chat_id
     call(["fswebcam", "-d","/dev/video0","-F 150", "-r", "1280x720", "666.jpg"])
     bot.send_photo(chat_id=chat_id, photo=open('666.jpg', 'rb'))
     os.remove('666.jpg')
     sendStatus(bot,chat_id)

def sendStatus(bot,chat_id):
    bot.send_message(chat_id,'Ip={}\n{}\nuptime={}\n'.format(commands.getoutput('hostname -I'),commands.getoutput('/opt/vc/bin/vcgencmd measure_temp'),commands.getoutput('uptime') ))

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
    updater = Updater("EHEIDONTPOSTTHEBOTID")#sooooooo smart!!
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start,pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("getstatus",getstatus))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    # Start the Bot
    updater.start_polling()
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main()
