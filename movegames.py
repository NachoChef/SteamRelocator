from winreg import ConnectRegistry, OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx  #Kappa
import logging
from steamfiles import *
import os


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
                sub_contents.append(ACF_Struct(''.join((d, '/SteamApps/', f))))
        lib_contents.append(sub_contents)
        logging.debug("library: ", d)
        logging.debug("contents: ", sub_contents)

    return install_path, libraries, lib_contents

# for i in range(len(lib_contents)):
#     for j in lib_contents[i]:
#         print(j.get_param("name"))
#         print(os.path.exists(''.join((libraries[i],'/SteamApps/common/', j.get_param("name")))))
def list_dir(libs):
    for i in libs:
        print(i, end='\t')
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


def new_dir(install):
    print("NEW_DIR")


def rm_dir(install):
    print("RM_DIR")


def mov_dir(install):
    print("MOV_DIR")


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def main():
    install_path, libraries, lib_contents = setup()
    switcher = {'0': lambda: sys.exit(),
                '1': lambda: list_dir(libraries),
                '2': lambda: view_dir(libraries, lib_contents),
                '3': lambda: new_dir(install_path),
                '4': lambda: rm_dir(install_path),
                '5': lambda: mov_dir(install_path),
                'clr': lambda: cls()}

    while True:
        action = input('Type 0 to exit.\n' \
                  'Type 1 to list current libraries.\n' \
                  'Type 2 to see the contents of a library.\n' \
                  'Type 3 to create a new library.\n' \
                  'Type 4 to delete a library.\n' \
                  'Type 5 to move a library.\n').strip()
        if action in switcher.keys():
            func = switcher[action]
            func()
        else:
            print("Not a valid option.\n")

if __name__ == '__main__':
    main()
