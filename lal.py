import os
import re
import sys

""" INIT GLOBALS - START """

tempfilename = 'tempfilename.tex'

# Temp variables for process function.
NO_NEW_LINE = '%!%NONEWLINE%!%'
NO_END_LINE = '%!%NOENDLINE%!%'

# Initialisation of Globals
def init():
    global isStartTag, isEndTag
    isStartTag = regexExactMatchFunction('={3,}start={3,}', re.I)
    isEndTag = regexExactMatchFunction('={3,}end={3,}', re.I)

noNewLineEnding = [
'{tabular}',
'{center}',
'{multicols}',
]
noNewLineEndingWithArguments = [
'{multicols}',
]
noNewLine = [
'{',
'}',
]

layoutSettings = {
    'default': ['\\usepackage[a4paper]{geometry}'],
    'wide': ['\\usepackage[margin=0.3in]{geometry}'],
    'narrow': [],
    '2col': ['\\usepackage[a4paper]{geometry}'],
    '3col': ['\\usepackage[margin=0.3in]{geometry}'],
}
layoutSettings_begin = {
    'default': [],
    'wide': [],
    'narrow': [],
    '2col': ['\\begin{multicols}{2}'],
    '3col': ['\\begin{multicols}{3}'],
}
layoutSettings_end = {
    'default': [],
    'wide': [],
    'narrow': [],
    '2col': ['\\end{multicols}'],
    '3col': ['\\end{multicols}'],
}

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
    
def removeEndBraces(line):
    if len(line) < 2: return ''
    if line[-1] != '}': return ''
    end = line.rfind('{')
    if end == -1: return ''
    return line[:end]
    
def process(s):
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
                if dontInsertNewLine(line):
                    line = line + '\n'
                else:
                    line = line + '\\\\\n'
            
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
    


def pdflatex(fileName):
    outputFile = setExt(fileName, 'pdf')
    removeIfExists(outputFile)
    os.system('pdflatex -halt-on-error ' + fileName)
    try:
        os.startfile(outputFile)
    except Exception as e:
        print('Cannot open file: ' + str(e))


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
    try:
        os.remove(file)
    except:
        pass
    
""" COMMANDS - START """
    
def cleanUp():
    removeIfExists(setExt(tempfilename, '.log'))
    removeIfExists(setExt(tempfilename, '.aux'))
    removeIfExists(setExt(tempfilename, '.tex'))
    
def printArgs(*args):
    print(','.join(map(str,args)))
    
def convertFileWithOption(option):
    def convertFile(*args):
        fileName = args[0]
        convert(fileName, option)            
        pdflatex(tempfilename)
    return convertFile
    
    
""" COMMANDS - END """    
    
def isCommandArgument(arg):
    return arg[0] == '-'
    
def initCommands():
    global commandMap
    commandMap = {
        'clean' : cleanUp,
        'test' : printArgs,
        'nar' : convertFileWithOption('narrow'),
        'narr' : convertFileWithOption('narrow'),
        'narrow' : convertFileWithOption('narrow'),
        'wide' : convertFileWithOption('wide'),
        '2col' : convertFileWithOption('2col'),
        '3col' : convertFileWithOption('3col'),
        '2' : convertFileWithOption('2col'),
        '3' : convertFileWithOption('3col'),
    }
    
def processCommand(args):
    arg = args[1]
    arg = arg[1:]
    command = commandMap[arg]
    command(*args[2:])
    
    
init()
if __name__ == '__main__':
    initCommands()
    args = sys.argv
    if len(args) < 2:
        print('Input a file name')
    else:
        if (isCommandArgument(args[1])):
            processCommand(args)
        else:
            fileName = args[1]
            convert(fileName)            
            pdflatex(tempfilename)