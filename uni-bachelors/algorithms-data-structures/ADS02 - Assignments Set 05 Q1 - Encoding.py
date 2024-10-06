# Maryam Rezaee - 981813088
# Huffman Encoding Program

'''
This code contains two parts:
- Tools -->  classes / functions needed in body of code
- Body  -->  main body of code (interaction with user, using tools, etc.)
'''

# -------------------------------- TOOLS --------------------------------


# class of each Huffman tree node
class Node:
    
    def __init__(self, char, freq, left = None, right = None):
        self.char = char   # character of the node
        self.freq = freq   # frequency of the character
        self.left = left   # left child
        self.right = right # right child
        self.dir = ''      # direction / bit passed to get to node
        

# function to find dict of unique chars
# value of chars is their frequency
def freqcount(text):
    counted = {}

    # get count of each char in text
    # add each uniquw char to dict 
    # add one to count if it already exists
    for char in text:
        counted[char] = counted.get(char, 0) + 1
        
    return counted


# function to create Huffman tree
# from dict shaped as {char:freq}
def makeHuff(textdict):
    
    # make all unique chars leaf nodes
    # keep tree's nodes in a list to edit
    nodes = [] 
    for key in textdict:
        nodes.append(Node(key, textdict.get(key)))

    # create inner nodes from leaf nodes and replace them in list
    # continue untill all nodes have united and only root is left
    while len(nodes) > 1:

        # sort list each time and find two smallest nodes
        nodes = sorted(nodes, key = lambda node: node.freq)
        left = nodes[0]
        left.dir = '0'
        right = nodes[1]
        right.dir = '1'

        # unite two smallest nodes into a new inner node
        # remove nodes from list and replace with parent
        parent = Node(left.char + right.char,
                      left.freq + right.freq,
                      left, right)
        nodes.remove(right)
        nodes.remove(left)
        nodes.append(parent)

    # return root node
    return nodes[0]
        
    
# function to make chars into 8-bit binary
def getbin(char):

    bytearr = char.encode()                  # byte array
    byteint = int.from_bytes(bytearr, 'big') # binary int of byte array
    bytestr = f'{byteint:08b}'               # 8-bit binary string of int

    return bytestr


# function to traverse tree preorder to encode
# use getbin() to put 8-bit bin of each char
treecode = ''
def encodeTree(root):

    # global variable for encoded tree
    # to make it accessible in recursion
    global treecode

    # if current node is a parent
    if root.left:
        treecode += '0'
        # if it has a left child it means it has both children
        # because Huffman tree is always a complete binary tree
        encodeTree(root.left)
        encodeTree(root.right)

    # if current node is a leaf
    else:
        treecode += '1'
        treecode += getbin(root.char)


# function to get Huffman encoding of each char
# using a dictionary to store {char:code}
charcode = {}
def encodeChar(root, code = ''):

    # add the direction taken to current node
    code += root.dir
    
    # if children exist, traverse preoreder
    # Huffman tree is complete so 1 child means 2
    if root.left:
        encodeChar(root.left, code)
        encodeChar(root.right, code)

    # if node is leaf, save the code till now
    else:
        charcode[root.char] = code


# function to encode text using Huffman tree
# traversal is done preorder
textcode = ''
def encodeText(text):

    global textcode
    # iterate through text and find charcode of each
    # which is the value of its key in the dictionary
    for char in text:
        textcode += charcode.get(char)


# -------------------------------- BODY ---------------------------------


if __name__ == '__main__':

    # get file from user to encode
    # then convert file to string
    name = input('Type file name (e.g. text.txt): ')
    text = ''
    with open(name, 'r', newline = '') as file:
        for line in file:
            text = text + line

    # convert string to dict of {unique char : freq}
    # and create Huffman tree of text's unique chars
    textdict = freqcount(text)
    root = makeHuff(textdict)
    
    # change the treecode string to be encoded tree
    # start from found root
    encodeTree(root)
    # do the same to fill predefined charcode{}
    # and get dictionary of chars and codes
    encodeChar(root)
    # encode text using charcode{}
    # edits global textcode string
    encodeText(text)

    # save treecode, text len, and textcode
    # each will be a new line of file
    with open('encoded.txt', 'w+', newline = '') as file:
        file.write(treecode)
        file.write('\n')
        file.write(str(len(text)))
        file.write('\n')
        file.write(textcode)

    # finally calculate compression ratio
    # and print text and code and ratio
    textspace = len(text) * 8
    codespace = len(treecode + textcode) + len(bin(len(text)))
    compratio = codespace / textspace
    print('-- Original text:',
          text,
          '-- Encoded result:',
          treecode,
          len(text),
          textcode,
          f'-- Size of original text: {textspace}',
          f'-- Size of encoded result: {codespace}',
          f'-- Compression ratio: {compratio}',
          sep = '\n')

