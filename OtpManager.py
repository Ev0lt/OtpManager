from lib.config import config
from PyQt6.QtWidgets import QMainWindow,QApplication,QMessageBox,QDialog,QLineEdit
from PyQt6.QtCore import QTimer
from PIL import ImageGrab
from lib.configure import Ui_Dialog as configUi
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from PyQt6 import QtCore
from threading import Thread
import lib.DrawUi as ui
import lib.config as conf
import lib.otp as otp
import lib.filelist as fl
import optparse
import sys
import os
import hashlib
import time
win = None
#get real resolution
def grr():
    hDC = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h

class drawSubWindowConfigure(QDialog):
    def __init__(self,win=ui.SubConfigWin()):
        super().__init__()
        self.ui = win
        self.bool=False
        self.ui.setupUi(self)
        self.ui.comboBox.setEnabled(True)
        self.ui.comboBox.addItem("totp")
        self.ui.comboBox.addItem("hotp")
        self.ui.comboBox.addItem("steam")
        self.ui.comboBox_2.addItem("sha1")
        self.ui.comboBox_2.addItem("md5")
        self.ui.comboBox_2.addItem("sha224")
        self.ui.comboBox_2.addItem("sha256")
        self.ui.comboBox_2.addItem("sha384")
        self.ui.comboBox_2.addItem("sha512")
        self.ui.comboBox_2.addItem("sha3_224")
        self.ui.comboBox_2.addItem("sha3_384")
        self.ui.comboBox_2.addItem("sha3_512")
        self.ui.comboBox_2.addItem("blake2b")
        self.ui.comboBox_2.addItem("blake2s")
        self.ui.pushButton.clicked.connect(self.save)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.comboBox.currentIndexChanged.connect(self.unlock)

    def save(self):
        otpType = self.ui.comboBox.currentText()
        username = self.ui.lineEdit.text()
        site = self.ui.lineEdit_2.text()
        issuer = self.ui.lineEdit_3.text()
        encType = self.ui.comboBox_2.currentText()
        length = self.ui.spinBox.value()
        flushTime = self.ui.spinBox_2.value()
        key = self.ui.lineEdit_4.text()
        if site == "" and issuer != "":
            site = issuer
        elif site == "" and issuer == "":
            QMessageBox.information(self,"Error","用户名和站点不能同时为空")
        else:
            issuer == site
        
        if encType == "":
            encType = "sha1"
        
        if length == 0 or not length:
            length = 6
        
        if flushTime == 0 or not flushTime:
            flushTime = 30

        if key == "":
            pass
        cnf = config(username,site,encType,length,issuer,flushTime,key,otpType)
        cnf.save()
        win.flushPage()
    def unlock(self):
        
        if self.ui.comboBox.currentText() == "steam":
            self.ui.comboBox_2.setCurrentIndex(0)
            self.ui.spinBox.clear()
            self.ui.spinBox_2.clear()
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.spinBox.setEnabled(False)
            self.ui.spinBox_2.setEnabled(False)

        elif self.ui.comboBox.currentText() == "totp":
            self.ui.comboBox_2.setCurrentIndex(0)
            self.ui.spinBox.clear()
            self.ui.spinBox_2.clear()
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.spinBox.setEnabled(True)
            self.ui.spinBox_2.setEnabled(True)

        elif self.ui.comboBox.currentText() == "hotp":
            self.ui.comboBox_2.setCurrentIndex(0)
            self.ui.spinBox.clear()
            self.ui.spinBox_2.clear()
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.spinBox.setEnabled(True)
            self.ui.spinBox_2.setEnabled(True)

class drawSubSubWindowConfigure(drawSubWindowConfigure):
    def __init__(self,win=ui.SubConfigWin()):
        super().__init__(win)
        self.bool = False
    
    def setBool(self):
        self.bool=True
        self.unlock()
    #Change PassKey Echo Mode
    def cpm(self):
        mode = self.ui.lineEdit_4.echoMode()
        if mode == QLineEdit.EchoMode.Password:
            self.ui.lineEdit_4.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEdit_4.setEchoMode(QLineEdit.EchoMode.Password)

    def unlock(self):
        if self.bool:
            self.ui.frame.setEnabled(True)
            self.bool=False

        if self.ui.comboBox.currentText() == "steam":
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.spinBox.setEnabled(False)
            self.ui.spinBox_2.setEnabled(False)

        elif self.ui.comboBox.currentText() == "totp":
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.spinBox.setEnabled(True)
            self.ui.spinBox_2.setEnabled(True)

        elif self.ui.comboBox.currentText() == "hotp":
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.spinBox.setEnabled(True)
            self.ui.spinBox_2.setEnabled(True)


