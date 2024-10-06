# Maryam Rezaee (981813088) - first coding exercise (compiler design)

'''
This code contains three parts:
Scanner Construction - the classes required for the scanner to tokenise code
Language Grammar - the grammar of the language whose code will be tokenised
Interactive Code - the final part to recieve txt file and scan and tokenise
'''

# ------------------------ SCANNER CONSTRUCTION ------------------------

import re

class Scanner(object):

    # takes list of grammar and lines of code and creates empty list of
    # tokens, which will be later filled as token pairs are found
    def __init__(self, stringlist, grammar):
        self.string = stringlist
        self.grammar = grammar
        self.tokens = []

    def tokenise(self):
        # for each line, matches chrctrs to grammar (in order of priority)
        # and creates tokens if found; to do this, it jumps forward after
        # each found string to prevent repeats; what remains counts as error

        linenum = 1
        for line in self.string:
            linetokens = []
            index = 0
            while index < len(line):
                for pair in self.grammar:
                    pattern = pair[1]
                    compiled = re.compile(rf'{pattern}')
                    found = compiled.match(line[index:])

                    if found:
                        linetokens.append((pair[0], found.group()))
                        index += found.end() - 1
                        found = None
                        break
                        
                    elif self.grammar.index(pair) == len(self.grammar)-1:
                        ignore = [' ', '    ', '\n', '\t']
                        try:
                            if line[index] not in ignore:
                                linetokens.append(('error', line[index], f'line{linenum}'))
                        except IndexError:
                            break
                index += 1
                
            # if multiple errors are given back to back in a line, we merge them
            length = len(linetokens)
            i = 0
            while i <= length:
                i += 1
                try:
                    if linetokens[i][0] == 'error' and linetokens[i+1][0] == 'error':
                        temp = linetokens[i][1] + linetokens[i+1][1]
                        linetokens[i] = ('error', temp, linetokens[i+1][2])
                        linetokens.remove(linetokens[i+1])
                        i -= 1
                except IndexError:
                    pass

            linenum += 1
            self.tokens += linetokens


# -------------------------- LANGUAGE GRAMMAR --------------------------


# shaped as (type, regex alternatives)
grammar = [ ('key', 'if|else|while|do'),
            ('id', '[a-zA-Z_]\w+'),
            ('num', '((\d+(\.\d*)?)|(\.\d+))([eE][+-]?\d+)?'),
            ('op', '\+|-|\*|/'),
            ('r_op', '<|>|<=|>=|!=|=='),
            ('=', '='),
            ('{', '{'),
            ('}', '}'),
            (';', ';') ]


# -------------------------- INTERACTIVE CODE --------------------------


if __name__ == '__main__':

    filename = input('Enter file name to open (e.g. example.txt): ')
    with open(f'{filename}', 'r') as file:
        lines = file.readlines()
        
    code = Scanner(lines, grammar)
    code.tokenise()
    for token in code.tokens:
        print(token, end = ' ')
        
