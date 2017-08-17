import re, os, sys, itertools

class ACFStruct():
    def __init__(self, filepath):
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
#END ACFStruct


class VDFStruct():
    def __init__(self, filepath):
        with open(filepath, 'r+') as f:
            self.lines = f.readlines()
        self.filepath = filepath

    def new_lib(self, path):
        line = 4
        for i in self.lines[4::]:
            if i == '}\n':
                break
            line += 1

        lib_nums = [[int(j) for j in re.findall(r'\t\"([0-9]*)\"', i)] for i in self.lines[4:line]]
        lib_nums = list(itertools.chain.from_iterable(lib_nums))
        new_num = max(lib_nums) + 1
        self.lines.insert(line, ''.join(('\t', '"%d"\t\t"' % new_num, path, '"\n')))

        os.rename(os.path.join(self.filepath, '/steamapps/libraryfolders.vdf'),
                  os.path.join(self.filepath, '/steamapps/libraryfolders_backup.vdf'))

        with open(os.path.join(self.filepath, '/steamapps/libraryfolders.vdf'), 'r+') as f:
            f.seek(0)
            f.truncate()
            f.seek(0)
            f.writelines(self.lines)

#END VDFStruct