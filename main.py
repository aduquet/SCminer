import os
from CSminer import *
import pickle
import pathlib
import warnings
import glob as gl
import numpy as np
import pandas as pd
import networkx as nx
from tkinter import *
from tkinter.filedialog import askopenfile

def checkPaths(inputPaths):
    try:
        if len(inputPaths) != 0:
            return True
        else:
            raise NameError('\n ** Path list is empty! please verify the files path **')
    except NameError:
        print('*** An exception flew by! ***\n')
        raise

def oneFile(input_file):
    try:
        CSminer_openFile(input_file).extFile()
        if CSminer_openFile(input_file).is_non_empty_file():
            content = CSminer_openFile(input_file).readFile()
            return content
        else:
            print('Empty file!')
    except OSError:
        print('The file ' '"', input_file, '" does not exist!')

def multipleFiles(input_file):
    inputPaths = gl.glob(input_file)
    checkPaths(inputPaths)
    for input in inputPaths:
        try:
            CSminer_openFile(input).extFile()
            if CSminer_openFile(input).is_non_empty_file():
                content = CSminer_openFile(input).readFile()
                # print(content)
            else:
                print('Empty file!')
        except OSError:
            print('The file ' '"', input, '" does not exist!')

def getMetrics(input_file, data):

    name = input_file.split('\\')[-1]
    name = name.split('.')[0]
    
    cyclomatic_complexity, nloc, token_count, start_line, end_line, full_parameters = CSminer_openFile(input_file).CSminerLizar()
    
    updateDF(name, 'cyclomatic_complexity', cyclomatic_complexity)
    updateDF(name, 'nloc', nloc)
    updateDF(name, 'token_count', token_count)
    updateDF(name, 'start_line', start_line)
    updateDF(name, 'end_line', end_line)
    updateDF(name, 'full_parameters', full_parameters)

    updateDF(name, 'tloc', CSminerGenericMetrics(data).tloc())    
    
    updateDF(name, 'sloc_wbl', CSminerGenericMetrics(data).sloc_wbl())
    
    updateDF(name, 'sloc_statements_wc', CSminerGenericMetrics(data).sloc_statements_wc())    
    
    updateDF(name, 'numLoops', CSminerGenericMetrics(data).numLoops())    
    
    updateDF(name, 'numMethodsCalled', CSminerGenericMetrics(data).numMethodCall())    
    
    if CSminer_openFile(input_file).extFile() == 'py':
        argDT, numArg = CSminerPY(data).numArg()
        updateDF(name, 'argDT', 'NA') 
        updateDF(name, 'numArg', 'NA') 
        
        numVariablesDeclared, numAritOper = CSminerPY(data).numVar_numOper()
        updateDF(name, 'numArg', numVariablesDeclared)
        updateDF(name, 'numArg', numAritOper)
        
        # print(sloc, sloc_wbl, sloc_statements_wc, argDT, numArg, numLoops, numVariablesDeclared, numAritOper, numMethodsCalled)
    
    elif CSminer_openFile(input_file).extFile() == 'java':
        argDT, numArg = CSminerJAVA(data).numArg_argDT()
        updateDF(name, 'numArg', argDT)
        updateDF(name, 'numArg', numArg)
        
        numVariablesDeclared, numAritOper = CSminerGenericMetrics(data).numVar_numOper()
        updateDF(name, 'numArg', numVariablesDeclared)
        updateDF(name, 'numArg', numAritOper)

        # print(sloc, sloc_wbl, sloc_statements_wc, numArg, argDT, numLoops, numVariablesDeclared, numAritOper, numMethodsCalled)
    
    else:
        argDT, numArg = CSminerCplus(data).numArg_argDT()
        updateDF(name, 'numArg', argDT)
        updateDF(name, 'numArg', numArg)
        
        numVariablesDeclared, numAritOper = CSminerGenericMetrics(data).numVar_numOper()
        updateDF(name, 'numArg', numVariablesDeclared)
        updateDF(name, 'numArg', numAritOper)
        
        # print(sloc, sloc_wbl, sloc_statements_wc, numArg, argDT, numLoops, numVariablesDeclared, numAritOper, numMethodsCalled)
    
    saveDF(df_main)

def updateDF(method_id, metric_id, metric):
    global df_main

    if not df_main.empty:
        df_main.at[method_id, metric_id] = metric        
    
    else:
        df_main.at[method_id] = method_id
        df_main.at[method_id, metric_id] = metric
    
def saveDF(name):

    print(df_main)
    

def createDF():
    global df_main

    metric_names = [ 
        'method_id',
        'cyclomatic_complexity', 
        'nloc', 
        'token_count', 
        'start_line', 
        'end_line', 
        'full_parameters',
        'tloc', 
        'sloc_wbl', 
        'sloc_statements_wc', 
        'argDT', 
        'numArg', 
        'numLoops', 
        'numVariablesDeclared', 
        'numAritOper', 
        'numMethodsCalled'
    ]

    df_main = pd.DataFrame(columns = metric_names, index=None)


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('-i', '--input', 'input_file', help = 'Path to the file')
    @click.option('-nf', '--numbFiles', 'nf', help= 'One file or multple files/directory options are "f" for one file and "d" for directoy')
    @click.option('-o', '--output', 'output_file', help = 'Output file Name')

    def main(input_file, nf, output_file):

        global df_main
        

        here_iam = str(pathlib.Path().absolute())
        resultsPath = here_iam + '\\CSminerResults-csv'
        createDF()

        if not os.path.exists(resultsPath):
            os.mkdir(resultsPath)

        if nf == 'f':
            data = oneFile(input_file)
            getMetrics(input_file, data)
            
        elif nf == 'd':
            multipleFiles(input_file)

        else:
            print('Something is wrong, please verify the comand line!')

main()