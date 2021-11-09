import os
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
        return len(self.data.split('\n'))
    
    def sloc_wbl(self):
        aux = self.data.split('\n')
        aux1 = []
        for i in aux:
            aux1.append( i.replace(' ', ''))
        aux2 = []
        for i in aux1:
            if i != '':
                aux2.append(i)
        return len(aux2)
    
    def sloc_statements(self):
        data = self.data.split('\n')
        aux= []
        for i in data:
            a = i.replace(' ', '')
            if a not in string.punctuation:
                aux.append(a)
        return(len(aux))

