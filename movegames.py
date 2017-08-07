from winreg import ConnectRegistry, OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx
import logging
from steamfiles import *

reg = ConnectRegistry(None, HKEY_CURRENT_USER)
steam_key = OpenKey(reg, r'Software\Valve\Steam', 0, KEY_READ)
install_path = (QueryValueEx(steam_key, "SteamPath"))

logging.debug("install path: ", install_path[0])
libraries = []

with open(''.join((install_path[0], '/steamapps/libraryfolders.vdf')), 'r+') as file:
    for line in file:
        libraries += re.findall(r'\"([A-Z]:.*?)\"', line)
        if len(libraries) > 0:
            libraries[-1] = re.sub(r'\\\\', '/', libraries[-1])

logging.debug("libraries found: ", len(libraries))
logging.debug("library results: ", libraries)

lib_contents = []
for d in libraries:
    sub_contents = []
    for f in os.listdir(''.join((d, '/SteamApps/'))):
        if 'app' in f:
            sub_contents.append(ACF_Struct(''.join((d, '/SteamApps/', f))))
    lib_contents.append(sub_contents)

# for i in range(len(lib_contents)):
#     for j in lib_contents[i]:
#         print(j.get_param("name"))
#         print(os.path.exists(''.join((libraries[i],'/SteamApps/common/', j.get_param("name")))))

while(True):
    for item in libraries:
        print(item, end='\t')
    print("0 to exit fam")
    myDir = input("Enter the directory you want to see: ")
    if myDir == '0':
        sys.exit(0)
    num = int()
    for i in range(len(libraries)):
        if libraries[i] == myDir:
            num = i
            break
    for item in lib_contents[i]:
        print(item.get_param("name"))

