# coding=utf-8

import sys
import os
import re

class Parser():

    A_COMMAND = 0 # A指令
    C_COMMAND = 1 # C指令
    L_COMMAND = 2 # 伪指令

    COMMADN_NAME = ['A_COMMAND','C_COMMAND','L_COMMAND']

    """语法分析器"""
    def __init__(self, asmPath):
        super(Parser, self).__init__()
        self._file = open(asmPath,mode='r',encoding='utf-8')
        self._lineCnt = -1;

    def hasMoreCommands(self):
        if self._file == None:
            return False

        while True:
            prePos = self._file.tell()
            rawline = self._file.readline()
            self._lineCnt+=1
            readSize = len(rawline)
            if readSize <=0 :
                self._file.close()
                self._file = None
                return False

            line = rawline.strip()
            isEmpty = len(line)<=0
            isComment = False if isEmpty else line.startswith('//')
            skip = isEmpty or isComment
            if not skip:
                self._file.seek(prePos,0) # 如果当前读取行就是有效行，回退文件读取位置
                self._lineCnt-=1
                return True
            else:
                print("跳过行{0}:{1}".format(self._lineCnt,rawline.rstrip()))

    def advance(self):
        rawline = self._file.readline()
        self._lineCnt+=1
        self._currLine = rawline.strip().replace(' ','')
        print('当前行内容为:'+self._currLine)

    def commandType(self):
        if self._currLine[0]=='@':
            return Parser.A_COMMAND
        elif self._currLine[0]=='(' and self._currLine[-1]==')':
            return Parser.L_COMMAND
        else:
            return Parser.C_COMMAND

    def symbol(self):
        t = self.commandType()
        if t == Parser.A_COMMAND:
            return self._currLine[1:]
        elif t == Parser.L_COMMAND:
            return self._currLine[1:-1]
        else:
            return None

    def dest(self):
        t = self.commandType()
        if t == Parser.C_COMMAND:
            i = self._currLine.find('=')
            if i >= 0:
                d = self._currLine[:i].strip()
                if not d in ['M','D','MD','A','AM','AD','AMD']:
                    raise Exception('解析到错误的dest:{0}，在{1}第行'.format(d,self._lineCnt))

                return d
            else:
                return 'null'
        else:
            return None

    def comp(self):
        t = self.commandType()
        if t == Parser.C_COMMAND:
            iEq = self._currLine.find('=')

            iQt = self._currLine.find(';')
            iQt = len(self._currLine) if iQt<0 else iQt

            c = self._currLine[iEq+1:iQt].strip()
            if not c in ['0','1','-1','D','A','!D','!A','-D','-A','D+1','A+1','D-1','A-1','D+A','D-A','A-D','D&A','D|A','M','!M','-M','M+1','M-1','D+M','D-M','M-D','D&M','D|M']:
                    raise Exception('解析到错误的comp:{0}，在{1}第行'.format(c,self._lineCnt))

            return c
        else:
            return None

    def jump(self):
        t = self.commandType()
        if t == Parser.C_COMMAND:
            i = self._currLine.find(';')
            if i >= 0:
                j= self._currLine[i+1:].strip()
                if not j in ['JGT','JEQ','JGE','JLT','JNE','JLE','JMP']:
                    raise Exception('解析到错误的jump:{0}，在{1}第行'.format(j,self._lineCnt))

                return j
            else:
                return 'null'
        else:
            return None



def main():
    inputPath = sys.argv[1]
    print('输入文件为:{0}'.format(inputPath))
    parser = Parser(inputPath)
    while parser.hasMoreCommands():
        parser.advance()
        t = Parser.COMMADN_NAME[parser.commandType()]
        s = parser.symbol()
        d = parser.dest()
        c = parser.comp()
        j = parser.jump()
        print('type:{0},symbol:{1},dest:{2},comp:{3},jump:{4}'.format(t,s,d,c,j))

main()