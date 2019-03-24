import configparser


def main():
   configParser = configparser.RawConfigParser()
   configFilePath = r'TelegramBot.config'
   configParser.read(configFilePath)
   backupConfig == configparser.RawConfigParser()
   backupConfigPath = r'TelegramBotBACKUP.config'
   backupConfig.read(backupConfigPath)
   if not configParser['BOTCONFIG']['botId']:
      configParser['BOTCONFIG']['botId'] = backupConfig['BOTCONFIG']['botId']
   if not configParser['BOTCONFIG']['urls']:
      configParser['BOTCONFIG']['urls'] = backupConfig['BOTCONFIG']['urls']
   if not configParser['BOTCONFIG']['urlsHighway']:
      configParser['BOTCONFIG']['urlsHighway'] = backupConfig['BOTCONFIG']['urlsHighway']
   if not configParser['BOTCONFIG']['insults']:
      configParser['BOTCONFIG']['insults'] = backupConfig['BOTCONFIG']['insults']
   if not configParser['BOTCONFIG']['noToInsult']:
      configParser['BOTCONFIG']['noToInsult'] = backupConfig['BOTCONFIG']['noToInsult']
   if not configParser['BOTCONFIG']['speedtestUrl']:
      configParser['BOTCONFIG']['speedtestUrl'] = backupConfig['BOTCONFIG']['speedtestUrl']


if __name__ == '__main__':
    main()
