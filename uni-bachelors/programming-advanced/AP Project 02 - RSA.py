#Maryam Rezaee (981813088)


import sys
sys.setrecursionlimit(10**6)
        

'''
This file contains three parts:
- Main Functions --> functions needed in main body of code (key production, etc.)
- Main Tools --> basic functions defined/redefined (PRNG, EGCD, etc.)
- Main Code --> main body of code (menu, interaction with user, etc.)
'''


# -------------------------- MAIN FUNCTIONS --------------------------


from time import time


# generating key pairs
def keys():
    
    # picking two prime numbers
    # seperating the loops to increase probablity
    while True:
        p = next(prng(time()))
        if primality(p, 20):
            break
    while True:
        q = next(prng(time()))
        if p != q and primality(q, 20):
            break

    # finding n, phi, e, d
    n = multiply(p, q)
    phi = multiply(p - 1, q - 1)
    
    i = 16
    while True:
        e = power(2, i) + 1
        if gcd(e, phi) == 1 and e < phi:
            break
        i -= 1
        
    d = modinv(e, phi)

    pubkey = (e, n)
    prvkey = (d, n)

    # putting keys in file
    with open('Keys.txt', mode = 'w') as file:
        file.write(f"Public key pair: {pubkey}\nPrivate key pair: {prvkey}")

    return f"Your public key pair: {pubkey}\nPrivate key pair is saved in file."


# ASCII block to int with ord() and base of 10
def blockOrd(string):

    integer = 0
    for i, j in enumerate(string):
        integer += (256 ** i) * ord(j)
    return integer


# int to ASCII block with chr() and base of 10
def blockChr(integer):

    string = []
    # finding the last index because
    # len of block might have been
    # shorter than maximum len
    i = 0
    quot = 257
    while quot > 256:
        quot = integer // (256 ** i)
        i += 1
    i -= 1 # removing last addition to have len of block
    
    while integer != 0:
        quot = integer // (256 ** i)
        string.append(chr(quot))
        integer %= 256 ** i
        i -= 1

    string.reverse()
    string = ''.join(string)
    return string
        

def encrypt(m, e, n):

    c = modexpo(m, e, n) 
    return c 


def decrypt(c, d, n):

    m = modexpo(c, d, n)
    return m


# -------------------------- MAIN TOOLS --------------------------


# linear congruential generator algorithm for
# pseudorandom number generator 
def prng(seed):
    
    seed = int(seed)
    # using 1024 and 512 so p * q would be larger than 1024 bits
    m = power(2, 1024)
    a = power(2, 512)

    c = 1
    while True:
        seed = (multiply(a, seed) + c) % m
        yield seed


# iterates Miller–Rabin primality test k times
def primality(n, k): 
      
    # corner cases 
    if n <= 1 or n == 4: 
        return False # is composite 
    elif n <= 3: 
        return True # is prime
    else:
  
        # finding d that n = ((2^d) * r) + 1
        d = n - 1
        while d % 2 == 0: 
            d //= 2 # d = d // 2
            
        # repeating for accuracy aka witness loop
        for i in range(k):
            # d is now odd
            if test(d, n) == False: 
                return False  # is composite
      
        return True # is probably prime


# Miller–Rabin primality test
def test(d, n):
      
    # picking a random number in [2, ..., n - 2] and we know n > 4
    import random
    a = 2 + random.randint(1, n - 4)
  
    # calculating (a^d) % n 
    x = modexpo(a, d, n)
  
    if x == 1 or x == n - 1: 
        return True # continuing witness loop
    else:
      
        # squaring x while none of the following is true:
        # d is n - 1 
        # (x^2) % n is 1
        # (x^2) % n is n - 1
        while d != n - 1:
            x = (x * x) % n 
            d *= 2
            
            if x == 1: 
                return False # is composite
            if x == n - 1: 
                return True # continuing witness loop
      
        return False #is composite
  

# to calculate modular exponentiation aka (x^y) % d but faster
# pow with 3 args (but for positive inputs only)
def modexpo(x, y, d): 
      
    result = 1 # in case y = 0
    
    # making sure these two conditions don't happen: x = d or x > d
    # and making x smaller for increasing speed
    # using Chinese remainder theorem
    x = x % d
    while y > 0: 
          
        # if y is odd
        if y & 1: 
            result = multiply(result, x) % d
  
        # y is now even
        y = y >> 1 # because bitwise shift is faster than y = y / 2 
        x = (x * x) % d 
      
    return result


