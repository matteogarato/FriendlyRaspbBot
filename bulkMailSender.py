import smtplib

senderAdress="email@gmail.com"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.login(senderAdress, "password")
bodyFile = open("BodyMail.text", "r") 
sendAdresses=open("Adresses.text", "r")
msg = bodyFile.read() 
adresses=sendAdresses.read()
adresses=adresses.splitlines()
for adress in adresses :
    server.sendmail(senderAdress, adress, msg.format(adress))
