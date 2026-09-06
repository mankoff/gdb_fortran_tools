#!/usr/bin/env python3
from subprocess import run
from os import environ
import sys
import re
import numpy as np

# for pretty-printing
ok = "✅"
failed = "❌"

# check for GFT_DIR is well defined
if not("GFT_DIR" in environ.keys()):
  print(f"error GFT_DIR is not defined {failed}")
  sys.exit(-1)
else :
  print(f"GFT_DIR variable    {ok} : {environ["GFT_DIR"]}")

# put MAX_DIM in FPP
MAX_DIM = 6
with open("array_type.fpp","r") as fp_fpp:
    lines=fp_fpp.readlines()
    fp_fpp.close()
    with open("array_type.fpp", "w+") as fp_fp2:
        for s in lines:
           if re.match(r"^.*set MAX_DIM\s=.*$",s)!=None:
               sp = f"#:set MAX_DIM = {MAX_DIM}\n"
           else:
               sp = s
           fp_fp2.write(sp)
        fp_fp2.close()
# first let run fypp and gforfran
preProcessRet = run("fypp array_type.fpp array_type.f90".split(" "))
if (preProcessRet.returncode != 0):
  print(f"Preprocessing phase {failed}")
  sys.exit(-1)
else : 
  print(f"Preprocessing phase {ok}")

compileRet = run("gfortran -g array_type.f90 -o array_type.x".split(" "))
if (compileRet.returncode != 0):
  print(f"Compile phase       {failed}")
  sys.exit(-1)
else:
  print(f"Compilation phase   {ok}")


# compute check_val
check_value  = int(np.sum(np.arange(np.prod(np.arange(1,MAX_DIM+1)))))


# generate a gdb script
gdbHeader = """set startup-quietly on
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
  for TYPE in ['i4','i8','r4','r8','c4','c8']:
    curr = f"{TYPE}_{DIM}d"
    filename = f"gdb.scr_"+curr
    run(("rm -f "+filename).split(" "))
    with open(filename,"w") as fp:
      fp.writelines(gdbHeader)
      fp.write(f"set args {curr}\n")
      fp.write(f"b test_{curr}\n")
      fp.write(f"run\n")
      fp.write("n 3\n")
      fp.write("pycmd a np.sum(np.int_(np.real(_)))\n")
      fp.write("exit\n")
    # GDB run the script
    outFile = curr+".out"
    runRet = run(("gdb -q -x ./"+filename).split(" "), stdout=open(outFile, "w"))
    print(f"{curr} ............. {(ok if runRet.returncode == 0 else failed) }")
    #print(int(open(outFile, "r").readlines()[-1].strip()),"==",check_value)
    # cleaning current file
    run(["rm", filename, curr+".out"])
# cleaning generated files
run(["rm", "array_type.x", "array_type.f90"])
