# coding=utf-8

import sys
import os
from pathlib import Path

class Parser():

    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8

    def __init__(self,path):
        super(Parser, self).__init__()
        self._file = open(path,mode='r',encoding='utf-8')
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

        self._currLine = rawline.strip()
        print('当前行内容为:'+self._currLine)

    def commandType(self):
        words = self._currLine.split(' ')
        c = words[0]
        if c in ['add','sub','neg','eq','gt','lt','and','or','not']:
            return Parser.C_ARITHMETIC
        elif c == 'push':
            return Parser.C_PUSH
        elif c == 'pop':
            return Parser.C_POP
        elif c == 'label':
            return Parser.C_LABEL
        elif c == 'goto':
            return Parser.C_GOTO
        elif c == 'if-goto':
            return Parser.C_IF
        elif c == 'function':
            return Parser.C_FUNCTION
        elif c == 'call':
            return Parser.C_CALL
        elif c == 'return':
            return Parser.C_RETURN
        else:
            raise Exception('解析到错误的指令:{0}，在{1}第行'.format(c,self._lineCnt))

    def arg1(self):
        t = self.commandType()
        words = self._currLine.split(' ')
        if t == Parser.C_ARITHMETIC:
            return words[0]
        elif t == Parser.C_RETURN:
            raise Exception('不应在指令为return时访问arg1，在{0}第行'.format(self._lineCnt))
        else:
            return words[1]
    
    def arg2(self):
        t = self.commandType()
        words = self._currLine.split(' ')
        if t in [Parser.C_PUSH,Parser.C_POP,Parser.C_FUNCTION,Parser.C_CALL]:
            return int(words[2])
        else:
            raise Exception('不应在指令为{0}时访问arg2，在{1}第行'.format(words[0],self._lineCnt))

class CodeWriter():

    def __init__(self,path):
        self._file = open(path,mode='w',encoding='utf-8')

    def setFileName(self,filename):
        self._currVMName = Path(filename).stem
        self._file.write("\\\\===={0}====\n".format(filename))

    def writeArithmetic(self,command):
        # add,sub,eq,gt,lt,and,or 是出栈两个
        # neg,not 是出栈一个
        asm = [self.__comment(command)]
        asm.extend(self.__vmStackPopD())
        if command in ['add','sub','eq','gt','lt','and','or']:
            asm.extend(self.__vmStackMapM())
            if command == 'add':
                asm.append('D=D+M')
            elif command == 'sub':
                asm.append('D=M-D')
            else:
                asm.append(command + ' 未实现')


            asm.extend(self.__vmStackDec()) # 上面调用了__vmStackMapM并未出栈，这里在运算完成后，把操作数出栈
        else:
            if command == 'neg':
                asm.append('D=-D')
            else:
                asm.append('D=!D')
        
        asm.extend(self.__vmStackPushD()) # 把运算结果从D入栈
        self.__writeAsmList(asm)

    def writePushPop(self,commandType,segment,index):
        if commandType == Parser.C_PUSH:
            asm = "push 未实现\n"
        else:
            asm = "pop 未实现\n"

        self._file.write(asm)

    def close(self):
        self._file.close()

    def __vmStackPopD(self):
        '''把栈顶弹出到D寄存器'''
        asm = []
        asm.append(self.__comment('开始：把栈顶弹出到D寄存器'))
        asm.append('@SP')
        asm.append('A=M')
        asm.append('D=M')
        asm.extend(self.__vmStackDec())
        asm.append(self.__comment('完成：把栈顶弹出到D寄存器'))
        return asm

    def __vmStackMapM(self):
        '''使M指向栈顶'''
        asm = []
        asm.append('@SP')
        asm.append('A=M')
        return asm

    def __vmStackPushD(self):
        '''把D寄存器值压入栈中'''
        asm = []
        asm.append(self.__comment('开始：把D寄存器值压入栈中'))
        asm.extend(self.__vmStackInc())
        asm.append('A=M')
        asm.append('M=D')
        asm.append(self.__comment('完成：把D寄存器值压入栈中'))
        return asm

    def __vmStackDec(self):
        '''栈-1'''
        asm = []
        asm.append('@SP')
        asm.append('M=M-1')
        return asm

    def __vmStackInc(self):
        '''栈+1'''
        asm = []
        asm.append('@SP')
        asm.append('M=M+1')
        return asm 
    
    def __comment(self,str):
        return '\\\\ '+str

    def __writeAsmList(self,asms):
        for line in asms:
            self._file.write(line)
            self._file.write('\n')

def main():
    inputPath = sys.argv[1]
    print('输入文件为:{0}'.format(inputPath))
    outputPath = ''
    fileList = []
    if inputPath.endswith('.vm'):
        print("输入的是文件")
        fileList.append(inputPath)
        outputPath = inputPath.replace('.vm','.asm')
    else:
        print("输入的是目录")
        outputPath = inputPath+'.asm'
        for root,dirs,files in os.walk(inputPath):
            for f in files:
                if f.endswith('.vm'):
                    fileList.append(os.path.join(root,f))

    print('输出文件为:{0}'.format(outputPath))
    writer = CodeWriter(outputPath)
    for file in fileList:
        print("待处理文件:"+file)
        writer.setFileName(file)
        parser = Parser(file)
        while parser.hasMoreCommands():
            parser.advance()
            t = parser.commandType()
            if t == Parser.C_ARITHMETIC:
                writer.writeArithmetic(parser.arg1())
            elif t == Parser.C_PUSH or t == Parser.C_POP:
                writer.writePushPop(t,parser.arg1(),parser.arg2())
    
    writer.close()

main()