class draw(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manager")
        self.setFixedSize(824,865)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        self.screenWidth=0
        self.screenHeight=0
        self.ui = ui.MainWin()
        self.ui.setupUi(self)
        self.ui.comboBox.addItem("查看账户配置")
        self.ui.comboBox.addItem("通过otp字符串来添加otp配置")
        self.ui.comboBox.addItem("通过二维码来添加otp配置")
        self.ui.comboBox.addItem("一个一个配置来填写")
        self.ui.comboBox.addItem("删除用户配置")
        self.ui.comboBox.currentIndexChanged.connect(self.unlockbox)
        self.ui.pushButton.clicked.connect(self.ComboxChange)
        self.ui.tabWidget.currentChanged.connect(self.showOTPPass)
        self.ui.timer = QTimer()
        self.ui.timer.timeout.connect(self.changeValue)
        self.ui.timer.start(1000)
        self.ui.timer1 = QTimer()
        self.ui.timer1.timeout.connect(self.showOTPPass)
        self.ui.timer1.start(1000)
        self.cnf = None

    def winConfigure(self):
        winC = drawSubWindowConfigure()
        winC.exec()
    def unlockbox(self):
        if self.ui.comboBox.currentText() == "通过otp字符串来添加otp配置":
            self.ui.lineEdit.setPlaceholderText("请输入otp字符串:")
            self.ui.lineEdit.setEnabled(True)
        elif self.ui.comboBox.currentText() == "通过二维码来添加otp配置":
            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit.setPlaceholderText("请输入OTP QrCodePath:")
        else:
            self.ui.lineEdit.setPlaceholderText("")
            self.ui.lineEdit.setEnabled(False)

    def changeValue(self,bool=False):
        # return
        if bool:
            file = fl.main(["-d",os.environ['USERPROFILE']+"\\"+"otpSave","-f","(\S+_)\S+\.pickle","-r"])
            try:
                file = file.__next__()
            except:
                return
            self.cnf = config().load(file)

        c = self.cnf
        self.ui.progressBar.setMinimum(0)
        if type(self.cnf) == type(config()):
            interval = self.cnf.period
            self.ui.progressBar.setMaximum(interval)
            num = int(time.time())%interval
            self.ui.progressBar.setValue(num)
            self.ui.progressBar.setFormat(f"还剩{interval - num}秒")

    def showOTPPass(self,first=None):
        if first and type(first) == type(True):
            try:
                file = fl.main(["-d",os.environ['USERPROFILE']+"\\"+"otpSave","-f","(\S+_)\S+\.pickle ","-r"])
                file = file.__next__()
            except:
                return 
            if file:
                cnf = config().load(file)
                self.cnf = cnf
                self.ui.label_3.setText(otp.otp().readConfig(cnf))
            else:
                pass
        else:
            try:
                index = self.ui.tabWidget.currentIndex()
                filename = self.ui.tabWidget.tabText(index)
                path = os.environ['USERPROFILE']+"\\"+"otpSave\\"+filename.split(":")[0]+"_"+filename.split(":")[1]+".pickle"
                cnf = config().load(path)
                self.cnf = cnf
                self.ui.label_3.setText(otp.otp().readConfig(cnf))
            except Exception as e:
                pass
    def delConfigPage(self):
        index = self.ui.tabWidget.currentIndex()
        title = self.ui.tabWidget.tabText(index)
        try:
            path = os.environ['USERPROFILE']+"\\"+"otpSave\\"+title.split(":")[0]+"_"+title.split(":")[1]+".pickle"
        except Exception as e:
            return QMessageBox.information(self,"Error","Page Not Found!!!")

        os.remove(path)
        win.flushPage()

    def flushPage(self):
        self.ui.tabWidget.clear()
        file = fl.main(["-d",os.environ['USERPROFILE']+"\\"+"otpSave","-f","(\S+_)\S+\.pickle","-r"])
        for i in file:
            fn = i.split("\\")[-1].replace(".pickle","")
            site = fn.split("_")[0]
            un = '_'.join(fn.split("_")[1:])
            cnf = config().load(i)
            subPage = drawSubSubWindowConfigure(ui.SubSubConfigWin())
            subPage.ui.comboBox.setCurrentText(cnf.type)
            subPage.ui.lineEdit.setText(cnf.userName)
            subPage.ui.lineEdit_2.setText(cnf.acName)
            subPage.ui.lineEdit_3.setText(cnf.issuer)
            subPage.ui.lineEdit_4.setText(cnf.secret)
            subPage.ui.comboBox_2.setCurrentText(cnf.algorithm)
            subPage.ui.spinBox.setValue(cnf.digits)
            subPage.ui.spinBox_2.setValue(cnf.period)
            subPage.ui.lineEdit_4.setEchoMode(QLineEdit.EchoMode.Password)
            subPage.ui.pushButton_3.clicked.connect(subPage.setBool)
            subPage.ui.pushButton_4.clicked.connect(subPage.cpm)
            self.ui.tabWidget.addTab(subPage,f"{site}:{un}")
            
    def ComboxChange(self):
        ability =self.ui.comboBox.currentText()
        if ability == "查看账户配置":
            self.flushPage()
            self.showOTPPass(True)
        
        elif ability == "通过otp字符串来添加otp配置":
            otpString = self.ui.lineEdit.text()
            cnf = config().parseOtp(otpString)
            if cnf == "ParseError":
                QMessageBox.information(self, "Error", cnf,)
                return
            cnf.save()
            self.flushPage()
        
        elif ability == "通过二维码来添加otp配置":
            if self.ui.lineEdit.text():
                cnf = config().readFromQR(self.ui.lineEdit.text())
                
            else:
                qr = ImageGrab.grab(bbox=(0, 0, self.screenWidth,self.screenHeight))
                try:
                    cnf = config().readFromQR(qr)
                except:
                    QMessageBox.information(self,"Error","QrParseError")
                    return
                cnf.save()
        
        elif ability == "一个一个配置来填写":
            self.winConfigure()

        elif ability == "删除用户配置":
            self.delConfigPage()
 
def parse_usage(args=None):
    global win
    usage = "%prog <option> <usage>"
    parser = optparse.OptionParser(usage=usage,version="%prog 1.0")
    parser.add_option("-l","--list",dest="List",action="store_true",help="查看存储的otp配置")
    parser.add_option("-c","--choice",dest="Chose",type="int",help="选择查看哪个配置,用序号来选择")
    parser.add_option("-s","--string",dest="String",help="通过otp字符串来添加otp配置")
    parser.add_option("-q","--qrcode",dest="Qrcode",help="通过二维码来添加otp配置")
    parser.add_option("-o","--other",dest="Other",help="通过一个一个来填写配置（不推荐）")
    parser.add_option("-d","--delete",dest="Delete",type="int",help="选择删除otp配置，用户号来删除")
    parser.add_option("-u","--ui",dest="UI",action="store_true",help="使用ui界面（未做完）")
    (options,args) = parser.parse_args(args if args else sys.argv)
    List = options.List
    Chose = options.Chose
    String = options.String
    Qrcode = options.Qrcode
    Other = options.Other
    Delete = options.Delete
    UI = options.UI
    delLock = True
    if os.path.exists(os.environ['USERPROFILE']+"\\"+"otpSave"):
        D = os.listdir(os.environ['USERPROFILE']+"\\"+"otpSave")
    else:
        os.makedirs(os.environ['USERPROFILE']+"\\"+"otpSave")
        D= os.listdir(os.environ['USERPROFILE']+"\\"+"otpSave")
    
    if UI:
        app = QApplication([])
        win = draw()
        win.screenWidth = grr()[0]
        win.screenHeight = grr()[1]
        win.show()
        app.exec()

    if List:
        num=1
        for i in D:
            print(f"{num}.{i.split('_')[0]} {i.split('_')[1].split('.')[0]}")
            num+=1

    if String:
        
        delLock = False
        cnf = conf.config().parseOtp(String)
        cnf.save()
    
    if Qrcode:
        
        delLock = False
        
        if not os.path.exists(Qrcode):
            sys.exit("Qrcode picture is not fond,Please Check the pciture path !!!")
        
        cnf = conf.config().readFromQR(Qrcode)
        cnf.save()
    
    if Other:
    
        Type = input("Please Input the otp Type(steam,totp,hotp):")
        
        if Type == "steam":
            un = input("Please Input the otp UserName:")
            sercet = input("Please Input the otp key:")
            S = f"otpauth://totp/steam:{un}?secret={sercet}&issuer=steam"
            cnf = conf.config().parseOtp(S)
            cnf.save()

        elif Type == "totp":
            un = input("Please Input the otp UserName:")
            an = input("Please Input the site name:")
            encType = input("Please input the hash function name:")
            length = input("Please input the once code length:")
            issuer = input("Please input the issuer:")
            period = input("Please input how time to reflush(s):")
            key = input("Please input totp key:")
            
            if an == "" and issuer != "":
                an = issuer
            elif an == "" and issuer == "":
                an = issuer = input("Please Input the site name again:")
            else:
                issuer == an
            
            if encType == "":
                encType = "sha1"
            
            if length == "":
                length = 6
            
            if period == "":
                period = 30
            
            if key == "":
                key = input("Please try agian input totp key:")
                if sercet == "":
                    sys.exit("你真是不识好歹啊!!!")

            cnf = conf.config(un,an,encType,length,issuer,period,key,"totp")
            cnf.save()
        elif Type == "hotp":
            sys.exit("暂不支持")
        
        else:
            sys.exit("Error OTP Type!!!!")


    if Delete and delLock:
        
        if len(D) < Delete:
            sys.exit("Chose Error!!!")
        
        path = os.environ['USERPROFILE']+"\\"+"otpSave\\"+D[Delete-1]
        os.remove(path)
    
    if Chose:
        if len(D) < Chose:
            sys.exit("Chose Error!!!")
        
        path = os.environ['USERPROFILE']+"\\"+"otpSave\\"+D[Chose-1]
        cnf = conf.config().load(path)
        oneCode = otp.otp().readConfig(cnf)
        print(f"来自{cnf.acName if cnf.acName else cnf.issuer}中用户名为{cnf.userName}的一次性密码是:{oneCode}")
        
def main():
    if "-u" or "--UI" not in sys.argv:
        sys.argv.append("-u")
    parse_usage()

if __name__=="__main__":
    main()