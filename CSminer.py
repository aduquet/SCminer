import os
import re
import sys
import string

from networkx.classes.function import is_empty
   
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
    
    def sloc_statements(self):
        data = CSmineOthers(self.data).dataSplit()
        aux= []
        for i in data:
            a = i.replace(' ', '')
            if a not in string.punctuation:
                aux.append(a)
        return(len(aux))
    
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
        num = []
        if len(aux) == 1:
            a = aux[0].replace(' ', '')
            a = a[a.index('(') + 1 : a.index(')') ].split(',')
            return len(a)

        else:
            
            for i in aux:
                a = i.replace(' ', '')
                a = a[a.index('(') + 1 : a.index(')') ].split(',')
                num.append(len(a))
            
            return num
                

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


