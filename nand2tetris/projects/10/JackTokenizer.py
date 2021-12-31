# coding=utf-8

import sys
import os
from pathlib import Path
from enum import Enum

class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

class Keyword(Enum):
    CLASS = "class"
    METHOD = "method"
    INT = "int"
    FUNCTION = "function"
    BOOLEAN = "bool"
    CONSTRUCTOR = "constructor"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"

class JackTokenizer:

    def __init__(self,filePath:str) -> None:
        self._path = filePath
        self._file = open(filePath,mode='r',encoding='utf-8')
        self._file.seek(0,os.SEEK_END)
        self._fileLen = self._file.tell()
        self._file.seek(0,os.SEEK_SET)
        self._readCnt = 0

    def hasMoreTokens(self) -> bool:
        if self._file == None:
            return False
        
        self.__skipCommentAndWhite()
        s = self._file.tell() >= self._fileLen
        if s:
            self.__close()
        
        return s


    def advance(self) -> None:
        pass

    def tokenType(self) -> TokenType:
        pass

    def keyword(self) -> Keyword:
        pass

    def symbol(self) -> str:
        pass

    def identifier(self) -> str:
        pass

    def intVal(self) -> int:
        pass

    def stringVal(self) -> str:
        pass
    
    class SkipState(Enum):
        none = 0
        commentTryBegin = 1
        commentTryEnd = 2
        comment = 3
        lineComment = 4

    def __skipCommentAndWhite(self) -> None:
        '''跳过空格符、换行符、注释'''
        state = self.SkipState.none
        skipChar = [' ','\n','\r','\t']
        c0 = '*'
        c1 = '/'

        while True:
            pos = self._file.tell()# 记录操作前位置
            if state == self.SkipState.none:
                c = self._file.read(1)
                if c == '':
                    return
                
                if c in skipChar:# 空白字符
                    pass
                elif c == c1:# 尝试开始注释
                    state = self.SkipState.commentTryBegin
                else:
                    # 是有效字符，结束跳过
                    self._file.seek(pos,os.SEEK_SET)
                    return

            elif state == self.SkipState.commentTryBegin:
                c = self._file.read(1)
                if c == '':
                    self.__close()
                    raise self.__error('未形成有效的注释开始:/' + c)

                if c == c0:# /**/型注释
                    state = self.SkipState.comment
                elif c == c1:# //型整行注释
                    state = self.SkipState.lineComment
                else:
                    self.__close()
                    raise self.__error('未形成有效的注释开始:/' + c)
                
            elif state == self.SkipState.comment:
                c = self._file.read(1)
                if c == '':
                    self.__close()
                    raise self.__error('在多行注释中遇到文件结尾')

                if c == c0:
                    state = self.SkipState.commentTryEnd

            elif state == self.SkipState.commentTryEnd:
                c = self._file.read(1)
                if c == '':
                    self.__close()
                    raise self.__error('在多行注释中遇到文件结尾')

                if c == c0:
                    state = self.SkipState.commentTryEnd
                if c == c1:
                    state = self.SkipState.none
                else:
                    state = self.SkipState.comment # *符号后不是*或/，回到/**/注释状态

            elif state == self.SkipState.lineComment:
                line = self._file.readline()
                state = self.SkipState.none

            else:
                self.__close()
                raise self.__error('未识别的跳过状态:' + str(state))

    def __error(self,msg:str) -> Exception:
        return Exception("{msg} 在{self._path}的第{self._readCnt}个字符")

    def __close(self):
        if self._file!=None:
            self._file.close()
            self._file = None

            

