import re, os, sys

class ACF_Struct():
    def __init__(self, filepath):
        lines = []
        with open(filepath, 'r+') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = re.findall(r'\t\t\"(.*?)\"', lines[i].strip())
            if i > 9:
                break
        if lines == [[]]:
            print("removing empty file at %s" % filepath)
            os.remove(filepath)
            sys.exit()
        try:
            self.__info = {"appid":lines[2][0],
                         "name":lines[4][0],
                         "dir":lines[6][0],
                         "isupdating":lines[8][0] == 0,
                         "SizeOnDisk":lines[9][0],
                         "filepath":filepath}
        except EOFError:
            print("ERROR IN DATA SET")

    def get_param(self, k: str):
        if k in self.__info.keys():
            return self.__info[k]
        else:
            raise ValueError('INVALID KEY NAME')

    def get_keys(self):
        return self.__info.keys()
#END ACF_Struct