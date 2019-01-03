#!/bin/sh
PIDFile="run.pid"
sudo kill -9 $(<"$PIDFile")
sudo git pull
suodo rm "run.pid"
nohup python3.5 TelegramBot.py > /dev/null 2>&1 & echo $! > run.pid