import socket
import json
import ssl
import SSLMessage as sslCommand
from SSLMessageEncoder import  SSLMessageEncoder as MyEncoder

class Client(object):

    ip=''

    def __init__(self,ipadress):
        self.ip = ipadress        
    
    def sendMessage(self,line1,line2):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(s,
                                       ca_certs="server.crt",
                                       cert_reqs=ssl.CERT_REQUIRED)
            
            ssl_sock.connect((self.ip, 10023))
            params = dict()
            params['line1'] = line1
            params['line2'] = line2
            cmd = sslCommand.SSLMessage('displayMessage',params)
            converted = self.serialize(cmd)
            ssl_sock.write(converted.encode('utf-8'))
            ssl_sock.close()
    
    def readTemp(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(s,
                                       ca_certs="server.crt",
                                       cert_reqs=ssl.CERT_REQUIRED)
            
            ssl_sock.connect((self.ip, 10023))
            params = dict()
            cmd = sslCommand.SSLMessage('readTemperature',params)
            converted = self.serialize(cmd)
            ssl_sock.write(converted.encode('utf-8'))
            data = ssl_sock.read()
            ssl_sock.close()
    
    def serialize(self,toSerialize):    
        serialized = json.dumps(MyEncoder().encode(toSerialize),cls=MyEncoder)
        return serialized 
    