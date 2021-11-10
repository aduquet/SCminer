import os
import re
import sys
import ast
import string
from typing import Counter

from networkx.classes.function import is_empty

class keyWords():
    loops = ['for ', 'while ', 'do ', 'if']
    op = ['and', 'or', 'xor']
    aritmeticOperator = ['+', '-', '*', '/', '%', '++', '--', '+=', '-=', '*=', '/=', '%=','**']
    comparativeOperator = ['<', '>', '<=', '>=', '==', '!=', '&&', '||', '!', '&', '|', '<<', '>>', '~', '^' ]
    comments = ['/*', '//', '*/', '/**', '*/' ]
class CSminer_openFile(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = self.openfile()
    
    def openfile(self):
        data = open(self.filePath, 'r')
        return data

    def is_non_empty_file(self): 
        return os.path.isfile(self.filePath) and os.path.getsize(self.filePath) > 0   
        
    def readFile(self):
        return self.data.read()

    def extFile(self):
        extSoport = ['py', 'cpp', 'java']
        
        try:
            ext = self.filePath.split('.')[-1]
            if  ext in extSoport:
                return ext
            else:
                raise Exception(ext)
        except Exception as inst:
            print('Extension file','".'+str(inst)+'"' ,'not suported') 
            sys.exit()

class CSminerGenericMetrics(object):
    def __init__(self, data):
        self.data = data

    def sloc(self):
        return len(CSmineOthers(self.data).dataSplit())
    
    def sloc_wbl(self):
        aux = CSmineOthers(self.data).dataSplit()
        aux = CSmineOthers(aux).removeSpace()
        return len(CSmineOthers(aux).removeBlankLines())
    
    def sloc_statements_wc(self):
        data = CSmineOthers(self.data).dataSplit()
        aux= []
        for i in data:
            a = i.replace(' ', '')
            if a not in string.punctuation:
                aux.append(a)
        return(len(aux))
    
    def numLoops(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        loops, pos = CSmineOthers(data).Loops()
        loops = list(filter(lambda a: a != 'if', loops))
        return len(loops)

class CSminerPY(object):
    def __init__(self, data):
        self.data = data

    def numArg(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        aux = []
        for i in data:
            if not CSmineOthers(i).onlySpaces():
                if i.find('def ') != -1:
                    aux.append(i)
        return CSmineOthers(aux).argFinder()
                
class CSminerJAVA(object):
    def __init__(self, data):
        self.data = data

    def numArg(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        aux = []
        for i in data:
            if not CSmineOthers(i).onlySpaces():
                if i.find('public static ') != -1:
                    aux.append(i)
        return CSmineOthers(aux).argFinder()

class CSminerCplus(object):
    def __init__(self, data):
        self.data = data

    def numArg(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        aux = []
        aux2 = []
        aux3 = []

        for i in data:
            if not CSmineOthers(i).onlySpaces():
                if i.find(';') == -1:
                    aux.append(i)
        loops, pos = CSmineOthers(aux).Loops()
        
        for i in range(0, len(aux)):
            if i not in pos:
                aux2.append(aux[i])
   
        for i in aux2:
            a = i.replace(' ', '')
            if a not in string.punctuation:
                aux3.append(a)
        return CSmineOthers(aux3).argFinder()

class CSmineOthers(object):

    def __init__(self, data):
        self.data = data
    
    def dataSplit(self):
        return self.data.split('\n')
    
    def removeBlankLines(self):
        aux = []
        for i in self.data:
            if i != '':
                aux.append(i)
        return aux
    
    def removeSpace(self):
        aux = []
        for i in self.data:
            aux.append(re.sub(' +', '', i))
        return aux
    
    def onlySpaces(self):
        return self.data.isspace()
    
    def argFinder(self):

        try:
            num = []
            if len(self.data) == 1:
                a = self.data[0].replace(' ', '')
                a = a[a.index('(') + 1 : a.index(')') ].split(',')
                return len(a)

            else:
                for i in self.data:
                    a = i.replace(' ', '')
                    a = a[a.index('(') + 1 : a.index(')') ].split(',')
                    num.append(len(a))
                return num
        except:

            num = []
            for i in self.data:
                if i.find('(') != -1:
                    a = i[i.index('(') + 1 : i.index(')') ].split(',')
                    num.append(a)
            num2= []
            for i in num:
                if len(num) == 1:
                    return len(i)
                else:
                    num2.append(len(i))
            return num2

    def Loops(self):
        loopsName = []
        pos = []
        for i in keyWords.loops:
            counter = 0
            for j in self.data:
                if i in j != -1:
                    loopsName.append(i)
                    pos.append(counter)
                counter += 1
        return loopsName, pos

