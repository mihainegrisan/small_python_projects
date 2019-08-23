import os, shutil

"""
    Searches for images bigger than 3MB and adds them into a folder.
    Useful when you have you family photos in a bunch of different places in your pc.
"""


def copy_archive_photos(PLACEMENT_FOLDER, MIN_SIZE = 3000000):
    nr = 0
    #os.chdir('D:\\')
    #folder = os.getcwd()
    folder = os.path.dirname(PLACEMENT_FOLDER)
    foldername_copy = os.path.basename(PLACEMENT_FOLDER)
    if not os.path.exists(PLACEMENT_FOLDER):
        os.makedirs(PLACEMENT_FOLDER)

    for foldername, subfolders, filenames in os.walk(folder):
        if foldername == foldername_copy: #'Poze_py'
            continue

        print('Adding files from %s...' % (foldername))
        folder = os.path.abspath(foldername)

        files_found_in_folder = nr
        for filename in filenames:
            abs_filename = os.path.join(folder, filename)
            if (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')) and os.path.getsize(abs_filename)>MIN_SIZE:
                try:
                    shutil.copy(abs_filename, PLACEMENT_FOLDER)
                    print(filename)
                    nr += 1
                except shutil.SameFileError:
                    pass # if it's the same photo then don't copy
                    # can add it with a different name ex 01, 02
        if files_found_in_folder is not nr:
            print('Done.')
    print(f' {nr} items bigger than {MIN_SIZE/1000} KB found')

    # Archive all found files
    from backup_to_zip import backup_to_zip
    print("Archiving ...")
    backup_to_zip(PLACEMENT_FOLDER)

if __name__ == '__main__'
    PLACEMENT_FOLDER = 'D:\\Poze_py'
    copy_archive_photos(PLACEMENT_FOLDER)
