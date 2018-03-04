import smtplib
import configparser
import logging


def main():
    try:
        configParser = configparser.RawConfigParser()
        configFilePath = r'bulkMailSender.config'
        configParser.read(configFilePath)
        server = smtplib.SMTP(configParser.get('SMTP', 'smtpAddress'), configParser.getint('SMTP', 'smtpPort'))
        senderaddress = configParser.get('SMTP', 'senderAddress')
        server.login(senderaddress, "password")
        msg = configParser.get('MAIL', 'body')
        addresses = configParser.get('MAIL', 'addresses').split('\n')
        for address in addresses:
            server.sendmail(senderaddress, address, msg.format(address))
    except Exception as e:
        logging.exception('ERROR: ' + str(e))


if __name__ == "__main__":
    main()
