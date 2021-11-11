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

    sloc = CSminerGenericMetrics(data).sloc()
    sloc_wbl = CSminerGenericMetrics(data).sloc_wbl()
    sloc_statements_wc = CSminerGenericMetrics(data).sloc_statements_wc()
    numLoops = CSminerGenericMetrics(data).numLoops()
    if CSminer_openFile(input_file).extFile() == 'py':
        numArg = CSminerPY(data).numArg()
        numVariablesDeclared, numAritOper = CSminerJAVA(data).numVar_numExpressions()
        print(sloc, sloc_wbl, sloc_statements_wc, numArg, numLoops)
    
    elif CSminer_openFile(input_file).extFile() == 'java':
        argDT, numArg = CSminerJAVA(data).numArg_argDT()
        numVariablesDeclared, numAritOper = CSminerGenericMetrics(data).numVar_numExpressions()
        print(sloc, sloc_wbl, sloc_statements_wc, numArg, argDT, numLoops, numVariablesDeclared, numAritOper)
    
    else:
        argDT, numArg = CSminerCplus(data).numArg_argDT()
        numVariablesDeclared, numAritOper = CSminerGenericMetrics(data).numVar_numExpressions()

        print(sloc, sloc_wbl, sloc_statements_wc, numArg, argDT, numLoops, numVariablesDeclared, numAritOper)


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('-i', '--input', 'input_file', help = 'Path to the file')
    @click.option('-nf', '--numbFiles', 'nf', help= 'One file or multple files/directory options are "f" for one file and "d" for directoy')
    @click.option('-o', '--output', 'output_file', help = 'Output file Name')

    def main(input_file, nf, output_file):

        if nf == 'f':
            data = oneFile(input_file)
            getMetrics(input_file, data)
            
        elif nf == 'd':
            multipleFiles(input_file)

        else:
            print('Something is wrong, please verify the comand line!')

main()