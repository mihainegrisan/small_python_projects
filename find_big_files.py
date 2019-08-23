import os

""" Search for files bigger than 300MB and print their paths. """

os.chdir('D:\\')
folder = os.getcwd()

nr = 0
MIN_SIZE = 300000000  # 300 MB

for foldername, subfolders, filenames in os.walk(folder):
    if foldername == 'D:\\Poze_py' or foldername == 'D:\\Python_code':
        continue

    folder = os.path.abspath(foldername)

    for filename in filenames:
        abs_filename = os.path.join(folder, filename)
        if os.path.getsize(abs_filename)>MIN_SIZE:
            nr += 1
            print(f'Searching {abs_filename} ...')

print('Done.')
print(f'Found {nr} items bigger than {MIN_SIZE/1000000} MB.')
