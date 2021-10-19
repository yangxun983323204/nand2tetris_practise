# coding=utf-8

import sys
import os

class Parser():

    def hasMoreCommands():
        pass

    def advance():
        pass

    def commandType():
        pass

    def arg1():
        pass
    
    def arg2():
        pass

class CodeWriter():

    def setFileName(filename):
        pass

    def writeArithmetic(command):
        pass

    def writePushPop(command):
        pass

    def close():
        pass

def main():
    inputPath = sys.argv[1]
    print('输入文件为:{0}'.format(inputPath))
    fileList = []
    if inputPath.endswith('.vm'):
        print("输入的是文件")
        fileList.append(inputPath)
    else:
        print("输入的是目录")
        for root,dirs,files in os.walk(inputPath):
            for f in files:
                if f.endswith('.vm'):
                    fileList.append(os.path.join(root,f))

    for file in fileList:
        print("待处理文件:"+file)

main()