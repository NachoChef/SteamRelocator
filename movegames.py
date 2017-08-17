from winreg import ConnectRegistry, OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx  #Kappa
import logging
from steamfiles import *
import os
import time

def setup():
    reg = ConnectRegistry(None, HKEY_CURRENT_USER)
    steam_key = OpenKey(reg, r'Software\Valve\Steam', 0, KEY_READ)
    install_path = QueryValueEx(steam_key, "SteamPath")

    logging.debug("install path: ", install_path[0])
    libraries = []

    with open(''.join((install_path[0], '/steamapps/libraryfolders.vdf')), 'r+') as file:
        for line in file:
            libraries += re.findall(r'\"([A-Z]:.*?)\"', line)
            if len(libraries) > 0:
                libraries[-1] = re.sub(r'\\\\', '/', libraries[-1])

    logging.debug("# libraries found: ", len(libraries))
    logging.debug("library results: ", libraries)

    lib_contents = []
    for d in libraries:
        sub_contents = []
        for f in os.listdir(''.join((d, '/SteamApps/'))):
            if 'app' in f:
                sub_contents.append(ACFStruct(''.join((d, '/SteamApps/', f))))
        lib_contents.append(sub_contents)
        logging.debug("library: ", d)
        logging.debug("contents: ", sub_contents)

    return install_path[0], libraries, lib_contents


def list_dir(libs):
    for i in libs:
        print(i, end='\t')
    #double return
    print('\n')


def view_dir(libraries, lib_contents):
    num = -1
    lib = input("Enter the library path: ").strip()
    for i in range(len(libraries)):
        if libraries[i] == lib:
            num = i
            break
    if num == -1:
        print("Not a valid library.\nCanceling print...\n")
        return None

    for item in lib_contents[i]:
        print(item.get_param("name"))
    print('\n\n')


def new_dir(install, new_lib_path):
    with VDFStruct(open(os.path.join((install, '/steamapps/libraryfolders.vdf')), 'r+')) as file:
        file.new_lib(new_lib_path)

def rm_dir(install):
    print("RM_DIR")


def mov_dir(source_list: list, dest: str):
    for source in source_list:
        start = time.time()
        size = os.stat(source).st_size
        chunk_size = size // 10000   #optimal? or 4K
        sz_per_seg = size // 40
        try:
            with open(source, 'rb') as infile:
                with open(dest, 'wb') as outfile:
                    copied = 0  # bytes
                    chunk = infile.read(chunk_size)
                    while chunk:
                        outfile.write(chunk)
                        copied += len(chunk)
                        elapsed = time.time() - start
                        time_per_byte = elapsed / float(copied)
                        remaining = size - copied
                        remaining_estimate = remaining * time_per_byte
                        yield (copied // sz_per_seg), remaining_estimate
                        # so it would yield number of progress bars to display, time remaining
                        chunk = infile.read(chunk_size)

        except IOError as err:
            print('\nERROR: %s' % err)
            sys.exit(1)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

#prelim testing
def main():

    #This is all being replaced

    install_path, libraries, lib_contents = setup()
    switcher = {'0': lambda: sys.exit(),
                '1': lambda: list_dir(libraries),
                '2': lambda: view_dir(libraries, lib_contents),
                '3': lambda: new_dir(install_path),
                '4': lambda: rm_dir(install_path),
                '5': lambda: mov_dir(install_path),
                'clr': lambda: cls()}

    while True:
        action = input('Type 0 to exit.\n'
                        'Type 1 to list current libraries.\n'
                        'Type 2 to see the contents of a library.\n'
                        'Type 3 to create a new library.\n'
                        'Type 4 to delete a library.\n'
                        'Type 5 to move a library.\n').strip()
        if action in switcher.keys():
            func = switcher[action]
            func()
        else:
            print("Not a valid option.\n")

if __name__ == '__main__':
    main()
