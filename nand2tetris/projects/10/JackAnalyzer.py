# coding=utf-8

import sys
import os
from pathlib import Path
from JackTokenizer import *
from XmlWriter import *

def main():
    inputPath = sys.argv[1]
    print('输入文件为:{0}'.format(inputPath))
    outputPath = ''
    fileList:list[str] = []
    if inputPath.endswith('.jack'):
        print("输入的是文件")
        fileList.append(inputPath)
        outputPath = inputPath.replace('.jack','.xml')
    else:
        print("输入的是目录")
        outputPath = os.path.join(inputPath,Path(inputPath).name+'.xml')
        for root,dirs,files in os.walk(inputPath):
            for f in files:
                if f.endswith('.jack'):
                    fileList.append(os.path.join(root,f))

    print('输出文件为:{0}'.format(outputPath))

    for file in fileList:
        print("待处理文件:"+file)
        tokenizer = JackTokenizer(file)
        tokenXml = XmlWriter(file.replace(".jack","_work_token.xml"))
        tokenXml.AddNode("tokens",None)
        tokenXml.Forword()
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            t = tokenizer.tokenType()
            if t == TokenType.KEYWORD:
                print("KEYWORD:{0}".format(tokenizer.keyword().value))
                tokenXml.AddNode("keyword",tokenizer.keyword().value)
            elif t == TokenType.SYMBOL:
                print("SYMBOL:{0}".format(tokenizer.symbol()))
                tokenXml.AddNode("symbol",tokenizer.symbol())
            elif t == TokenType.IDENTIFIER:
                print("IDENTIFIER:{0}".format(tokenizer.identifier()))
                tokenXml.AddNode("identifier",tokenizer.identifier())
            elif t == TokenType.INT_CONST:
                print("INT_CONST:{0}".format(tokenizer.intVal()))
                tokenXml.AddNode("integerConstant",str(tokenizer.intVal()))
            elif t == TokenType.STRING_CONST:
                print("STRING_CONST:{0}".format(tokenizer.stringVal()))
                tokenXml.AddNode("stringConstant",tokenizer.stringVal())
            else:
                print("UNKOWN:{0}".format(str(t)))
        
        tokenXml.Save()
        print("结束处理文件:"+file)

main()