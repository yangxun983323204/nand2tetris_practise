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
        self._asm = []
        self._currLineNum = 0
        self._vmCmdCnt=0

    def setFileName(self,filename):
        self._currVMName = Path(filename).stem
        self.__asmComment("file:{0}".format(filename))

    def writeArithmetic(self,command):
        # add,sub,eq,gt,lt,and,or 是出栈两个操作数,一个到D、另一个使用M，并在操作完成后出栈
        # neg,not 是出栈一个操作数到D
        # 所有操作都把结果保存在D寄存器，并最终压入栈
        self.__asmComment("vm cmd:"+command)
        self.__vmStackPopD()
        if command in ['add','sub','eq','gt','lt','and','or']:
            self.__vmStackMapM()
            if command == 'add':
                self.__asmCmd('D=D+M','add')
            elif command == 'sub':
                self.__asmCmd('D=M-D','sub')
            elif command == 'eq':
                self.__asmCmd('D=M-D','eq')
                self.__vmIfD('JEQ')
            elif command == 'gt':
                self.__asmCmd('D=M-D','gt')
                self.__vmIfD('JGT')
            elif command == 'lt':
                self.__asmCmd('D=M-D','lt')
                self.__vmIfD('JLT')
            elif command == 'and':
                self.__asmCmd('D=D&M','and')
            elif command == 'or':
                self.__asmCmd('D=D|M','or')
            else:
                raise Exception('未识别的第{0}个vm指令:{1}'.format(self._vmCmdCnt,command))

            self.__vmStackDec()
        else:
            if command == 'neg':
                self.__asmCmd('D=-D','neg')
            elif command == 'not':
                self.__asmCmd('D=!D','not')
            else:
                raise Exception('未识别的第{0}个vm指令:{1}'.format(self._vmCmdCnt,command))
        
        self.__vmStackPushD() # 把运算结果从D入栈
        self._vmCmdCnt += 1

    def writePushPop(self,commandType,segment,index):
        if commandType == Parser.C_PUSH:
            self.__asmComment("vm cmd:{0} {1} {2}".format('push',segment,index))
            if segment == 'constant':
                self.__vmPushConstant(index)
            else:
                self.__asmComment("vm cmd:{0} {1} {2} 未实现".format(commandType,segment,index))
        elif commandType == Parser.C_POP:
            self.__asmComment("vm cmd:{0} {1} {2}".format('pop',segment,index))
            self.__asmComment("vm cmd:pop 未实现")
        else:
            raise Exception('未识别的第{0}个vm指令:{1} {2} {3}'.format(self._vmCmdCnt,commandType,segment,index))

        self._vmCmdCnt += 1

    def close(self):
        self.__flush()
        self._file.close()

    # 栈指针应始终指向栈顶元素的下一个，即栈指针应指向写入位置

    def __vmStackPopD(self):
        '''把栈顶弹出到D寄存器'''
        self.__vmStackDec()
        self.__asmInlineComment('[begin]:pop stack to D',-2)
        self.__asmCmd('A=M')
        self.__asmCmd('D=M')
        self.__asmInlineComment('[end]:pop stack to D')

    def __vmStackPushD(self):
        '''把D寄存器值压入栈中'''
        self.__asmCmd('@SP','[begin]:push D to stack')
        self.__asmCmd('A=M')
        self.__asmCmd('M=D')
        self.__vmStackInc()
        self.__asmInlineComment('[end]:push D to stack')

    def __vmStackMapM(self):
        '''使M等于栈顶元素，也即A寄存器的地址指向SP-1'''
        self.__asmCmd('@SP')
        self.__asmCmd('A=M')
        self.__asmCmd('A=A-1')

    def __vmStackDec(self):
        '''栈-1'''
        self.__asmCmd('@SP')
        self.__asmCmd('M=M-1')

    def __vmStackInc(self):
        '''栈+1'''
        self.__asmCmd('@SP')
        self.__asmCmd('M=M+1')
    
    def __vmIfD(self,jmpCode):
        '''对D寄存器作if判断'''
        self.__asmCmd('A='+self.__asmGetAutoLabel('IF_TRUE',5))# IF_TRUE在此后第5条指令
        self.__asmCmd('D;{0}'.format(jmpCode))
        self.__asmCmd('D=1')# False
        self.__asmCmd('A='+self.__asmGetAutoLabel('IF_END',3))# IF_END在此后第3条指令
        self.__asmCmd('0;JMP')
        self.__asmAutoLabel('IF_TRUE')
        self.__asmCmd('D=-1')# True
        self.__asmAutoLabel('IF_END')

    def __vmPushConstant(self,val):
        '''将常量压入栈中'''
        self.__asmCmd('@{0}'.format(val))
        self.__asmCmd('D=A')
        self.__vmStackPushD()

    def __asmCmd(self,cmd,comment=None):
        '''写入一条指令，可以传入comment字段，将在当前行添加注释'''
        self._asm.append(cmd)
        self._currLineNum += 1
        if comment!=None:
            self.__asmInlineComment(comment)

    def __asmAutoLabel(self,name):
        '''写入一条自动标签，自动标签后面带有指令行数，以避免重复'''
        self._asm.append('(LABEL_AUTO_{0}_{1})'.format(name,self._currLineNum))

    def __asmGetAutoLabel(self,name,offset):
        '''获取自动标签，offset用来指定相对当前指令的偏移'''
        return 'LABEL_AUTO_{0}_{1}'.format(name,self._currLineNum+offset)

    def __asmComment(self,text):
        '''写入一条注释'''
        self._asm.append('// '+text)

    def __asmInlineComment(self,text,idx=-1):
        '''给指定行后添加内注释'''
        if '//' in self._asm[idx]:
            self._asm[idx] += ' '+text
        else:
            self._asm[idx] = self._asm[idx].ljust(35) + '// '+text

    def __flush(self):
        for line in self._asm:
            self._file.write(line)
            self._file.write('\n')
        
        self._asm = []

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