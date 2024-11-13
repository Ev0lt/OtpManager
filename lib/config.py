from typing import Union
from PIL import Image
from pyzbar.pyzbar import decode
from urllib.parse import urlparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import re
import numpy
import os
import platform
import pickle
import base64

class config:
    def __init__(self,userName=None,acName=None,algorithm="sha1",digits=6,issuer=None,period=30,secret=None,Type="totp"):
        self.userName = userName   #用户名
        self.acName = acName       #来自哪里和issuer一致
        self.algorithm = algorithm #加密方式sha1等等
        self.digits = digits       #otp密钥长度
        self.issuer = issuer       #和acName一致
        self.period = period       #间隔多少秒刷新
        self.secret = secret       #密钥
        self.type = Type           #otp的类型
        self.otpstring=""
        self.text=""
    def __str__(self):
        return self.text
    #解构otp字符串
    def queryPase(self):
        find = re.findall("([a-zA-z]+)\s*\=\s*([a-zA-Z0-9]+)",self.otpstring)
        query = {}
        for i in find:
            query[i[0]]=i[1]
        return query

    #读取otp字符串
    def parseOtp(self,otpStr):
        try:
            pu = urlparse(otpStr)
            if pu.query == "" or pu.scheme == "" or pu.netloc == "" or pu.path == "":
                raise Exception("Error")
            self.text = otpStr
            self.otpstring = pu.query
            query = self.queryPase()
            self.userName = pu.path.split(":")[1]
            self.acName = pu.path[1:].split(":")[0]
            self.secret = query['secret'] if "secret" in query.keys() else ""
            self.secret = self.secret + "="*((8-len(self.secret)%8)%8)
            self.issuer = query['issuer'] if "issuer" in query.keys() else ""
            self.type = pu.netloc
            self.algorithm = query['algorithm'] if "algorithm" in query.keys() else self.algorithm
            self.period = int(query['period'] if "period" in query.keys() else self.period)
            self.digits = int(query['digits'] if 'digits' in query.keys() else self.digits)
        except:
            return "ParseError"
        return self
    #通过扫码等到otp字符串
    def readFromQR(self,img:Union[str,Image.Image,numpy.ndarray]):
        if type(img) == type(""):
            img = Image.open(img)
        try:
            deContent = decode(img)
        except Exception as e:
            raise Exception("DecodeQRError")
        if deContent:
            self.parseOtp(deContent[0].data.decode())
            return self
        raise Exception("ReadQRDecodeContentError")
    def save(self):
        if platform.system() == "Windows":
            basePath = os.environ['USERPROFILE']+"\\otpSave"
            if not os.path.exists(basePath):
                os.makedirs(basePath)
            
            savePath = f"{basePath}\\{str(self.acName)}_{str(self.userName)}.pickle"
        elif platform.system() == "Linux":
            user=os.environ['USER']
            basePath=f"/{'root' if user == 'root' else 'home/'+user}"+"/otpSave"
            if not os.path.exists(basePath):
                os.makedirs(basePath)
            savePath = f"{basePath}/{str(self.acName)}_{str(self.userName)}.pickle"
        else:
            raise Exception("Unknown Operating System")

        dumpData = pickle.dumps(self)
        dumpData = base64.b64encode(dumpData)
        aes = AES.new(b"1234567812345678",AES.MODE_ECB)
        enc = aes.encrypt(pad(dumpData,32))
        
        open(savePath,'wb').write(enc)
        return self
    
    def load(self,basePath):
        enc = open(basePath,'rb').read()
        aes = AES.new(b"1234567812345678",AES.MODE_ECB)
        dec = aes.decrypt(enc)
        text = base64.b64decode(dec)
        Load = pickle.loads(text)
        self.userName = Load.userName
        self.acName = Load.acName
        self.algorithm = Load.algorithm
        self.digits = Load.digits
        self.issuer = Load.issuer
        self.period = Load.period
        self.secret = Load.secret
        self.type = Load.type
        return self


if __name__=='__main__':
    cnf = config().readFromQR(r"D:\program_project\python\authotp\test\github.png")
    cnf.save()
    cnf = config()
    cnf = cnf.load(r"C:\Users\Evolt\otpSave\GitHub_Ev0lt.pickle")
    
    print(cnf.secret)