#Maryam Rezaee (981813088)

import random
#to produce account numbers


class BankAccount:

    def __init__(self, name, ID, accNum, credit):
        self.name = name
        self.ID = ID
        self.accNum = accNum
        self.credit = credit
        
    def get_acc(self):
        return f"Customer name: {self.name}\nNational ID number: {self.ID}\nAccount number: {self.accNum}\nCredit: {self.credit}"
        
    def deposit(self, amount):
        if amount >= 0:
            self.credit += amount
            return f"Deposit was successful! Balance: {self.credit}"
        else:
            return "Amount must be positive."
    
    def withdraw(self, amount):
        if amount < self.credit and amount >= 0:
            self.credit -= amount
            return f"Withdraw was successful! Balance: {self.credit}"
        elif amount >= self.credit:
            return "You cannot empty your account."
        else:
            return "Amount must be positive."


import csv


with open('Bank.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    csvlines = list(reader)
    #to make code work without any previous file
    if len(csvlines) > 0: #avoiding error in case of empty list
        csvlines = csvlines[1:]
    csvheader = ['Customer', 'National ID', 'Acc Num', 'Credit']


#to ease updating csvfile
def updatecsv(header, lines):
    with open('Bank.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(lines)


if __name__ == '__main__':
    
    print("Welcome to the Bank of Wonderland!")
    
    while True:
        print("""Do you...
    1 ) Want to create an account?
    2 ) Want to check existing account?""")
        n = input("Enter your choice: ")

        
        if n == '1':
            print("\nTo create an account, there are only three simple steps...")
            name = input("Enter customer name: ")
            ID, credit = None, None
            
            while ID == None:
                try:
                    ID = int(input("Enter national ID number: "))
                except ValueError:
                    print("Oops! ID number must be int. Try again.")
                    
            while credit == None:
                try:
                    credit = int(input("Enter credit number: "))
                except ValueError:
                    print("Oops! Credit number must be int. Try again.")

            IsAccNew = 'Yes'
            for i in range(len(csvlines)-1):
                if csvlines[i][0] == name and int(csvlines[i][1]) == ID:
                    IsAccNew = 'No'
            
            if credit > 0 and IsAccNew == 'Yes':
                accNum = random.randint(100000000, 999999999)
                csvlines.append([name, ID, accNum, credit])
                updatecsv(csvheader, csvlines)
                print(f"Account was successfully created! We'll take good care of your money *winky face*\nAccount number: {accNum}\nBack to main menu...\n")
            elif credit <= 0:
                print("Sorry, we could not create your account. You need credit larger than 0.\nBack to main menu...\n")
            elif IsAccNew == 'No':
                print("Oops, an account already exists for that info.\nBack to main menu...\n")
                

        elif n == '2':
            name = input("Customer name: ")
            accNum = None
            while accNum == None:
                try:
                    accNum = int(input("Account number: "))
                except ValueError:
                    print("Oops! Account number must be int. Try again.")

            account = None
            for i in range(len(csvlines)-1):
                if csvlines[i][0] == name and int(csvlines[i][2]) == accNum:
                    index = i
                    account = BankAccount(csvlines[i][0], int(csvlines[i][1]), int(csvlines[i][2]), int(csvlines[i][3]))
                    print("You are in!")
                    
            while account != None:  
                print("""\nAvailable options:
    1 ) Show info
    2 ) Deposit
    3 ) Withdraw
    4 ) Exit account""")
                n = input("Enter number of option: ")
    
                if n == '1':
                    print(account.get_acc())
                elif n == '2':
                    try:
                        amount = int(input("Enter amount (in Rial): "))
                        print(account.deposit(amount))
                        csvlines[index][3] = account.credit
                    except ValueError:
                        print("Oops! Amount must be int. Back to 2nd manu...")
                elif n =='3':
                    try:
                        amount = int(input("Enter amount (in Rial): "))
                        print(account.withdraw(amount))
                        csvlines[index][3] = account.credit
                    except ValueError:
                        print("Oops! Amount must be int. Back to 2nd manu...")
                elif n =='4':
                    print("Have a nice day! Back to main menu...\n")
                    break
                updatecsv(csvheader, csvlines)
                       
            else:         
                print("No matching account. Check your info and try again.\n")


