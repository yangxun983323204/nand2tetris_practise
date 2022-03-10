# coding=utf-8

from subprocess import call
import sys
import os
from typing import Any, Dict, List, Tuple

from cv2 import RETR_CCOMP
from JackTokenizer import *

class CompilationToken:
    '''每个字元的编译所需信息'''
    def __init__(self, type:TokenType, keyword:Keyword, symbol:str, identifier:str, intVal:int, stringVal:str) -> None:
        self.tokenType = type
        self.keyword = keyword
        self.symbol = symbol
        self.identifier = identifier
        self.intVal = intVal
        self.stringVal = stringVal
        pass

#region 语法树节点定义

class SyntaxNode:
    def __init__(self) -> None:
        self.Parent:SyntaxNode = None

class SyntaxClassNode(SyntaxNode):
    '''类'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "class"
        self.Name = ''
        self.VarDecList:List[SyntaxClassVarDecNode] = []
        self.SubroutineDecList:List[SyntaxSubroutineDecNode] = []

class SyntaxClassVarDecNode(SyntaxNode):
    '''类变量声明'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "classVarDec"
        self.Permission:str = '' # static|field
        self.TypeType:str = ''
        self.Type:str = ''
        self.VarList:List[str] = []

class SyntaxSubroutineDecNode(SyntaxNode):
    '''方法声明'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "subroutineDec"
        self.Permission:str = '' # constructor|function|method
        self.ReturnTypeType:str = ''
        self.ReturnType:str = ''
        self.Name:str = ''
        self.ParameterList:SyntaxParameterListNode = None
        self.Body:SyntaxSubroutineBodyNode = None

class SyntaxParameterListNode(SyntaxNode):
    '''参数列表'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "parameterList"
        self.ParameterList:List[Tuple[str,str,str]] = []

class SyntaxSubroutineBodyNode(SyntaxNode):
    '''方法体'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "subroutineBody"
        self.LocalVarDecList:List[SyntaxVarDecNode] = []
        self.Statements:SyntaxStatementsNode = None

class SyntaxVarDecNode(SyntaxNode):
    '''变量声明'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "varDec"
        self.TypeType:str = ''
        self.Type:str = ''
        self.VarList:List[str] = []

class SyntaxStatementsNode(SyntaxNode):
    '''一系列语句'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "statements"
        self.StatementList:List[SyntaxNode] = []

class SyntaxDoNode(SyntaxNode):
    '''do语句'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "doStatement"
        # SubroutineCall
        self.HasTarget:bool = False
        self.TargetName:str = ''
        self.FuncName:str = ''
        self.ExpressionList:SyntaxExpressionListNode = None

class SyntaxLetNode(SyntaxNode):
    '''let语句'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "letStatement"
        self.HasIndex:bool = False
        self.VarName:str = ''
        self.Index:SyntaxExpressionNode = None
        self.Expression:SyntaxExpressionNode = None

class SyntaxWhileNode(SyntaxNode):
    '''while语句'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "whileStatement"
        self.Expression:SyntaxExpressionNode = None
        self.Statements:SyntaxStatementsNode = None

class SyntaxReturnNode(SyntaxNode):
    '''return语句'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "returnStatement"
        self.Expression:SyntaxExpressionNode = None

class SyntaxIfNode(SyntaxNode):
    '''if语句'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "ifStatement"
        self.Expression:SyntaxExpressionNode = None
        self.Statements:SyntaxStatementsNode = None
        self.ElseStatements:SyntaxStatementsNode = None

