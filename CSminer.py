import os
import re
import sys
import string
from typing import Counter


class keyWords():
    loops = ['for ', 'while ', 'do ', 'if']
    op = ['and', 'or', 'xor']
    aritmeticOperator = ['+', '-', '*', '/', '%', 'sqrt', '^', 'pow']
    specialOperands = ['+=', '-=', '*=', '/=', '%=', '++', '--', '**']
    comparativeOperator = ['<', '>', '<=', '>=', '==', '!=', '&&', '||', '!', '&', '|', '<<', '>>', '~', '^' ]
    comments = ['/*', '//', '*/', '/**', '*/' ]
    dataType = ['byte ', 'short ', 'int ', 'long ', 'double ', 'char ', 'boolean ', 'integer ', 'float ']


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

    def numVar_numExpressions(self):
        data = CSmineOthers(self.data).dataSplit()
        aux = []
        for i in data:
            if not CSmineOthers(i).onlySpaces():
                if i.find(';') != -1:
                    aux.append(i)
        #aux = CSmineOthers(aux).removeSpace()
        var = []
        for i in aux:
            for j in keyWords.dataType:
                if j in i:
                    var.append(i)

        loops, pos = CSmineOthers(aux).Loops()
        aux1 = []
        if len(loops) != 0:
            for i in range(0, len(aux)):
                if i not in pos:
                    aux1.append(aux[i])
        else:
            aux1 = aux

        count = 0
        for i in aux1:
            for j in keyWords.aritmeticOperator:
                if j in i:
                    count +=1      
        
        return len(var), count

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

    def numArg_argDT(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        aux = []
        for i in data:
            if not CSmineOthers(i).onlySpaces():
                if i.find('public static ') != -1:
                    aux.append(i)

        a, len_a = CSmineOthers(aux).argFinder()
        a = CSmineOthers(a).argType()
        return a, len_a
    
    
class CSminerCplus(object):
    def __init__(self, data):
        self.data = data

    def numArg_argDT(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        aux = []
        aux2 = []
 
        for i in data:
            if not CSmineOthers(i).onlySpaces():
                if i.find(';') == -1:
                    aux.append(i)
        loops, pos = CSmineOthers(aux).Loops()
        
        for i in range(0, len(aux)):
            if i not in pos:
                aux2.append(aux[i]) 
        #print(aux3)
        a, len_a = CSmineOthers(aux2).argFinder()
        a = CSmineOthers(a).argType()
        return a, len(a)


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
                a = self.data[0]
                a = a[a.index('(') + 1 : a.index(')') ].split(',')
                return a, len(a)

            else:
                try:
                    num2 =[]
                    for i in self.data:
                        a = i[i.index('(') + 1 : i.index(')') ].split(',')
                        num.append(a)
                        num2.append(len(a))
                    return num, num2
                except:
                    for i in self.data:
                        if '(' in i:
                            a = i[i.index('(') + 1 : i.index(')') ].split(',')
                            num.append(a)
                            num2.append(len(a))
                    return num, num2

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
    
    def argType(self):
        argDT = []
        try:
            for i in self.data:
                var = i.lower()
                if '[]' in var:
                    for j in keyWords.dataType:
                        j = j.replace(' ', '')
                        if j + '[' in var:
                            argDT.append('array_' + j)
                else:
                    for j in keyWords.dataType:
                        if j in var:
                            argDT.append(j)   
            return argDT

        except:
            for k in self.data:
                for i in k:
                    var = i.lower()
                    if '[]' in var:
                        for j in keyWords.dataType:
                            j = j.replace(' ', '')
                            if j in var:
                                argDT.append('array_' + j)
                    else:
                        for j in keyWords.dataType:
                            if j in var:
                                argDT.append(j)
            return argDT

