# Maryam Rezaee - 981813088
# Huffman Decoding Program

'''
This code contains two parts:
- Tools -->  classes / functions needed in body of code
- Body  -->  main body of code (interaction with user, using tools, etc.)
'''

# -------------------------------- TOOLS --------------------------------


# class of each Huffman tree node
class Node:
    
    def __init__(self, parent = None, left = None, right = None):
        self.parent = parent  # parent of node
        self.left = left      # left child
        self.right = right    # right child
        self.char = ''        # character of the node


# get char from 8-bit string of ASCII
def getchar(bitstring):

    # turn binary string to int
    # then get  char from ASCII int
    charint = int(bitstring, 2)
    char = chr(charint)
    return char


# function to construct tree from preorder bin sequence
# process string recursively while traversing tree
# use getchar() to get char from bitstring of ASCII
def decodeTree(node, bitstring):

    # base case to break recursion
    if bitstring == '':
        return

    # if current node is an inner node
    # meaning it was made & passed before
    if node.left:

        # if the subtree is full, go back up
        if node.right:
            decodeTree(node.parent, bitstring)

        # if right subtree is None, make it, and
        # since current node was visited before
        # next bit refers to the new right child
        # so send the string to new child as is
        else:
            right = Node(node)
            node.right = right
            decodeTree(node.right, bitstring)

    # if current node is new and has no child
    # find out if it has to be a leaf or not
    else:

        # if it is an inner node, make child
        # remove bit for current node from bitstr
        if bitstring[0] == '0':
            left = Node(node)
            node.left = left
            decodeTree(node.left, bitstring[1:])

        # if we've reached a leaf, jump 8 bits for char
        # use getchar() to convert those 8 bits to char
        elif bitstring[0] == '1':
            node.char = getchar(bitstring[1:9])
            decodeTree(node.parent, bitstring[9:])


# function to decode text with Huffman tree
def decodeText(textcode, length, root):

    # store root to later return to it &
    # create var for storing decoded text
    curr = root
    text = ''

    # if text was single-symbol
    if textcode == '':
        for i in range(0, length):
            text += root.char

    # iterate through if possible
    for bit in textcode:

        # take the bit's action
        if bit == '0':
            curr = curr.left
        elif bit == '1':
            curr = curr.right

        # if we've reached a Huffman leaf
        # add leaf char and return to root
        if curr.left == None:
            text += curr.char
            curr = root
            
    return text    


# -------------------------------- BODY ---------------------------------


if __name__ == '__main__':

    # get file from user to decode
    # put the 2 lines of treecode and textcode into list
    name = input('Type file name (e.g. encoded.txt): ')
    with open(name, 'r', newline = '') as file:
        encoded = file.read().splitlines()
    # special case if original text was 1 char
    if len(encoded) == 2:
        encoded.append('')

    # reconstruct data from bitstring
    root = Node()
    decodeTree(root, encoded[0])
    text = decodeText(encoded[2], int(encoded[1]), root)

    # save decoded text in file
    with open('decoded.txt', 'w+', newline = '') as file:
        file.write(text)

    # print code and decoded text
    print('-- Encoded text:',
          encoded[0],
          encoded[1],
          encoded[2],
          '-- Decoded result:',
          text,
          sep = '\n')