# redefing pow function (for positive inputs only)
def power(x, y):

    if y == 0:
        return 1
    elif y == 1:
        return x
    elif y > 0:
        n = x
        for i in range(2, y + 1):
            x = multiply(x, n)
        return x


# Karatsuba algorithm for fast multiplication
def multiply(x, y):

    # for small numbers
    if len(str(x)) == 1 or len(str(y)) == 1:
        return x * y
    
    else:
        # factoring in plus–minus sign
        # (not needed but included for completion's sake)
        if x < 0 and y < 0:
            x, y, sign = abs(x), abs(y), 1
        elif x < 0:
            x, sign = abs(x), -1
        elif y < 0:
            y, sign = abs(y), -1
        else:
            sign = 1
            
        # finding middle
        m = max(len(str(x)),len(str(y)))
        m //= 2

        a = x // 10**(m)
        b = x % 10**(m)
        c = y // 10**(m)
        d = y % 10**(m)

        # 3 calls made to numbers approximately half the length
        z0 = multiply(b, d)
        z1 = multiply((a + b), (c + d))
        z2 = multiply(a, c)

        return sign * ((z2 * 10**(2 * m)) + ((z1 - z2 - z0) * 10**m) + (z0))    


# extended Euclidean algorithm to help find modulo inverse
def egcd(e, phi):  

    if e == 0 :   
        return phi, 0, 1
    else:    
        gcd, a, b = egcd(phi % e, e)  
        # updating with recursion results 
        a, b = b - multiply(phi // e, a), a
        return gcd, a, b 


# modular multiplicative inverse of e with respect to phi
# needed for finding d, which is mod inverse of e
def modinv(e, phi): 

    g, a, b = egcd(e, phi) 
    return a % phi


# needed for cheking if gcd(e, phi) is 1
def gcd(e, phi):
    
    gcd, a, b = egcd(e, phi)
    return gcd


# -------------------------- MAIN CODE --------------------------


if __name__ == '__main__':

    print("Welcome to RSA cipher probram!")
    
    while True:
        n = input("\nDo you wish to...\n1 ) generate keys\n2 ) encrypt\n3 ) decrypt\n4 ) exit\nEnter number of choice: ")

        if n == '1':
            print("Generating your keys now...")
            print(keys())

        elif n == '2':
            e, n = map(int, input("Enter key pair for encryption, divided by space: ").split())
            plaintext = input("Enter message: ")
            print("Encrypting message...")

            mlen = len(plaintext)
            mlist = []

            # setting each block as 20 characters because:
            # len of ASCII python unicode symbols is 256
            # smallest possible key is 1024 bits with data size of 164 bytes
            # put in the formula log(2 ** keySize, symbolsLen) it yields 20.5
            # using a smaller number helps the speed of program

            # if message is one block
            if mlen <= 20: 
                mlist.append(plaintext)

            # message is longer than one block
            elif mlen > 20:
                # diving to full blocks
                for i in range(mlen):
                    if (i+1) % 20 == 0:
                        mlist.append(plaintext[i-19:i+1])
                # in case an extra block shorter than 20 remains at the end
                if mlen % 20 != 0:
                    i = (mlen // 20) * 20
                    mlist.append(plaintext[i:])

            ciphertext = ''
            for m in mlist:
                m = blockOrd(m)
                c = encrypt(m, e, n)
                ciphertext += f'{c} '

            print(f"Your encrypted message: {ciphertext}")

        elif n == '3':
            d, n = map(int, input("Enter key pair for decryption, divided by space: ").split())
            ciphertext = input("Enter encrypted message (blocks divided by space): ")
            print("Decrypting message...")

            clist = list(ciphertext.split())
            plaintext = ''

            for c in clist:
                c = int(c)
                m = decrypt(c, d, n)
                m = blockChr(m)
                plaintext += f'{m}'

            print(f"Your decrypted message: {plaintext}")

        elif n == '4':
            print("We'll be here for your spy business whenever ;)")
            break
        