class SyntaxExpressionNode(SyntaxNode):
    '''表达式'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "expression"
        self.HasOperate:bool = False
        self.Term:SyntaxTermNode = None
        self.OpTermList:List[Tuple[str,SyntaxTermNode]] = []

class SyntaxTermNode(SyntaxNode):
    '''term，这个里面包含分支比较多，要通过Type字来区别是哪种term'''

    class TermType(Enum):
        IntConst = 0,
        StrConst = 1,
        KeywordConst = 2,
        Var = 3,
        VarIdx = 4,
        Call = 5,
        Exp = 6,
        UnaryOpTerm = 7

    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "term"
        self.Type:SyntaxTermNode.TermType = None
        self.IntVal:int = 0
        self.StrVal:str = '' # 既可以存stringConst，也可以存identifier
        self.KeyWordVal:Keyword = None
        self.ExpVal:SyntaxExpressionNode = None
        # SubroutineCall
        self.HasTarget:bool = False
        self.TargetName:str = ''
        self.FuncName:str = ''
        self.ExpressionList:SyntaxExpressionListNode = None

        self.Term:SyntaxTermNode = None

class SyntaxExpressionListNode(SyntaxNode):
    '''逗号分隔的表达式'''
    def __init__(self) -> None:
        super().__init__()
        self.NodeName = "expressionList"
        self.ExpressionList:List[SyntaxExpressionNode] = []

#endregion

class CompilationEngine:

    def __init__(self,inFilePath:str,outFilePath:str) -> None:
        self._inPath = inFilePath
        self._outPath = outFilePath
        self._tokenizer = JackTokenizer(inFilePath)

    def CompileClass(self) -> SyntaxClassNode:
        node = SyntaxClassNode()
        className = ''

        # 检查第一个字元是否是class
        n = self.__GetNextToken()
        self.__checkKeyword(n,Keyword.CLASS)
        # 检查第二个字元是否是类名
        n = self.__GetNextToken()
        self.__checkIdentifer(n)
        className = n.identifier

        node.Name = className
        # 检查第三个字元是否是{
        n = self.__GetNextToken()
        self.__checkSymbol(n,'{')
        n = self.__PeekNextToken()
        while n.tokenType == TokenType.KEYWORD and (n.keyword == Keyword.STATIC or n.keyword == Keyword.FIELD):
            varDec = self.CompileClassVarDec()
            varDec.Parent = node
            node.VarDecList.append(varDec)
            n = self.__PeekNextToken()
        
        while n.tokenType == TokenType.KEYWORD and (n.keyword == Keyword.CONSTRUCTOR or n.keyword == Keyword.FUNCTION or n.keyword == Keyword.METHOD):
            subroutine = self.CompileSubroutine()
            subroutine.Parent = node
            node.SubroutineDecList.append(subroutine)
            n = self.__PeekNextToken()

        # 检查最后一个字元是否是}
        n = self.__GetNextToken()
        self.__checkSymbol(n,'}')
        return node

    def CompileClassVarDec(self) -> SyntaxClassVarDecNode:
        node = SyntaxClassVarDecNode()

        n = self.__GetNextToken()
        varPermission = n.keyword
        n = self.__GetNextToken()
        self.__assert(self.__canBeVarType(n),"变量类型只能为关键字int,char,boolean或标识符")
        varTypeType,varType = self.__getType(n)
        n = self.__GetNextToken()
        self.__checkIdentifer(n)
        varName:str = n.identifier

        node.Permission = varPermission.value
        node.TypeType = varTypeType
        node.Type = varType
        node.VarList.append(varName)

        n = self.__GetNextToken()
        while self.__isSymbol(n, ','):
            n = self.__GetNextToken()
            varName:str = n.identifier
            n = self.__GetNextToken()

            node.VarList.append(varName)
        
        self.__checkSymbol(n,';')
        return node

    def CompileSubroutine(self) -> SyntaxSubroutineDecNode:
        node = SyntaxSubroutineDecNode()
        body = SyntaxSubroutineBodyNode()
        body.Parent = node
        node.Body = body

        n = self.__GetNextToken()
        funcType = n.keyword
        n = self.__GetNextToken()
        self.__assert(self.__canBeRetType(n),"返回类型只能为关键字void,int,char,boolean或标识符")
        retTypeType,retType = self.__getType(n)
        n = self.__GetNextToken()
        self.__checkIdentifer(n)
        funcName:str = n.identifier
        n = self.__GetNextToken()
        self.__checkSymbol(n, '(')

        node.Permission = funcType.value
        node.ReturnTypeType = retTypeType
        node.ReturnType = retType
        node.Name = funcName

        parameters = self.CompileParameterList()
        parameters.Parent = node
        node.ParameterList = parameters

        n = self.__GetNextToken()
        self.__checkSymbol(n, ')')
        n = self.__GetNextToken()
        self.__checkSymbol(n, '{')
        n = self.__PeekNextToken()
        while n.tokenType == TokenType.KEYWORD and n.keyword == Keyword.VAR:
            varDec = self.CompileVarDec()
            varDec.Parent = body
            body.LocalVarDecList.append(varDec)

            n = self.__PeekNextToken()
        
        statements = self.CompileStatements()
        statements.Parent = body
        body.Statements = statements

        n = self.__GetNextToken()
        self.__checkSymbol(n, '}')
        return node

    def CompileParameterList(self) -> SyntaxParameterListNode:
        node = SyntaxParameterListNode()

        n = self.__PeekNextToken()
        if (self.__canBeVarType(n)):
            # 有参数
            n = self.__GetNextToken()
            varTypeType,varType = self.__getType(n)
            n = self.__GetNextToken()
            self.__checkIdentifer(n)
            varName = n.identifier

            node.ParameterList.append({varTypeType, varType, varName})

            # 检测是否多个参数
            n = self.__PeekNextToken()
            while self.__isSymbol(n, ','):
                n = self.__GetNextToken()
                varTypeType,varType = self.__getType(n)
                n = self.__GetNextToken()
                self.__checkIdentifer(n)
                varName = n.identifier

                node.ParameterList.append({varTypeType, varType, varName})
        else:
            pass
            
        return node

    def CompileVarDec(self) -> SyntaxVarDecNode:
        node = SyntaxVarDecNode()

        n = self.__GetNextToken()
        self.__checkKeyword(n,Keyword.VAR)
        n = self.__GetNextToken()
        self.__assert(self.__canBeVarType(n),"变量类型只能为关键字int,char,boolean或标识符")
        varTypeType, varType = self.__getType(n)
        n = self.__GetNextToken()
        self.__checkIdentifer(n)
        varName = n.identifier

        node.TypeType = varTypeType
        node.Type = varType
        node.VarList.append(varName)
        # 检查是否同时声明多个变量
        n = self.__GetNextToken()
        while self.__isSymbol(n, ','):
            n = self.__GetNextToken()
            self.__checkIdentifer(n)
            varName = n.identifier
            n = self.__GetNextToken()

            node.VarList.append(varName)
        
        self.__checkSymbol(n,';')
        return node

    def CompileStatements(self) -> SyntaxStatementsNode:
        '''let,if,while,do,return中一种语句，或者空语句'''
        node = SyntaxStatementsNode()

        keys = [Keyword.LET,Keyword.IF,Keyword.WHILE,Keyword.DO,Keyword.RETURN]
        n = self.__PeekNextToken()
        while n.tokenType == TokenType.KEYWORD and n.keyword in keys:
            if n.keyword == Keyword.LET:
                letNode = self.CompileLet()
                letNode.Parent = node
                node.StatementList.append(letNode)
            elif n.keyword == Keyword.IF:
                ifNode = self.CompileIf()
                ifNode.Parent = node
                node.StatementList.append(ifNode)
            elif n.keyword == Keyword.WHILE:
                whileNode = self.CompileWhile()
                whileNode.Parent = node
                node.StatementList.append(whileNode)
            elif n.keyword == Keyword.DO:
                doNode = self.CompileDo()
                doNode.Parent = node
                node.StatementList.append(doNode)
            elif n.keyword == Keyword.RETURN:
                retNode = self.CompileReturn()
                retNode.Parent = node
                node.StatementList.append(retNode)

        return node

    def CompileDo(self) -> SyntaxDoNode:
        node = SyntaxDoNode()

        isTargetCall:bool=False
        target:str=None
        callName:str

        n = self.__GetNextToken()# do
        callInfo = self.__CompileSubroutineCall()

        node.HasTarget = callInfo.isTargetCall
        node.TargetName = callInfo.TargetName
        node.FuncName = callInfo.FuncName

        callInfo.ExpList = node
        node.ExpressionList = callInfo.ExpList

        n = self.__GetNextToken()
        self.__checkSymbol(n,';')
        return node

    def CompileLet(self) -> SyntaxLetNode:
        node = SyntaxLetNode()

        varName:str
        hasIdx:bool=False

        n = self.__GetNextToken() # let
        n = self.__GetNextToken()
        self.__checkIdentifer(n)
        varName = n.identifier

        node.VarName = varName
        # 判断是否有下标
        n = self.__PeekNextToken()
        if self.__isSymbol(n,'['):
            hasIdx = True
            n = self.__GetNextToken() # [

            node.HasIndex = hasIdx

            exp = self.CompileExpression()  # 下标表达式
            exp.Parent = node
            node.Index = exp

            n = self.__GetNextToken() # ]
            self.__checkSymbol(n,']')

        n = self.__GetNextToken()
        self.__checkSymbol(n,'=')

        exp = self.CompileExpression()
        exp.Parent = node
        node.Expression = exp
        
        n = self.__GetNextToken()
        self.__checkSymbol(n,';')
        return node

    def CompileWhile(self) -> SyntaxWhileNode:
        node = SyntaxWhileNode()

        n = self.__GetNextToken()
        n = self.__GetNextToken()
        self.__checkSymbol(n,'(')

        exp = self.CompileExpression()
        exp.Parent = node
        node.Expression = exp

        n = self.__GetNextToken()
        self.__checkSymbol(n,')')
        n = self.__GetNextToken()
        self.__checkSymbol(n,'{')

        statements = self.CompileStatements()
        statements.Parent = node
        node.Statements = statements

        n = self.__GetNextToken()
        self.__checkSymbol(n,'}')
        return node

    def CompileReturn(self) -> SyntaxReturnNode:
        node = SyntaxReturnNode()

        n = self.__GetNextToken()
        n = self.__PeekNextToken()
        if self.__isSymbol(n,';'):  # 无返回值
            n = self.__GetNextToken()
        else:
            exp = self.CompileExpression()
            exp.Parent = node
            node.Expression = exp
        
        return node

    def CompileIf(self) -> SyntaxIfNode:
        node = SyntaxIfNode()

        n = self.__GetNextToken()
        self.__checkKeyword(n,Keyword.IF)
        n = self.__GetNextToken()
        self.__checkSymbol(n,'(')
        exp = self.CompileExpression()
        exp.Parent = node
        node.Expression = exp
        n = self.__GetNextToken()
        self.__checkSymbol(n,')')
        n = self.__GetNextToken()
        self.__checkSymbol(n,'{')
        statements = self.CompileStatements()
        statements.Parent = node
        node.Statements = statements
        n = self.__GetNextToken()
        self.__checkSymbol(n,'}')
        # 判断是否有else部分
        n = self.__PeekNextToken()
        if self.__isKeyword(n,Keyword.ELSE):
            n = self.__GetNextToken()
            n = self.__GetNextToken()
            self.__checkSymbol(n,'{')
            statements = self.CompileStatements()
            statements.Parent = node
            node.ElseStatements = statements
            n = self.__GetNextToken()
            self.__checkSymbol(n,'}')
        
        return node

    def CompileExpression(self) -> SyntaxExpressionNode:
        node = SyntaxExpressionNode()
        op = ['+','-','*','/','&','|','<','>','=']

        term = self.CompileTerm()
        term.Parent = node
        node.Term = term

        n = self.__PeekNextToken()
        while n.tokenType == TokenType.SYMBOL and n.symbol in op:
            opCode = n.symbol
            n = self.__GetNextToken()
            term = self.CompileTerm()
            term.Parent = node
            node.HasOperate = True
            node.OpTermList.append({opCode,term})

            n = self.__PeekNextToken()

        return node

    def CompileTerm(self) -> SyntaxTermNode:
        node = SyntaxTermNode()
        unaryOp = ['-','~']
        keywordConst = [Keyword.TRUE, Keyword.FALSE, Keyword.NULL, Keyword.THIS]

        p0 = self.__PeekNextToken()
        p1 = self.__PeekToken(2)
        if p0.tokenType == TokenType.INT_CONST: # integerConstant
            n = self.__GetNextToken()
            node.Type = SyntaxTermNode.TermType.IntConst
            node.IntVal = n.intVal
        elif p0.tokenType == TokenType.STRING_CONST: # stringConstant
            n = self.__GetNextToken()
            node.Type = SyntaxTermNode.TermType.StrConst
            node.IntVal = n.stringVal
        elif p0.tokenType == TokenType.KEYWORD and p0.keyword in keywordConst: # keywordConstant
            n = self.__GetNextToken()
            node.Type = SyntaxTermNode.TermType.KeywordConst
            node.KeyWordVal = n.keyword
        elif p0.tokenType == TokenType.IDENTIFIER and self.__isSymbol(p1,'['): # varName[expression]
            n = self.__GetNextToken()
            node.Type = SyntaxTermNode.TermType.VarIdx
            node.StrVal = n.identifier
            n = self.__GetNextToken()
            self.__checkSymbol(n,'[')
            idx = self.CompileExpression()
            idx.Parent = node
            node.ExpVal = idx
            n = self.__GetNextToken()
            self.__checkSymbol(n,']')
        elif p0.tokenType == TokenType.IDENTIFIER and self.__isSymbol(p1,'('): # subroutineCall
            callInfo = self.__CompileSubroutineCall()
            node.Type = SyntaxTermNode.TermType.Call
            node.HasTarget = callInfo.isTargetCall
            node.TargetName = callInfo.TargetName
            node.FuncName = callInfo.FuncName
            node.ExpressionList = callInfo.ExpList
        elif p0.tokenType == TokenType.IDENTIFIER: # varName
            n = self.__GetNextToken()
            self.__checkIdentifer(n)
            node.StrVal = n.identifier
        elif self.__isSymbol(p0,'('): # (expression)
            n = self.__GetNextToken()
            self.__checkSymbol(n,'(')
            exp = self.CompileExpression()
            exp.Parent = node
            node.ExpVal = exp
            n = self.__GetNextToken()
            self.__checkSymbol(n,')')
        elif p0.tokenType == TokenType.SYMBOL and p0.symbol in unaryOp: # unaryOp term
            n = self.__GetNextToken()
            node.StrVal = n.symbol
            term = self.CompileTerm()
            term.Parent = node
            node.Term = term
        else:
            raise self.__error("未识别的term:" + str(p0))

        return node

    def CompileExpressionList(self) -> SyntaxExpressionListNode:
        # 注意一个事实：表达式列表只出现在子过程调用的参数列表中
        # 因此，空列表可通过看当前字符是否是')'来判断，是的话就是空表达式列表
        node = SyntaxExpressionListNode()

        n = self.__GetNextToken()
        if n.tokenType == TokenType.SYMBOL and n.symbol == ')': # 空表达式列表
            pass
        else:
            # todo
            pass

        return node
    
    class SubroutineCallInfo:
        '''SubroutineCall分析'''
        def __init__(self) -> None:
            '''SubroutineCall分析'''
            self.isTargetCall:bool = False
            self.TargetName:str = None
            self.FuncName:str = None
            self.ExpList:SyntaxExpressionListNode = None

    def __CompileSubroutineCall(self) -> SubroutineCallInfo:
        '''因为do语句和term语句都有subroutineCall语句，因此把解析部分提取出来公用'''
        info = CompilationEngine.SubroutineCallInfo()

        n = self.__GetNextToken()# target或callName
        self.__checkIdentifer(n)
        # 判断是同内部函数调用还是类函数或对象函数调用
        t = self.__PeekNextToken()
        if self.__isSymbol(n,'.'): # 是类函数或对象函数调用
            info.isTargetCall = True
            info.TargetName = n.identifier
            n = self.__GetNextToken() # .号
            n = self.__GetNextToken() # callName
            self.__checkIdentifer(n)

        info.FuncName = n.identifier
        n = self.__GetNextToken()
        self.__checkSymbol(n,'(')
        info.ExpList = self.CompileExpressionList()
        n = self.__GetNextToken()
        self.__checkSymbol(n,')')

        return info

    def __GetNextToken(self) -> CompilationToken:
        pass

    def __PeekNextToken(self) -> CompilationToken:
        return self.__PeekToken(1)
    
    def __PeekToken(self,idx:int) -> CompilationToken:
        '''向前查看第idx个'''
        pass

    def __OutputXml(self) -> None:
        '''把语法树输出为xml'''
        pass

#region 辅助方法
    def __error(self,msg:str) -> Exception:
        return Exception("{0} 在{1}的{2}附近".format(msg,self._inPath,self._readPos))

    def __assert(self,condition:bool,msg:str) ->None:
        if not condition:
            raise self.__error(msg)

    def __isKeyword(self,token:CompilationToken,wantKey:Keyword) -> bool:
        '''token是否是指定的关键字'''
        return token.tokenType == TokenType.KEYWORD and token.keyword == wantKey

    def __isSymbol(self,token:CompilationToken,wantSymbol:str) -> bool:
        '''token是否是指定的符号'''
        return token.tokenType == TokenType.SYMBOL and token.symbol == wantSymbol

    def __checkKeyword(self,token:CompilationToken,wantKey:Keyword) -> bool:
        if not self.__isKeyword(token,wantKey):
            raise self.__error("期望关键字:"+wantKey.value)

    def __checkSymbol(self,token:CompilationToken,wantSymbol:str) -> bool:
        if self.__isSymbol(token,wantSymbol):
            raise self.__error("期望符号:"+wantSymbol)

    def __checkIdentifer(self,token:CompilationToken) -> bool:
        if token.tokenType != TokenType.IDENTIFIER:
            raise self.__error("期望标识符")

    def __checkIntConst(self,token:CompilationToken) -> bool:
        if token.tokenType != TokenType.INT_CONST:
            raise self.__error("期望int常量")

    def __checkStrConst(self,token:CompilationToken) -> bool:
        if token.tokenType != TokenType.STRING_CONST:
            raise self.__error("期望string常量")
    
    def __canBeVarType(self,token:CompilationToken) -> bool:
        '''token能否作为返回类型'''
        isBuiltinType:bool = token.tokenType == TokenType.KEYWORD and token.keyword in [Keyword.INT,Keyword.CHAR,Keyword.BOOLEAN]
        isCustomType:bool = token.tokenType  == TokenType.IDENTIFIER
        return isBuiltinType or isCustomType

    def __canBeRetType(self,token:CompilationToken) -> bool:
        '''token能否作为变量类型'''
        isBuiltinType:bool = token.tokenType == TokenType.KEYWORD and token.keyword in [Keyword.VOID,Keyword.INT,Keyword.CHAR,Keyword.BOOLEAN]
        isCustomType:bool = token.tokenType  == TokenType.IDENTIFIER
        return isBuiltinType or isCustomType

    def __getType(self,token:CompilationToken) ->Tuple[str,str]:
        '''从token读取类型的类型和类型'''
        if token.tokenType == TokenType.KEYWORD:
            retTypeType = token.tokenType.value
            retType = token.keyword.value
        elif token.tokenType == TokenType.IDENTIFIER:
            retTypeType = token.tokenType.value
            retType = token.identifier
        else:
            raise self.__error("类型必须为关键字或标识符")

        return retTypeType, retType
#endregion