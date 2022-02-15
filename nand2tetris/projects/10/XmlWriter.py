# coding=utf-8

import xml.dom.minidom as xml

class XmlWriter:

    def __init__(self,path:str) -> None:
        self._path = path
        self._dom:xml.Document = xml.getDOMImplementation().createDocument(None,None,None)
        self._curr:xml.Node = self._dom

    def Forword(self) -> None:
        n = self._curr.lastChild
        self._curr = n

    def Back(self) -> None:
        p = self._curr.parentNode
        self._curr = p

    def AddNode(self,name:str, txt:str) -> None:
        e = self._dom.createElement(name)
        if txt:
            e.appendChild(self._dom.createTextNode(txt))
        self._curr.appendChild(e)

    def Save(self) -> None:
        with open(self._path, 'w', encoding='utf-8') as f:
            self._dom.writexml(f, addindent='\t', newl='\n',encoding='utf-8')