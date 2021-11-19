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
        self._asm = []                  # 存放生成的每一条汇编指令
        self._currVMFileName = ''       # 当前正在汇编的vm文件名字
        self._currVMCmdCnt=0            # 当前所处的vm指令条数
        self._currVMFuncName = 'global' # 当前函数名
        self._currAsmCmdCnt = 0         # 当前生成的asm指令条数
        self._hasSysInit = False        # 是否检测到Sys.Init函数
        self._initBegin = 0             # Init指令起始索引
        self._initEnd = 0               # Init指令终止索引

    def setFileName(self,filename):
        self._currVMFileName = Path(filename).stem
        self.__asmComment("file:{0}".format(filename))

    def writeInit(self):
        '''生成vm初始化的汇编代码'''
        self._initBegin = len(self._asm)
        self.__asmComment("====Init begin====")
        self.__asmCmd('@256')
        self.__asmCmd('D=A')
        self.__asmCmd('@SP')
        self.__asmCmd('M=D')
        self.writeCall('Sys.init',0)
        self.__asmComment("====Init end====")
        self._initEnd = len(self._asm)

    def writeArithmetic(self,command):
        # add,sub,eq,gt,lt,and,or 是出栈两个操作数,一个到D、另一个使用M，并在操作完成后出栈
        # neg,not 是出栈一个操作数到D
        # 所有操作都把结果保存在D寄存器，并最终压入栈
        self.__asmComment("vm cmd:"+command)
        self.__vmStackPopToD()
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
                raise Exception('未识别的第{0}个vm指令:{1}'.format(self._currVMCmdCnt,command))

            self.__vmStackDec()
        else:
            if command == 'neg':
                self.__asmCmd('D=-D','neg')
            elif command == 'not':
                self.__asmCmd('D=!D','not')
            else:
                raise Exception('未识别的第{0}个vm指令:{1}'.format(self._currVMCmdCnt,command))
        
        self.__vmStackPushFromD() # 把运算结果从D入栈
        self._currVMCmdCnt += 1

    def writePushPop(self,commandType,segment,index):
        if commandType == Parser.C_PUSH:
            self.__asmComment("vm cmd:{0} {1} {2}".format('push',segment,index))
            if segment == 'constant':
                self.__vmStackPushFromConstant(index)
            elif segment in ['local','argument','this','that']:
                self.__vmStackPushFromSegment(segment,index)
            elif segment in ['pointer','temp']:
                self.__vmStackPushFromPointer(segment,index)
            elif segment == 'static':
                self.__vmStackPushFromStatic(index)
            else:
                self.__asmComment("vm cmd:{0} {1} {2} 未实现".format(commandType,segment,index))
        elif commandType == Parser.C_POP:
            self.__asmComment("vm cmd:{0} {1} {2}".format('pop',segment,index))
            #constant不接受数据弹栈
            if segment in ['local','argument','this','that']:
                self.__vmStackPopToSegment(segment,index)
            elif segment in ['pointer','temp']:
                self.__vmStackPopToPointer(segment,index)
            elif segment == 'static':
                self.__vmStackPopToStatic(index)
            else:
                self.__asmComment("vm cmd:{0} {1} {2} 未实现".format(commandType,segment,index))
        else:
            raise Exception('未识别的第{0}个vm指令:{1} {2} {3}'.format(self._currVMCmdCnt,commandType,segment,index))

        self._currVMCmdCnt += 1

    def writeLabel(self,label):
        '''vm label'''
        self.__asmComment("vm cmd:label "+label)
        self.__asmScopeLabel(label)

    def writeGoto(self,label):
        '''vm goto'''
        self.__asmComment("vm cmd:goto "+label)
        self.__asmCmd('@'+self.__asmGetScopeLabel(label))
        self.__asmCmd('0;JMP')

    def writeIf(self,label):
        '''vm if-goto'''
        self.__asmComment("vm cmd:if-goto "+label)
        self.__vmStackPopToD()
        self.__asmCmd('@'+self.__asmGetScopeLabel(label))
        self.__asmCmd('D;JNE')
        pass

    def writeCall(self,functionName,numArgs):
        '''vm call'''
        if numArgs<0:
            raise Exception('第{0}个vm指令:call {1} {2}，numArgs小于0'.format(self._currVMCmdCnt,functionName,numArgs))

        self.__asmComment("vm cmd:call {0} {1}".format(functionName,numArgs))
        # vm call命令是不包含参数压栈的，参数压栈在高级语言编译成vm语言时产生
        # 保存返回地址和vm寄存器状态
        returnLabel = '{0}_CALL_{1}_RETURN'.format(self._currVMFuncName,functionName)
        returnRefStub = self.__asmAutoLabelRefStub(returnLabel) # 返回处的自动标签行号难得数，用stub去延迟生成吧
        self.__asmCmd('D=A')
        self.__vmStackPushFromD()
        self.__asmCmd('@LCL')
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()
        self.__asmCmd('@ARG')
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()
        self.__asmCmd('@THIS')
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()
        self.__asmCmd('@THAT')
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()
        # 设置新的ARG段地址
        self.__asmCmd('@SP')
        self.__asmCmd('D=M')
        if numArgs > 0:
            self.__asmCmd('@'+str(numArgs))
            self.__asmCmd('D=D-A')

        self.__asmCmd('@5')
        self.__asmCmd('D=D-A')
        self.__asmCmd('@ARG')
        self.__asmCmd('M=D')
        # 设置新的LCL段地址
        self.__asmCmd('@SP')
        self.__asmCmd('D=M')
        self.__asmCmd('@LCL')
        self.__asmCmd('M=D')
        # 跳转到被调函数
        self.__asmCmd('@'+functionName)
        self.__asmCmd('0;JMP')
        # 声明返回地址
        self.__asmAutoLabel(returnLabel)
        returnRefStub.Complete()

    def writeReturn(self):
        '''vm return'''
        self.__asmComment("vm cmd:return")
        # FRAME = LCL   FRAME地址暂存在R13
        self.__asmCmd('@LCL')
        self.__asmCmd('D=M')
        self.__asmCmd('@R13')
        self.__asmCmd('M=D')
        # RET = *(FRAME-5)  RET地址暂存在R14
        self.__asmCmd('@5')
        self.__asmCmd('D=D-A')
        self.__asmCmd('A=D')
        self.__asmCmd('D=M')
        self.__asmCmd('@R14')
        self.__asmCmd('M=D')
        # *ARG=pop()   当前栈顶是被调函数返回值，*ARG是被调函数帧清栈后的栈顶地址，**ARG是栈顶元素
        self.__vmStackPopToD()
        self.__asmCmd('@ARG')
        self.__asmCmd('A=M')
        self.__asmCmd('M=D')
        # SP = ARG+1  被调函数帧清栈
        self.__asmCmd('@ARG')
        self.__asmCmd('D=M')
        self.__asmCmd('D=D+1')
        self.__asmCmd('@SP')
        self.__asmCmd('M=D')
        # 恢复vm寄存器
        self.__asmCmd('@R13')   
        self.__asmCmd('D=M')    # D = FRAME
        self.__asmCmd('@R13')   
        self.__asmCmd('M=D-1')  # FRAME = FRAME-1
        self.__asmCmd('A=M')
        self.__asmCmd('D=M')    # D=&FRAME
        self.__asmCmd('@THAT')  # THAT
        self.__asmCmd('M=D')

        self.__asmCmd('@R13')   
        self.__asmCmd('D=M')
        self.__asmCmd('@R13')   
        self.__asmCmd('M=D-1')
        self.__asmCmd('A=M')
        self.__asmCmd('D=M')
        self.__asmCmd('@THIS')  # THIS
        self.__asmCmd('M=D')

        self.__asmCmd('@R13')
        self.__asmCmd('D=M')
        self.__asmCmd('@R13')
        self.__asmCmd('M=D-1')
        self.__asmCmd('A=M')
        self.__asmCmd('D=M')
        self.__asmCmd('@ARG')  # ARG
        self.__asmCmd('M=D')

        self.__asmCmd('@R13')
        self.__asmCmd('D=M')
        self.__asmCmd('@R13')
        self.__asmCmd('M=D-1')
        self.__asmCmd('A=M')
        self.__asmCmd('D=M')
        self.__asmCmd('@LCL')  # LCL
        self.__asmCmd('M=D')
        # 返回调用函数
        self.__asmCmd('@R14')
        self.__asmCmd('A=M')
        self.__asmCmd('0;JMP')

    def writeFunction(self,functionName,numLocals):
        '''vm function'''
        if functionName == 'Sys.init':
            self._hasSysInit = True

        self.__asmComment("vm cmd:funcion {0} {1}".format(functionName,numLocals))
        self.__asmLabel(functionName)
        self._currVMFuncName = functionName
        for i in range(numLocals):
            self.__vmStackPushFromConstant(0) # 分配局部变量

    def close(self):
        if not self._hasSysInit:
            del(self._asm[self._initBegin:self._initEnd])
            print('警告：未发现Sys.init函数，将不会生成引导程序')

        self.__flush()
        self._file.close()

    # 栈指针应始终指向栈顶元素的下一个，即栈指针应指向写入位置

    def __vmStackPopToD(self):
        '''把栈顶弹出到D寄存器'''
        self.__vmStackDec()
        self.__asmInlineComment('[begin]:pop stack to D',-2)
        self.__asmCmd('A=M')
        self.__asmCmd('D=M')
        self.__asmInlineComment('[end]:pop stack to D')

    def __vmStackPushFromD(self):
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
        self.__asmCmd('@'+self.__asmGetAutoLabel('IF_TRUE',5))# IF_TRUE在此后第5条指令
        self.__asmCmd('D;{0}'.format(jmpCode))
        self.__asmCmd('D=0')# False
        self.__asmCmd('@'+self.__asmGetAutoLabel('IF_END',3))# IF_END在此后第3条指令
        self.__asmCmd('0;JMP')
        self.__asmAutoLabel('IF_TRUE')
        self.__asmCmd('D=-1')# True
        self.__asmAutoLabel('IF_END')

    def __vmStackPushFromConstant(self,val):
        '''将常量压入栈中'''
        self.__asmCmd('@{0}'.format(val))
        self.__asmCmd('D=A')
        self.__vmStackPushFromD()

    __vmSegmentReg = {
        'local':'LCL',
        'argument':'ARG',
        'this':'THIS',
        'that':'THAT'
    }

    def __vmStackPushFromSegment(self,segment,index):
        '''从以下内存段取数据压栈:local,argument,this,that'''
        reg = CodeWriter.__vmSegmentReg[segment]
        self.__asmCmd('@'+reg)
        self.__asmCmd('D=M')
        self.__asmCmd('@'+str(index))
        self.__asmCmd('A=D+A')
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()

    def __vmStackPopToSegment(self,segment,index):
        '''把数据弹栈到以下内存段:local,argument,this,that'''
        # 弹栈需要：A寄存器指向栈顶元素地址
        # 写入需要：A寄存器指向写入地址,D寄存器放数据
        # 计算地址需要：A寄存器放基地址，D寄存器放偏移
        # 因此两步操作都使用了AD寄存器，无法直接弹栈到D再写到M
        reg = CodeWriter.__vmSegmentReg[segment]
        self.__asmCmd('@'+reg)
        self.__asmCmd('D=M')
        self.__asmCmd('@'+str(index))
        self.__asmCmd('D=D+A') # D指向写入地址
        self.__asmCmd('@R13')
        self.__asmCmd('M=D') # 先把写入地址放到R13寄存器中

        self.__vmStackPopToD()
        self.__asmCmd('@R13')
        self.__asmCmd('A=M') # A指向写入地址
        self.__asmCmd('M=D')

    def __vmStackPushFromPointer(self,segment,index):
        '''从以下内存段取数据压栈:pointer,temp'''
        addr = ''
        if segment == 'pointer':
            addr = 'R'+str(3+index)
        elif segment == 'temp':
            addr = 'R'+str(5+index)
        else:
            raise Exception('未识别的vm内存段:{1}'.format(segment))
        
        self.__asmCmd('@'+addr)
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()

    def __vmStackPopToPointer(self,segment,index):
        '''把数据弹栈到以下内存段:pointer,temp'''
        addr = ''
        if segment == 'pointer':
            addr = 'R'+str(3+index)
        elif segment == 'temp':
            addr = 'R'+str(5+index)
        else:
            raise Exception('未识别的vm内存段:{1}'.format(segment))

        self.__vmStackPopToD()
        self.__asmCmd('@'+addr)
        self.__asmCmd('M=D')

    def __vmStackPushFromStatic(self,index):
        '''从以下内存段取数据压栈:static'''
        addr = self._currVMFileName+'.'+str(index)
        self.__asmCmd('@'+addr)
        self.__asmCmd('D=M')
        self.__vmStackPushFromD()

    def __vmStackPopToStatic(self,index):
        '''把数据弹栈到以下内存段:static'''
        addr = self._currVMFileName+'.'+str(index)
        self.__vmStackPopToD()
        self.__asmCmd('@'+addr)
        self.__asmCmd('M=D')

    def __asmCmd(self,cmd,comment=None):
        '''写入一条指令，可以传入comment字段，将在当前行添加注释'''
        self._asm.append(cmd)
        self._currAsmCmdCnt += 1
        if comment!=None:
            self.__asmInlineComment(comment)

    class AutoLabelRefStub:
        def __init__(self,writer,arrayIdx,label):
            '''为了方便计算自动标签中添加的行号，这个类用来对_asm某个自动标签引用的延迟确定'''
            self._writer = writer
            self._arrayIdx = arrayIdx
            self._label = label

        def Complete(self):
            '''完成对自动标签引用的确定'''
            self._writer._asm[self._arrayIdx] = '@LABEL_AUTO_{0}_{1}'.format(self._label, self._writer._currAsmCmdCnt)

    def __asmAutoLabel(self,name):
        '''写入一条自动标签，自动标签后面带有指令行数，以避免重复'''
        self._asm.append('(LABEL_AUTO_{0}_{1})'.format(name,self._currAsmCmdCnt))

    def __asmAutoLabelRefStub(self,name):
        '''引用一条自动标签，返回AutoLabelStub，需要在后续声明自动标签处调用Complete方法以完成'''
        self.__asmCmd('stub:@LABEL_AUTO_{0} (将在stub Complete时完成此行的替换)'.format(name))
        stub = CodeWriter.AutoLabelRefStub(self,len(self._asm)-1,name)
        return stub

    def __asmGetAutoLabel(self,name,offset):
        '''获取自动标签，offset用来指定相对当前指令的偏移'''
        return 'LABEL_AUTO_{0}_{1}'.format(name,self._currAsmCmdCnt+offset)

    def __asmLabel(self,label):
        '''写入一条标签'''
        self._asm.append('({0})'.format(label))

    def __asmScopeLabel(self,label):
        '''写入一条标签，标签会考虑当前所处的function'''
        fullLabel = self.__asmGetScopeLabel(label)
        self._asm.append('({0})'.format(fullLabel))
    
    def __asmGetScopeLabel(self,label):
        '''生成一条标签，标签会考虑当前所处的function'''
        fullLabel = self._currVMFuncName + "$" + label
        return fullLabel

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
        outputPath = os.path.join(inputPath,Path(inputPath).name+'.asm')
        for root,dirs,files in os.walk(inputPath):
            for f in files:
                if f.endswith('.vm'):
                    fileList.append(os.path.join(root,f))

    print('输出文件为:{0}'.format(outputPath))
    writer = CodeWriter(outputPath)
    writer.writeInit()
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
            elif t == Parser.C_LABEL:
                writer.writeLabel(parser.arg1())
            elif t == Parser.C_GOTO:
                writer.writeGoto(parser.arg1())
            elif t == Parser.C_IF:
                writer.writeIf(parser.arg1())
            elif t == Parser.C_CALL:
                writer.writeCall(parser.arg1(),parser.arg2())
            elif t == Parser.C_RETURN:
                writer.writeReturn()
            elif t == Parser.C_FUNCTION:
                writer.writeFunction(parser.arg1(),parser.arg2())

    writer.close()

main()