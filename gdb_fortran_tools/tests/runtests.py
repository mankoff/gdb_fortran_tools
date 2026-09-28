#!/usr/bin/env python3
from subprocess import run
from os import environ
import sys
import re
import numpy as np

# for pretty-printing
OK = "✅"
FAILED = "❌"

# check for GFT_DIR is well defined

if "GFT_DIR" in list(environ):
    print(f"GFT_DIR variable    {OK} : {environ["GFT_DIR"]}")
else:
    print(f"error GFT_DIR is not defined {FAILED}")
    sys.exit(-1)

# insert MAX_DIM value in array_type.fpp
MAX_DIM = 6
with open("array_type.fpp", "r") as fp_fpp:
    lines = fp_fpp.readlines()
    fp_fpp.close()
    with open("array_type.fpp", "w+") as fp_fp2:
        for s in lines:
            if re.match(r"^.*set MAX_DIM\s=.*$", s) is not None:
                sp = f"#:set MAX_DIM = {MAX_DIM}\n"
            else:
                sp = s
            fp_fp2.write(sp)
        fp_fp2.close()

# first let run fypp and gforfran
prepro_ret = run(["fypp", "array_type.fpp",
                  "array_type.f90"], check=False)
if prepro_ret.returncode != 0:
    print(f"Preprocessing phase {FAILED}")
    sys.exit(-1)
else:
    print(f"Preprocessing phase {OK}")

comp_ret = run(["gfortran", "-g", "array_type.f90",
                "-o", "array_type.x"], check=False)
if comp_ret.returncode != 0:
    print(f"Compilation phase   {FAILED}")
    sys.exit(-1)
else:
    print(f"Compilation phase   {OK}")


# compute check_val
check_value = int(np.sum(np.arange(np.prod(np.arange(1, MAX_DIM+1))+1)))

# generate a gdb script
GDBHEADER = """set startup-quietly on
set debuginfod enabled on
set debuginfod verbose 0
set debug libthread-db 0
set auto-load libthread-db on
set print thread-events off
set debug threads off
set interactive-mode off
set pagination off
set confirm off
file array_type.x
"""

for DIM in range(2, MAX_DIM+1):
    for TYPE in ['i4', 'i8', 'r4', 'r8', 'c4', 'c8']:
        curr = f"{TYPE}_{DIM}d"
        filename = "gdb.scr_"+curr
        run(["rm", "-f", filename], check=False)
        with open(filename, "w") as fp:
            fp.writelines(GDBHEADER)
            fp.write(f"set args {curr}\n")
            fp.write(f"b test_{curr}\n")
            fp.write("run\n")
            fp.write("n 3\n")
            fp.write("pycmd a np.sum(np.int_(np.real(_)))\n")
            fp.write("exit\n")
        # GDB run the script
        outFile = curr+".out"
        with open(outFile, "w") as f1:
            run_ret = run(["gdb", "-q", "-x", filename], check=False,
                          stdout=f1)
            f1.close()
            with open(outFile, "r") as f2:
                comp_val = int(f2.readlines()[-1].strip())
                if (comp_val == check_value) and (run_ret.returncode == 0):
                    print(f"{curr} ............. {OK}")
                else:
                    print(f"{curr} ............. {FAILED}")

        # cleaning current file
        run(["rm", filename, curr+".out"], check=False)
# cleaning generated files
run(["rm", "array_type.x", "array_type.f90"], check=False)
