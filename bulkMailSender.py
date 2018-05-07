import smtplib
import configparser
import logging
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
    try:
        configParser = configparser.RawConfigParser()
        configFilePath = r'bulkMailSender.config'
        configParser.read(configFilePath)
        smtpAddress = '{}:{}'.format(configParser.get('SMTP', 'smtpAddress'),configParser.getint('SMTP', 'smtpPort'))
        server = smtplib.SMTP(smtpAddress)
        server.starttls()
        senderaddress = configParser.get('SMTP', 'senderAddress')
        password = input("inserire la password per l'indirizzo {senderAddres}: ".format(senderAddres=senderaddress))
        server.login(senderaddress, password)
        msgText = configParser.get('MAIL', 'body')
        addresses = configParser.get('MAIL', 'addresses').split('\n')
        for address in addresses:
            companyName = address.split('@')[1].split('.')[0]
            msgText = msgText.format(company=companyName)
            msg = MIMEMultipart()
            msg['From'] = senderaddress
            msg['To'] = address
            msg.attach(MIMEText(msgText, 'html'))
            msg['Subject'] = configParser.get('MAIL', 'object')
            server.sendmail(senderaddress, address, msg.as_string())
            time.sleep(configParser.getint('SMTP', 'mailBreak'))
    except Exception as e:
        logging.exception('ERROR: ' + str(e))


if __name__ == "__main__":
    main()
