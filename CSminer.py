import os
import re
import sys
import lizard
import string
from tkinter.constants import FALSE
from typing import Counter


class keyWords():
    loops = ['for ', 'while ', 'do ', 'if']
    op = ['and', 'or', 'xor']
    aritmeticOperator = ['+', '-', '*', '/', '%', 'sqrt', '^', 'pow', 'abs', 'log']
    specialOperands = ['++', '--', '**']
    comparativeOperator = ['<', '>', '<=', '>=', '==', '!=', '&&', '||', '!', '&', '|', '<<', '>>', '~', '^' ]
    comments = ['/*', '//', '*/', '/**', '*/' ]
    dataType = ['byte ', 'short ', 'int ', 'long ', 'double ', 'char ', 'boolean ', 'Integer ', 'float ', 'Byte ', 'Short ', 'Long ', 'Double ', 'Char ', 'Boolean ',]


class CSminer_openFile(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = self.openfile()
    
    def CSminerLizar(self):
        i = lizard.analyze_file(self.filePath)

        cyclomatic_complexity = i.function_list[0].__dict__['cyclomatic_complexity']
        nloc = i.function_list[0].__dict__['nloc']
        token_count = i.function_list[0].__dict__['token_count']
        start_line = i.function_list[0].__dict__['start_line']
        end_line = i.function_list[0].__dict__['end_line']
        full_parameters = i.function_list[0].__dict__['full_parameters']

        return cyclomatic_complexity, nloc, token_count, start_line, end_line, full_parameters

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

    def tloc(self):
        return len(CSmineOthers(self.data).dataSplit())
    
    def sloc_whbl(self):
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

    def numVar_numOper(self):
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

        count = CSmineOthers(aux1).countFunc()   
        return len(var), count

    def numMethodCall(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        #data = CSmineOthers(data).removeSpace()
        data = CSmineOthers(data).semiColomNoRemove()
        # find external methods
        aux = []
        pos = []
        
        for i in data:
            i = i.replace(';','')
            if i.find('.') != -1:
                a = list(set(i.split(' ')))
                aux += a

        for i in aux:
            if i.find('.') != -1:
                if CSminerBool.is_number(i) == FALSE:
                    pos.append(i)        
        return len(pos)


    def returnInfo(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        count = 0
        for i in data:
            i = i.replace('  ','')
            i = i.replace('{','')
            i = i.replace('}','')
            if 'return' in i:
                if ';' in i:
                    returnInf = i.replace(';','')
                    returnInf = returnInf.split(' ')
                    returnInf.remove('return')
                
                else: 
                    returnInf = i.split(' ')
                    returnInf.remove('return')
                count += 1

        if count == 0:
            return False, 0, 'NA', 'NA'
        
        else:
            
            for i in data:
                i = i.replace('  ','')
                if returnInf[0] + ' =' in i:
                    for j in keyWords.dataType:
                        if j in i:
                            returnInfaux = j
            return True, count, 1, returnInfaux


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
    
    def numVar_numOper(self):
        data = CSmineOthers(self.data).dataSplit()
        aux = []
        # number of arimetic operations
        for i in data:
            i = i.replace(' ','')
            if i != '':
                if i.find(':') == -1:
                    aux.append(i)
        count = CSmineOthers(aux).countFunc()

        # number of variable declared
        var = []
        oper = []
        aux2 = []
        for i in aux:
            if '=' in i:
                aux2.append(i)
                for j in keyWords.aritmeticOperator:
                    if j in i:
                        oper.append(i)
        var = [item for item in aux2 if item not in oper]
        # print(count)
        return len(var), count

    def returnInfo(self):
        data = CSmineOthers(self.data).dataSplit()
        data = CSmineOthers(data).removeBlankLines()
        count_howmanyReturns = 0
        for i in data:
            i = i.replace('  ','')
            
            if 'return' in i:
                returnInf = i.split(' ')
                returnInf.remove('return')
                count_howmanyReturns += 1

        if count_howmanyReturns == 0:
            return False, 0, 'NA', 'NA'
        
        else:
            return True, count_howmanyReturns, len(returnInf),'NA'


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
        
        a, len_a = CSmineOthers(aux2).argFinder()
        a = CSmineOthers(a[0]).argType()
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
    #        print(self.data)
            for i in self.data:
                #print(i)
                if '[' and ']' in i:
                    for j in keyWords.dataType:
                        j = j.replace(' ', '')
                        if j in i:
                            argDT.append('array_' + j)
                else:
                    for j in keyWords.dataType:
                        if j in i:
                            argDT.append(j)     
            return argDT

        except:
            for k in self.data:
                for i in k:
                    var = i.lower()
                    var = var.replace(' ', '')
                    
                    if '[' and ']' in var:
                        for j in keyWords.dataType:
                            if j in var:
                                argDT.append('array_' + j)
                    else:
                        for j in keyWords.dataType:
                            if j in var:
                                argDT.append(j)
            return argDT

    def countFunc(self):
        count = 0
        for i in self.data:
            for j in keyWords.aritmeticOperator:
                if j in i:
                    count +=1
        return count

    def semiColomRemove(self):
        aux = []
        for i in self.data:
            if not CSmineOthers(i).onlySpaces():
                if i.find(';') == -1:
                    aux.append(i)
        return aux
    
    def semiColomNoRemove(self):
        aux = []
        for i in self.data:
            if not CSmineOthers(i).onlySpaces():
                if i.find(';') != -1:
                    aux.append(i)
        return aux

class CSminerBool():
    def is_number(n):
        try:
            float(n)
            return True
        except ValueError:
            return False
