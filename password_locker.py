#! python3
# pw.py - An insecure password locker program.
import shelve, pyperclip, sys, os

os.chdir('D:\\Python_code\\Automate_stuff')

# TODO: Password strength detector

with shelve.open('pass') as my_shelf:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("""
              "Not enough or too many attributes")
              Usage:
              python pw.py: [account] - copy account password")
              python pw.py: 'list'    - copy all account's names"
              python pw.py: 'add' [account] [password]"
              python pw.py: 'del' [account]"
              """)
        sys.exit()
    elif len(sys.argv) == 2:
        # user wants the list with all acc names stored
        if sys.argv[1].lower() == 'list':
            pyperclip.copy(str(list(my_shelf.keys())))
            print('Copied all acc names to clipboard.')
        else:
            # user wants the pass for his acc name
            account = sys.argv[1]
            if account in my_shelf.keys():
                pyperclip.copy(my_shelf[account])
                print('Password for ' + account + ' copied to clipboard.')
            else:
                print('There is no account named ' + account)
    elif len(sys.argv) == 3:
        account = sys.argv[2]
        if sys.argv[1].lower() == 'add':
            if account not in my_shelf.keys():
                my_shelf[account] = pyperclip.paste()
                print('Saved pass for %s' % (account))
            else:
                print('Account already on the shelve.')
        elif sys.argv[1].lower() == 'del':
            del my_shelf[account]
            print('Deleted account: %s' % (account))
