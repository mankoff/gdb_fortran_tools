import gdb  # pylint: disable=E0401

from . import data_extractor
from . import util

import numpy as np

class NumpyCmd(gdb.Command):
    """
    np min x
    """
    def __init__(self):
        super(NumpyCmd, self).__init__("np", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        cmd,var = args.split()
        data = data_extractor.extract_var(var)
        print(eval(f"np.{cmd}(data)"))
        
class PyCmd(gdb.Command):
    """
    pycmd x np.min(_) # same as "np min x"
    pycmd x np.min(_[np.where(_ != 0)]) # allows more complex queries
    """
    def __init__(self):
        super(PyCmd, self).__init__("pycmd", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        var = args.split()[0]
        cmd = ' '.join(args.split()[1:])
        _ = data_extractor.extract_var(var)
        eval(f"print({cmd})")

                       
NumpyCmd()
PyCmd()
