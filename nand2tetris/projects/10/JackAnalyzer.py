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
                print("{0}:{1}".format(t.value,tokenizer.keyword().value))
                tokenXml.AddNode(t.value,tokenizer.keyword().value)
            elif t == TokenType.SYMBOL:
                print("{0}:{1}".format(t.value,tokenizer.symbol()))
                tokenXml.AddNode(t.value,tokenizer.symbol())
            elif t == TokenType.IDENTIFIER:
                print("{0}:{1}".format(t.value,tokenizer.identifier()))
                tokenXml.AddNode(t.value,tokenizer.identifier())
            elif t == TokenType.INT_CONST:
                print("{0}:{1}".format(t.value,tokenizer.intVal()))
                tokenXml.AddNode(t.value,str(tokenizer.intVal()))
            elif t == TokenType.STRING_CONST:
                print("{0}:{1}".format(t.value,tokenizer.stringVal()))
                tokenXml.AddNode(t.value,tokenizer.stringVal())
            else:
                print("UNKOWN:{0}".format(str(t)))
        
        tokenXml.Save()
        print("结束处理文件:"+file)

main()