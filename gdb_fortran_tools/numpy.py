import gdb  # pylint: disable=E0401

from . import data_extractor
from . import util

import numpy as np

class NumpyCmd(gdb.Command):
    def __init__(self):
        super(NumpyCmd, self).__init__("np", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        cmd,var = args.split()
        data = data_extractor.extract_var(var)
        print(eval(f"np.{cmd}(data)"))
        
class PyCmd(gdb.Command):
    def __init__(self):
        super(PyCmd, self).__init__("pycmd", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        cmd,var = args.split()
        data = data_extractor.extract_var(var)
        eval(f"{cmd}(data)")

NumpyCmd()
PyCmd()
