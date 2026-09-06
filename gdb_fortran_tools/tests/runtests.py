#!/usr/bin/env python3
from subprocess import run
from os import environ
import sys

# for pretty-printing
ok = "✅"
failed = "❌"

# check for GFT_DIR is well defined
if not("GFT_DIR" in environ.keys()):
  print(f"error GFT_DIR is not defined {failed}")
  sys.exit(-1)
else :
  print(f"GFT_DIR variable defined {ok} : {environ["GFT_DIR"]}")

# first let run fypp and gforfran
#run("rm -f array_type.f90 array_type.x".split(" "))
preProcessRet = run("fypp array_type.fpp array_type.f90".split(" "))
if (preProcessRet.returncode != 0):
  print(f"Preprocessor phase {failed}")
  sys.exit(-1)
else : 
  print(f"Preprocessing phase      {ok}")

compileRet = run("gfortran -g array_type.f90 -o array_type.x".split(" "))
if (compileRet.returncode != 0):
  print(f"Compile phase       {failed}")
  sys.exit(-1)
else:
  print(f"Compilation phase       {ok}")

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
                                 
MAX_DIM = 2 #! synchronize in fypp with a sed command
for DIM in range(2, MAX_DIM+1):
  for TYPE in ['i4','i8','r4','r8']:
    curr = f"{TYPE}_{DIM}d"
    filename = f"gdb.scr_"+curr
    run(("rm -f "+filename).split(" "))
    with open(filename,"w") as fp:
      fp.writelines(gdbHeader)
      fp.write(f"set args {curr}\n")
      fp.write(f"b test_{curr}\n")
      fp.write("run\n")
      fp.write("n 3\n")
      fp.write("np sum a\n")
      fp.write("exit\n")
    # GDB run the script
    runRet = run(("gdb -q -x ./"+filename).split(" "))
    print(f"{curr} -> {(ok if runRet.returncode == 0 else failed) }")
    # cleaning current file
    run(["rm", filename])
      
# cleaning generated files
run(["rm", "array_type.x", "array_type.f90"])
