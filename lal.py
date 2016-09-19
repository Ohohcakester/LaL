import os
import re
import sys

""" INIT GLOBALS - START """

tempfilename = '__generated__tex__.tex'

# Temp variables for process function.
NO_NEW_LINE = '%!%NONEWLINE%!%'
NO_END_LINE = '%!%NOENDLINE%!%'

# Initialisation of Globals
def init():
    global isStartTag, isEndTag
    isStartTag = regexExactMatchFunction('={3,}start={3,}', re.I)
    isEndTag = regexExactMatchFunction('={3,}end={3,}', re.I)

# By default, we include all:
#     \begin + noNewLineEnding
# and \begin + noNewLineEndingWithArguments
noPrecedingNewLine = [
]
noNewLineEnding = [
'{tabular}',
'{center}',
'{multicols}',
'{enumerate}',
'{itemize}',
'{cases}',
'{matrix}',
'{pmatrix}',
'{align*}',
]
noNewLineEndingWithArguments = [
'{multicols}',
'{tabular}',
'\\section',
'\\subsection',
]
noNewLine = [
'{',
'}',
'\\hline',
'\\columnbreak',
]

layoutSettings = {
    'default': ['\\usepackage[a4paper]{geometry}'],
    'wide': ['\\usepackage[margin=0.3in]{geometry}'],
    'narrow': [],
    '2col': ['\\usepackage[a4paper]{geometry}'],
    '2colw': ['\\usepackage[margin=0.6in]{geometry}'],
    '3col': ['\\usepackage[margin=0.3in]{geometry}'],
}
layoutSettings_begin = {
    'default': [],
    'wide': [],
    'narrow': [],
    '2col': ['\\begin{multicols}{2}'],
    '2colw': ['\\begin{multicols}{2}'],
    '3col': ['\\begin{multicols}{3}'],
}
layoutSettings_end = {
    'default': [],
    'wide': [],
    'narrow': [],
    '2col': ['\\end{multicols}'],
    '2colw': ['\\end{multicols}'],
    '3col': ['\\end{multicols}'],
}

ERROR = 1
NO_ERROR = 0

""" INIT GLOBALS - END """
    
    
def dontInsertNewLine(line):
    if line in noNewLine:
        return True
    for ending in noNewLineEnding:
        if line.endswith(ending):
            return True
    for ending in noNewLineEndingWithArguments:
        if removeEndBraces(line).endswith(ending):
            return True
    return False
    
    
def dontPrecedeWithNewLine(line):
    if line in noPrecedingNewLine:
        return True
    if line.startswith('\\begin'):
        if dontInsertNewLine(line[len('\\begin'):]):
            return True
    return False
    
def removeEndBraces(line):
    if len(line) < 2: return ''
    if line[-1] != '}': return ''
    end = line.rfind('{')
    if end == -1: return ''
    return line[:end]
    
def process(s):
    s = s.replace('\n\\columnbreak', '\n\\vfill\\columnbreak')
    s = s.replace('\\end{addmargin}\n~\\\\\n', '\\\\\n\\end{addmargin}\n')
    s = s.replace('~\\\\\n'+NO_NEW_LINE,'\n')
    s = s.replace('\\\\\n'+NO_NEW_LINE,'\n')
    s = s.replace(NO_NEW_LINE,'')
    
    s = s.replace(NO_END_LINE+'\\\\','')
    s = s.replace(NO_END_LINE,'')
    
    return s

def convert(fileName, layout = 'default'):
    f = open(fileName)
    lines = f.read().split('\n')
    f.close()
    while len(lines) > 0 and len(lines[0]) == 0:
        lines = lines[1:]
        
    lines = trimByStartAndEndTags(lines)
        
    def convert(line):
        margin = len(line) - len(line.lstrip())
        if margin > 0 and len(line.strip()) > 0:
            line = ''.join([
                NO_NEW_LINE,
                '\\begin{addmargin}['+str(margin/2)+'em]{0em}\n',
                line,
                '\n\\end{addmargin}\n'])
        elif line.startswith('[img=') and line.endswith(']'):
            target = line[len('[img='):-len(']')]
            height = '100'
            if ',' in target:
                height = target[target.rfind(',')+1:]
                target = target[:target.rfind(',')]
            line = ''.join([
                NO_NEW_LINE,
                '\\begin{center}\n',
                '\\includegraphics[height=',
                height,
                'px]{',
                target,
                '}\n',
                '\\end{center}\n'])
        elif line == '\\newpage':
            line = '\\newpage \\noindent\n'
        else:
            if len(line.strip()) == 0:
                line = '~\\\\\n'
            else:
                dontPrecede = dontPrecedeWithNewLine(line)
                if dontInsertNewLine(line):
                    line = line + '\n'
                else:
                    line = line + '\\\\\n'
                if dontPrecede:
                    line = NO_NEW_LINE + line
            
        return line
        
    lines += [NO_NEW_LINE + NO_END_LINE]
    lines = map(convert, lines)
    
    try:
        os.remove(tempfilename)
    except:
        pass
    f = open(tempfilename, 'w+')
    f.write('\n'.join([
        '\\documentclass{article}',
        '\\usepackage{graphicx}',
        '\\usepackage{scrextend}',
        '\\usepackage{amsmath}',
        '\\usepackage{amsfonts}',
        '\\usepackage{multicol}',
        ]+layoutSettings[layout]+[
        '\\newcommand{\\floor}[1]{\\lfloor #1 \\rfloor}',
        '\\newcommand{\\ceil}[1]{\\lceil #1 \\rceil}',
        '\\begin{document}',
        ]+layoutSettings_begin[layout]+[
        '\\noindent',
        process(''.join(lines)),
        ]+layoutSettings_end[layout]+[
        '\\end{document}'
        ]))
    f.close()
    


