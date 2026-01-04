import os
import sys

ACCOUNTS_FILE = 'accounts.txt'

# Helper functions for file operations
def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                acc_no, name, balance = line.strip().split(',')
                accounts[acc_no] = {'name': name, 'balance': float(balance)}
    return accounts

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        for acc_no, data in accounts.items():
            f.write(f"{acc_no},{data['name']},{data['balance']}\n")

def create_account(accounts):
    acc_no = input('Enter new account number: ')
    if acc_no in accounts:
        print('Account already exists!')
        return
    name = input('Enter account holder name: ')
    try:
        balance = float(input('Enter initial deposit: '))
        if balance < 0:
            raise ValueError('Initial deposit cannot be negative.')
    except ValueError as e:
        print('Invalid amount:', e)
        return
    accounts[acc_no] = {'name': name, 'balance': balance}
    save_accounts(accounts)
    print('Account created successfully!')

def deposit(accounts):
    acc_no = input('Enter account number: ')
    if acc_no not in accounts:
        print('Account not found!')
        return
    try:
        amount = float(input('Enter amount to deposit: '))
        if amount <= 0:
            raise ValueError('Amount must be positive.')
    except ValueError as e:
        print('Invalid amount:', e)
        return
    accounts[acc_no]['balance'] += amount
    save_accounts(accounts)
    print('Deposit successful!')

def withdraw(accounts):
    acc_no = input('Enter account number: ')
    if acc_no not in accounts:
        print('Account not found!')
        return
    try:
        amount = float(input('Enter amount to withdraw: '))
        if amount <= 0:
            raise ValueError('Amount must be positive.')
        if amount > accounts[acc_no]['balance']:
            raise ValueError('Insufficient balance.')
    except ValueError as e:
        print('Invalid amount:', e)
        return
    accounts[acc_no]['balance'] -= amount
    save_accounts(accounts)
    print('Withdrawal successful!')

def check_balance(accounts):
    acc_no = input('Enter account number: ')
    if acc_no not in accounts:
        print('Account not found!')
        return
    print(f"Account Holder: {accounts[acc_no]['name']}")
    print(f"Balance: {accounts[acc_no]['balance']}")

def main():
    while True:
        print('\n--- Bank Account Management System ---')
        print('1. Create Account')
        print('2. Deposit')
        print('3. Withdraw')
        print('4. Check Balance')
        print('5. Exit')
        choice = input('Enter your choice: ')
        accounts = load_accounts()
        if choice == '1':
            create_account(accounts)
        elif choice == '2':
            deposit(accounts)
        elif choice == '3':
            withdraw(accounts)
        elif choice == '4':
            check_balance(accounts)
        elif choice == '5':
            print('Thank you for using the system!')
            sys.exit()
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()
