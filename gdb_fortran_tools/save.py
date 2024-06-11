import pickle
import numpy as np

import gdb  # pylint: disable=E0401

from . import data_extractor
from . import util

class SaveCSV(gdb.Command):
    def __init__(self):
        super(SaveCSV, self).__init__("savecsv", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        filename, var = args.split()
        data = data_extractor.extract_var(var)
        np.savetxt(filename, data, delimiter=",")


class SavePy(gdb.Command):
    def __init__(self):
        super(SavePy, self).__init__("savepy", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        filename, var = args.split()
        data = data_extractor.extract_var(var)
        with open(filename, "wb") as file:
            pickle.dump(data, file)


class Save(gdb.Command):
    def __init__(self):
        super(Save, self).__init__("save", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        filename, var = args.split()
        data = data_extractor.extract_var(var)
        data.tofile(filename)


SaveCSV()
SavePy()
Save()
