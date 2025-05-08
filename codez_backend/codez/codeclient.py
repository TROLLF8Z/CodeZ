# coding: utf-8
# author: TROLLF8Z
# createdate: 2024/08/01

"""
该程序是一个TCP网络客户端
用于向服务端发送 Python 代码, 并获取返回
This module is a TCP network client
It's major job is to send Python code to the server and retrieve the return
"""

# imports
import socket

codeclient_version = '1.1.2.240805' # 版本号

class CodeClient:
    # 初始化x
    def __init__(self, ip, port, maxTimeouts = 5, srcFile = ''):
        
        # 创建socket对象，连接服务端
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
        except socket.error as msg:
            print(msg)
        else:
            self.sock.send('|-!-!-!-CodeClientValidate-!-!-!-|'.encode('utf-8'))    # 进行身份验证
            self.recvMode = 1                                                   # 接收数据的处理分支
            self.timeoutRetries = 0                                           # 超时次数记录，用于判断是否断开连接
            self.maxTimeouts = maxTimeouts                        # 允许超时次数阈值，当超时次数达到这个值时将被认为已经断开连接
            self.srcFile = srcFile                                                   # 代码文件路径
            self.sendpaks = []                                                       # 分包文件列表
            self.nowindex = 0                                                       # 当前接收的分包索引
            self.active = True                                                        # 客户端是否继续运行
            self.receiveData()                                                        # 进入数据接收函数
    
    
    # 获取待接收分包索引
    def getPakIndex(self):
        try:
            ret = self.sendpaks.index('emptypak')
            
        except ValueError:
            ret = -1
            
        return ret
    
    
    # 分包接收完毕后的处理
    def recvFinish(self):
        # 先开始拼接分包
        tmpfile = ''    # 存放拼接文件的临时变量
        for pak in self.sendpaks:
            if tmpfile:
                tmpfile += pak
            else:
                tmpfile = pak
        
        # 保存返回结果
        with open('runret.txt', 'wb') as f:
            f.write(tmpfile)
        
        # 通知服务端接收完毕并主动断开连接
        self.sock.send('||||RecvFinish||||'.encode('utf-8'))
        self.sock.close()
        self.active = False
    
    
    # 数据接收函数
    def receiveData(self):
        self.sock.settimeout(3) # 设置超时时间为3秒， 3秒未接收到回复则视为一次超时
        
        while self.active:
            try:
                ret = self.sock.recv(2000) # 接收服务器数据
                
            except socket.timeout: # 超时处理，若超时次数达到阈值则将被视为断开连接，直接结束
                # print('ni')
                self.timeoutRetries += 1
                if self.timeoutRetries >= self.maxTimeouts:
                    self.sock.close()
                    break
                # self.sock.send('超时了喂'.encode('utf-8'))
                
            except AttributeError:
                pass
            
            except ConnectionResetError:
                break
                
            else:
                self.timeoutRetries = 0 # 获取到数据，将超时次数重置为 0
                
                # 分支 1
                if self.recvMode == 1:
                    ret = ret.decode('utf-8') # 分支 1 只会接收到字符串返回，直接解码
                    
                    if ret == '||||IDVerified||||': # 服务器返回了验证通过信息，开始处理并发送文件
                    
                        # 先将文件按照分包大小切割成分包并添加进分包文件列表中
                        paksize = 1024 # 分包大小
                        
                        with open (self.srcFile, 'rb') as f:
                            data = f.read(paksize)  # 从代码文件中按照分包大小逐次读取内容
                            while data:             # 若文件已读取完毕，data将会为空，则直接跳出循环
                                self.sendpaks.append(data)
                                data = f.read(paksize)
                        
                        # 发送分包总数
                        # print(len(self.sendpaks))
                        s = '||||TotalPaks||||%d' % (len(self.sendpaks))
                        self.sock.send(s.encode('utf-8'))
                    
                    # 服务器发送开始发送文件请求，发送第一个分包
                    elif ret == '||||RecvBegin||||':
                        self.sock.send('||||Paks||||'.encode('utf-8') + self.sendpaks[0]) 
                    
                    # 服务器发送后续分包请求，根据索引发送对应分包
                    elif ret[:18] == '||||PakRequest||||':
                        try:
                            ret = int(ret[18:])
                        except ValueError:
                            pass
                        else:
                            self.sock.send('||||Paks||||'.encode('utf-8') + self.sendpaks[ret])
                    
                    # 服务器准备发送运行返回文件，切换分支
                    elif ret == '||||RecvPrep||||':
                        self.recvMode = 2
                        self.sock.send('||||Ready2Recv||||'.encode('utf-8'))
                
                # 分支 2
                elif self.recvMode == 2:
                    # 判断包长度是否低于50, 若低于50很可能是文本信息，或也可能是尾包
                    if len(ret) < 50:
                        # 仅当包长度低于50时才进行UTF-8解码，节省资源
                        try:
                            tmpret = ret.decode('utf-8')
                        except:
                            pass
                        
                        # 服务端发来包总数，格式为 "||||TotalPaks||||分包总数"
                        if tmpret[:17] == '||||TotalPaks||||':
                            try:
                                tmpret = int(tmpret[17:]) # 去除包首信息
                            except:
                                pass
                            else:
                                # 创建一个长度与包总数对应的列表
                                # 用于严格控制每个接收的分包，防止丢包跳包
                                self.sendpaks = ['emptypak'] * tmpret
                                self.nowindex = 0 # 初始化当前分包索引
                                
                                self.sock.send('||||RecvBegin||||'.encode('utf-8')) # 通知服务端开始发送第一个包
                                
                        elif tmpret[:12] == '||||Paks||||':                     # 验证包首信息
                            ret = ret[12:]                                      # 去除包首信息
                            self.sendpaks[-1] = ret                             # 接收的是尾包，直接置于分包列表最后一位
                            self.nowindex = self.getPakIndex()                  # 防止跳包，再次检查待接收的分包索引
                            
                            if self.nowindex == -1:                             # 若所有分包已接收完毕
                                self.recvFinish()
                            
                    
                    # 分包长度不低于50，则应该是正常运行返回文件分包
                    else:
                        if ret[:12].decode('utf-8') == '||||Paks||||':          # 验证包首信息
                            ret = ret[12:]                                      # 去除包首信息
                            self.sendpaks[self.nowindex] = ret                  # 将分包文件置于接受分包列表内对应索引处
                            self.nowindex = self.getPakIndex()                  # 获取待接收的分包索引
                            
                            if self.nowindex == -1:                             # 若所有分包已接收完毕
                                self.recvFinish()
                            
                            else:
                                # 发送分包请求
                                s = '||||PakRequest||||%d' % (self.nowindex)
                                self.sock.send(s.encode('utf-8'))

if __name__ == '__main__':
    # a = CodeClient('106.52.88.53', 2971, srcFile = 'oof.py')
    a = CodeClient('localhost', 2971, srcFile = 'tests.py')