# coding=utf-8

import sys
import os
from JackTokenizer import *

class CompilationToken:
    def __init__(self, type:TokenType, keyword:Keyword, symbol:str, identifier:str, intVal:int, stringVal:str) -> None:
        self.tokenType = type
        self.keyword = keyword
        self.symbol = symbol
        self.identifier = identifier
        self.intVal = intVal
        self.stringVal = stringVal
        pass

class CompilationEngine:

    def __init__(self,inFilePath:str,outFilePath:str) -> None:
        self._inPath = inFilePath
        self._outPath = outFilePath
        self._tokenizer = JackTokenizer(inFilePath)

    def CompileClass(self) -> None:
        className = ''
        # 检查第一个字元是否是class
        n = self.__GetNextToken()
        self.__checkKeyword(n,Keyword.CLASS)
        # 检查第二个字元是否是类名
        n = self.__GetNextToken()
        self.__checkIdentifer(n)
        className = n.identifier
        # 检查第三个字元是否是{
        n = self.__GetNextToken()
        self.__checkSymbol(n,'{')
        # 编译
        #
        n = self.__PeekNextToken()
        while n.tokenType == TokenType.KEYWORD and (n.keyword == Keyword.STATIC or n.keyword == Keyword.FIELD):
            self.CompileClassVarDec()
            n = self.__PeekNextToken()
        
        while n.tokenType == TokenType.KEYWORD and (n.keyword == Keyword.CONSTRUCTOR or n.keyword == Keyword.FUNCTION or n.keyword == Keyword.METHOD):
            self.CompileSubroutine()
            n = self.__PeekNextToken()

        # 检查最后一个字元是否是}
        n = self.__GetNextToken()
        self.__checkSymbol(n,'}')


    def CompileClassVarDec(self) -> None:
        pass

    def CompileSubroutine(self) -> None:
        pass

    def CompileParameterList(self) -> None:
        pass

    def CompileVarDec(self) -> None:
        pass

    def CompileStatements(self) -> None:
        pass

    def CompileDo(self) -> None:
        pass

    def CompileLet(self) -> None:
        pass

    def CompileWhile(self) -> None:
        pass

    def CompileReturn(self) -> None:
        pass

    def ComileIf(self) -> None:
        pass

    def CompileExpression(self) -> None:
        pass

    def CompileTerm(self) -> None:
        pass

    def CompileExpressionList(self) -> None:
        pass

    def __GetNextToken(self) -> CompilationToken:
        pass

    def __PeekNextToken(self) -> CompilationToken:
        pass

    def __error(self,msg:str) -> Exception:
        return Exception("{0} 在{1}的{2}附近".format(msg,self._inPath,self._readPos))

    def __checkKeyword(self,token:CompilationToken,wantKey:Keyword) -> bool:
        if token.tokenType != TokenType.KEYWORD:
            raise self.__error("期望关键字:"+wantKey.value)
        elif token.keyword != wantKey:
            raise self.__error("期望关键字:"+wantKey.value)

    def __checkSymbol(self,token:CompilationToken,wantSymbol:str) -> bool:
        if token.tokenType != TokenType.SYMBOL:
            raise self.__error("期望关键字:"+wantSymbol)
        elif token.symbol != wantSymbol:
            raise self.__error("期望关键字:"+wantSymbol)

    def __checkIdentifer(self,token:CompilationToken) -> bool:
        if token.tokenType != TokenType.IDENTIFIER:
            raise self.__error("期望标识符")

    def __checkIntConst(self,token:CompilationToken) -> bool:
        if token.tokenType != TokenType.INT_CONST:
            raise self.__error("期望int常量")

    def __checkStrConst(self,token:CompilationToken) -> bool:
        if token.tokenType != TokenType.STRING_CONST:
            raise self.__error("期望string常量")