def pdflatex(fileName, outputFile):
    tempOutputFile = setExt(fileName, 'pdf')
    removeIfExists(tempOutputFile)
    removeIfExists(outputFile)
    errcode = os.system('pdflatex -halt-on-error ' + fileName)
    if errcode == 0:
        renameIfExists(tempOutputFile, outputFile)
    return errcode


def trimByStartAndEndTags(lines):
    start = 0
    end = len(lines)

    for i in range(0,len(lines)):
        line = lines[i]
        if isStartTag(line):
            start = i+1
        elif isEndTag(line):
            end = i
    return lines[start:end]
    
def setExt(fileName, ext):
    if ext[0] == '.': ext = ext[1:]
    return fileName[:fileName.rfind('.')] + '.' + ext
    
def regexExactMatchFunction(regex, flags = None):
    if flags == None:
        prog = re.compile(regex)
    else:
        prog = re.compile(regex, flags)
        
    def match(string):
        m = prog.match(string)
        if m == None: return False
        return m.string == string
    return match

def removeIfExists(file):
    try: os.remove(file)
    except: pass

def renameIfExists(fromFile, toFile):
    try: os.rename(fromFile, toFile)
    except: pass
        
""" ACTIONS - START """
    
def cleanUp(cmdhandler):
    removeIfExists(setExt(tempfilename, '.log'))
    removeIfExists(setExt(tempfilename, '.aux'))
    removeIfExists(setExt(tempfilename, '.tex'))
    return NO_ERROR
    
def printArgs(cmdhandler):
    print(','.join(map(str,cmdhandler.args)))
    return NO_ERROR
    
def convertFile(cmdhandler):
    if len(cmdhandler.args) < 2:
        print('Input a file name')
        return ERROR
    fileName = cmdhandler.args[-1]
    if (fileName.startswith('-')):
        print('Input a file name')
        return ERROR
    
    convert(fileName, cmdhandler.layout)
    
    outputFile = setExt(fileName, 'pdf')
    if cmdhandler.outputFile == fileName:
        print('Error: outputfile is the same as the input tex file!')
        return ERROR
    
    if cmdhandler.outputFile != None:
        outputFile = cmdhandler.outputFile
    
    errcode = pdflatex(tempfilename, outputFile)
    
    if not cmdhandler.noOpen and errcode == 0:
        try:
            os.startfile(outputFile)
        except Exception as e:
            print('Cannot open file: ' + str(e))
    
    return errcode
    
""" ACTIONS - END """


""" COMMANDS - START """

def setLayout(layout):
    def fun(cmdhandler):
        cmdhandler.layout = layout
    return fun
    
def setAction(action):
    def fun(cmdhandler):
        cmdhandler.action = action
    return fun

def noOpen(cmdhandler):
    cmdhandler.noOpen = True
    
def setOutputFile(cmdhandler, outputFile):
    cmdhandler.outputFile = outputFile
    
def initCommands(cmdhandler):
    cmdhandler.commandMap = {
        'clean' : setAction(cleanUp),
        'test' : setAction(printArgs),
        'nar' : setLayout('narrow'),
        'narr' : setLayout('narrow'),
        'narrow' : setLayout('narrow'),
        'wide' : setLayout('wide'),
        '2col' : setLayout('2col'),
        '2colw' : setLayout('2colw'),
        '3col' : setLayout('3col'),
        '2' : setLayout('2col'),
        '2w' : setLayout('2colw'),
        '3' : setLayout('3col'),
        'noopen' : noOpen,
        'out': waitForArgument(setOutputFile),
    }

""" COMMANDS - END """

def waitForArgument(action):
    def fun(cmdhandler):
        cmdhandler.argumentHandler.setCommand(action)
    return fun
        

class ArgumentHandler(object):
    def __init__(self):
        self.command = None

    def setCommand(self, command):
        self.command = command
        
    def hasCommandLoaded(self):
        return self.command != None
    
    def runWithArgument(self, cmdhandler, arg):
        self.command(cmdhandler, arg)
        self.command = None
    

class CommandHandler(object):
    def __init__(self):
        self.layout = 'default'
        self.noOpen = False
        self.action = convertFile
        self.outputFile = None
        self.argumentHandler = ArgumentHandler()
        
        initCommands(self)
        
        
    def processCommand(self, arg):
        arg = arg[1:]
        if arg not in self.commandMap:
            print('Unknown option: -' + arg)
            sys.exit(1)
        command = self.commandMap[arg]
        command(self)
        
    def parseArgs(self, args):
        remainingArgs = []
        for arg in args:
            if self.argumentHandler.hasCommandLoaded():
                self.argumentHandler.runWithArgument(self, arg)
            elif arg[0] == '-':
                self.processCommand(arg)
            else:
                remainingArgs.append(arg)
        self.args = remainingArgs
        
    def run(self):
        errcode = self.action(self)
        if errcode == None: return 0
        return errcode

    
init()
if __name__ == '__main__':
    handler = CommandHandler()
    handler.parseArgs(sys.argv)
    errcode = handler.run()
    sys.exit(errcode)