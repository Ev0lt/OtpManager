import struct
import time
import base64
import hmac
import hashlib

class otp:
  def __init__(self,key=None):
    self.key = key
    self.oneCode = None

  def uk(self,key):
    self.key = key
    return self
  def readConfig(self,cnf):
    if cnf.algorithm == "sha1":
      cnf.algorithm = hashlib.sha1
    elif cnf.algorithm == "md5":
      cnf.algorithm = hashlib.md5
    elif cnf.algorithm == "sha512":
      cnf.algorithm = hashlib.sha512
    elif cnf.algorithm == "sha224":
      cnf.algorithm = hashlib.sha224
    elif cnf.algorithm == "sha256":
      cnf.algorithm = hashlib.sha256
    elif cnf.algorithm == "sha384":
      cnf.algorithm = hashlib.sha384
    elif cnf.algorithm == "sha3_224":
      cnf.algorithm = hashlib.sha3_224
    elif cnf.algorithm == "sha3_384":
      cnf.algorithm = hashlib.sha3_384
    elif cnf.algorithm == "sha3_512":
      cnf.algorithm = hashlib.sha3_512
    elif cnf.algorithm == "blake2b":
      cnf.algorithm = hashlib.blake2b
    elif cnf.algorithm == "blake2s": 
      cnf.algorithm = hashlib.blake2s

    self.key = cnf.secret
    if cnf.type == "totp" and (cnf.acName.lower() == "steam" or cnf.issuer.lower() == "steam"):
        return self.steam()
    
    elif cnf.type == "totp":
      return self.totp(cnf.digits,cnf.period,cnf.algorithm)
    
    elif cnf.type == "hotp":
      return None
    
    else:
      return None
  def otp(self,size=6,interval=30,h=hashlib.sha1):
    ts = struct.pack(">Q",int(time.time())//interval)
    mac = hmac.new(base64.b32decode(self.key.encode()),ts,h).digest()
    length = len(mac)
    length = mac[length-1]&0xf
    b2 = mac[length]
    b1 = mac[length+1]
    b3 = mac[length+2]
    b4 = mac[length+3]
    self.oneCode = (b4&0xff|(b3&0xff)<<8|(b2&0x7f)<<24|(b1&0xff)<<16)
  def totp(self,size=6,interval=30,h=hashlib.sha1):
    self.otp(size,interval,h)
    j = 1
    for i in range(size):
      j*=10
    return str(self.oneCode%j).zfill(size)

  def hotp(self,size=6,count=0,h=hashlib.sha1):
    ts = struct.pack(">Q",count)
    mac = hmac.new(base64.b32decode(self.key.encode()),ts,h).digest()
    length = len(mac)
    length = mac[length-1]&0xf
    b2 = mac[length]
    b1 = mac[length+1]
    b3 = mac[length+2]
    b4 = mac[length+3]
    self.oneCode = (b4&0xff|(b3&0xff)<<8|(b2&0x7f)<<24|(b1&0xff)<<16)
    return str(self.oneCode%j).zfill(size)
  def steam(self):
    ct = "23456789BCDFGHJKMNPQRTVWXY"
    self.otp()
    
    cl = [0]*5
    for i in range(5):
      cl[i] = ct[self.oneCode%len(ct)]
      self.oneCode //=len(ct)
    return ''.join(cl)