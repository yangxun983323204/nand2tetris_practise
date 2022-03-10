# coding=utf-8

import re
import sys
import os
from pathlib import Path
from enum import Enum
import traceback

class TokenType(Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"

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

    __SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    __KEYWORDS = []
    __SKIPCHAR = [' ','\n','\r','\t']
    for e in Keyword:
        __KEYWORDS.append(str(e.value))

    def __init__(self,filePath:str) -> None:
        self._path = filePath
        with open(filePath,mode='r',encoding='utf-8') as f:
            # file.tell()在windows下unix换行符时存在bug，可能会返回异常的数值，因此必须手动记录当前位置了
            # 同时发现file.seek也会有问题，因此只能用string来做了
            self._file = f.read()
            self._fileLen = len(self._file)
            self._readPos = 0

    def hasMoreTokens(self) -> bool:
        if self._file == None:
            return False
        
        self.__skipCommentAndWhite()
        s = self._readPos >= self._fileLen
        if s:
            self.__close()

        return not s


    def advance(self) -> None:
        self._token =  self.__readNextToken()
        # 分析其tokentype
        if self._token in JackTokenizer.__KEYWORDS:
            self._type = TokenType.KEYWORD
        elif self._token in JackTokenizer.__SYMBOLS:
            self._type = TokenType.SYMBOL
        elif self._token.isdigit():
            self._type = TokenType.INT_CONST
        elif re.match('"[^"]*"',self._token):
            self._type = TokenType.STRING_CONST
        elif re.match("[a-zA-Z_][a-zA-Z0-9_]*",self._token):
            self._type = TokenType.IDENTIFIER
        else:
            raise self.__error("未识别的字元:" + self._token)

    def tokenType(self) -> TokenType:
        return self._type

    def keyword(self) -> Keyword:
        if self._type == TokenType.KEYWORD:
            return Keyword(self._token)
        else:
            raise self.__error("当前字元类型不是KEYWORDS而是" + self._type.name)

    def symbol(self) -> str:
        if self._type == TokenType.SYMBOL:
            return self._token
        else:
            raise self.__error("当前字元类型不是SYMBOL而是" + self._type.name)

    def identifier(self) -> str:
        if self._type == TokenType.IDENTIFIER:
            return self._token
        else:
            raise self.__error("当前字元类型不是IDENTIFIER而是" + self._type.name)

    def intVal(self) -> int:
        if self._type == TokenType.INT_CONST:
            return int(self._token)
        else:
            raise self.__error("当前字元类型不是INT_CONST而是" + self._type.name)

    def stringVal(self) -> str:
        if self._type == TokenType.STRING_CONST:
            return self._token
        else:
            raise self.__error("当前字元类型不是STRING_CONST而是" + self._type.name)
    
    class SkipState(Enum):
        none = 0
        commentTryBegin = 1     # 在none状态下读取到字符/
        commentTryEnd = 2       # 在comment状态下读取到字符*
        comment = 3             # 在commentTryBegin状态下读取到字符*
        lineComment = 4         # 在commentTryBegin状态下读取到字符/

    def __skipCommentAndWhite(self) -> bool:
        '''跳过空格符、换行符、注释'''
        state = self.SkipState.none
        c0 = '*'
        c1 = '/'
        prei = self._readPos
        skipStr = ''
        while True:
            c = self.__fileReadOne()
            if state == self.SkipState.none:
                if c == '':
                    break
                
                if c in JackTokenizer.__SKIPCHAR:# 空白字符
                    skipStr += c
                    continue
                elif c == c1:# 尝试开始注释
                    skipStr += c
                    state = self.SkipState.commentTryBegin
                    continue
                else:
                    # 是有效字符，结束跳过
                    skipStr = skipStr[:-1]
                    self.__fileBack(1)
                    break

            elif state == self.SkipState.commentTryBegin:
                if c == '':
                    self.__close()
                    raise self.__error('未形成有效的注释开始:/' + c)

                if c == c0:# /**/型注释
                    skipStr += c
                    state = self.SkipState.comment
                    continue
                elif c == c1:# //型整行注释
                    skipStr += c
                    state = self.SkipState.lineComment
                    continue
                else:
                    # 是除法字符，结束跳过
                    skipStr = skipStr[:-2]
                    self.__fileBack(2)
                    break
                
            elif state == self.SkipState.comment:
                if c == '':
                    self.__close()
                    raise self.__error('在多行注释中遇到文件结尾')

                if c == c0:
                    skipStr += c
                    state = self.SkipState.commentTryEnd
                    continue
                else:
                    skipStr += c
                    continue

            elif state == self.SkipState.commentTryEnd:
                if c == '':
                    self.__close()
                    raise self.__error('在多行注释中遇到文件结尾')

                if c == c0:
                    skipStr += c
                    state = self.SkipState.commentTryEnd
                    continue
                if c == c1:
                    skipStr += c
                    state = self.SkipState.none
                    continue
                else:
                    skipStr += c
                    state = self.SkipState.comment # *符号后不是*或/，回到/**/注释状态
                    continue

            elif state == self.SkipState.lineComment:
                skipStr += c
                if c == '\n':
                    state = self.SkipState.none
                continue

            else:
                self.__close()
                raise self.__error('未识别的跳过状态:' + str(state))
        
        s = self._readPos != prei
        #if s:
            #print("跳过:[{0}]".format(skipStr))
        return s

    def __readNextToken(self) -> str:
        '''读取下一个字元'''
        self.__skipCommentAndWhite()
        self._token = self.__fileReadOne()
        if self._token in JackTokenizer.__SYMBOLS:
            return self._token

        isStr = self._token.startswith('"')
        while True:
            if not isStr:
                s = self.__skipCommentAndWhite()
                if s:
                    break

            c = self.__fileReadOne()
            if c == '':
                break

            if isStr and c == '"':
                self._token += c
                break

            if (not isStr) and (c in JackTokenizer.__SKIPCHAR):
                self.__fileBack(1)
                break

            if c in JackTokenizer.__SYMBOLS:
                # 是分隔字符，结束读取并回退文件流读取位置
                self.__fileBack(1)
                break
            else:
                self._token += c

        return self._token

    def __fileReadOne(self) -> str:
        if self._readPos >= self._fileLen:
            return ''

        s = self._file[self._readPos]
        self._readPos += 1
        return s

    def __fileBack(self,cnt:str) -> None:
        self._readPos -= cnt

    def __error(self,msg:str) -> Exception:
        return Exception("{0} 在{1}的第{2}个字符".format(msg,self._path,self._readPos))

    def __close(self):
        if self._file!=None:
            self._file = None

            

