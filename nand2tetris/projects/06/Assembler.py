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
        self._lineCnt = -1

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
        commentIdx = rawline.find("//")
        if commentIdx >= 0:
            rawline = rawline[:commentIdx]

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

class Code():
    _destDict = {
        'null':0,
        'M':0b1,
        'D':0b10,
        'MD':0b11,
        'A':0b100,
        'AM':0b101,
        'AD':0b110,
        'AMD':0b111
    }

    _compDict = {
        '0'  :0b0101010,
        '1'  :0b0111111,
        '-1' :0b0111010,
        'D'  :0b0001100,
        'A'  :0b0110000,
        '!D' :0b0001111,
        '!A' :0b0110001,
        '-D' :0b0001111,
        '-A' :0b0110011,
        'D+1':0b0011111,
        'A+1':0b0110111,
        'D-1':0b0001110,
        'A-1':0b0110010,
        'D+A':0b0000010,
        'D-A':0b0010011,
        'A-D':0b0000111,
        'D&A':0b0000000,
        'D|A':0b0010101,
        'M'  :0b1110000,
        '!M' :0b1110001,
        '-M' :0b1110011,
        'M+1':0b1110111,
        'M-1':0b1110010,
        'D+M':0b1000010,
        'D-M':0b1010011,
        'M-D':0b1000111,
        'D&M':0b1000000,
        'D|M':0b1010101
    }

    _jumpDict = {
        'null':0,
        'JGT':0b1,
        'JEQ':0b10,
        'JGE':0b11,
        'JLT':0b100,
        'JNE':0b101,
        'JLE':0b110,
        'JMP':0b111
    }

    @classmethod
    def dest(cls,name):
        """3 bits"""
        return cls._destDict[name]

    @classmethod
    def comp(cls,name):
        """7 bits"""
        return cls._compDict[name]

    @classmethod
    def jump(cls,name):
        """3 bits"""
        return cls._jumpDict[name]


class SymbolTable():
    """符号表"""
    def __init__(self):
        self._dict = {}
        # 加入预定义符号
        self._dict['SP'] = 0
        self._dict['LCL'] = 1
        self._dict['ARG'] = 2
        self._dict['THIS'] = 3
        self._dict['THAT'] = 4
        for i in range(16):
            self._dict['R'+str(i)] = i
        
        self._dict['SCREEN'] = 16384
        self._dict['KBD'] = 24576

    def addEntry(self,symbol,address):
        self._dict[symbol] = address

    def contains(self,symbol):
        return symbol in self._dict

    def GetAddress(self,symbol):
        return self._dict[symbol]


def main():
    inputPath = sys.argv[1]
    print('输入文件为:{0}'.format(inputPath))
    outputPath = inputPath.replace('.asm','_yx.hack')
    # 第一遍，收集符号
    print('========第一遍，收集符号========')
    address = 0
    tbl = SymbolTable()
    parser = Parser(inputPath)
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == Parser.L_COMMAND:
            symbol = parser.symbol()
            if not tbl.contains(symbol):
                tbl.addEntry(symbol,address)
                print('收集到符号:{0}={1}'.format(symbol,address))
        else:
            address+=1
    # 第二遍，汇编
    print('========第二遍，汇编========')
    valAddress = 16
    parser = Parser(inputPath)
    output = open(outputPath,mode='w',encoding='utf-8')
    while parser.hasMoreCommands():
        parser.advance()
        t = Parser.COMMADN_NAME[parser.commandType()]
        s = parser.symbol()
        d = parser.dest()
        c = parser.comp()
        j = parser.jump()
        print('type:{0},symbol:{1},dest:{2},comp:{3},jump:{4}'.format(t,s,d,c,j))
        if t == Parser.COMMADN_NAME[Parser.A_COMMAND]:
            isSymbol = tbl.contains(s)
            if isSymbol:
                addr = '{0:b}'.format(tbl.GetAddress(s)).zfill(16)
            elif not s.isnumeric():
                tbl.addEntry(s,valAddress)
                addr = '{0:b}'.format(valAddress).zfill(16)
                valAddress += 1
            else:
                addr = '{0:b}'.format(int(s)).zfill(16)

            print('symbol address:'+addr)
            output.write(addr+'\n')
        elif t == Parser.COMMADN_NAME[Parser.C_COMMAND]:
            destCode = '{0:b}'.format(Code.dest(d)).zfill(3)
            compCode = '{0:b}'.format(Code.comp(c)).zfill(7)
            jumpCode = '{0:b}'.format(Code.jump(j)).zfill(3)
            print('dest code:{0},comp code:{1},jump code:{2}'.format(destCode,compCode,jumpCode))
            output.write('111'+compCode+destCode+jumpCode+'\n')

    output.close()

main()