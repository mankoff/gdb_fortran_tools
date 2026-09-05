from subprocess import run

# first let run fypp and gforfran
run("rm -f array_type.f90 array_type.x".split(" "))
run("fypp array_type.fpp array_type.f90".split(" "))
run("gfortran -g array_type.f90 -o array_type.x".split(" "))

MAX_DIM = 3 #! synchronize in fypp with a sed command
for DIM in range(2, MAX_DIM+1):
  for TYPE in ['i4','i8','r4','r8']:
    filename = f"gdb.scr_{TYPE}_{DIM}"
    run(("rm -f "+filename).split(" "))
    with open(filename,"w") as fp:
        fp.write("set startup-quietly on\n")
        fp.write("set debuginfod enabled on\n")
        fp.write("set debuginfod verbose 0\n")
        fp.write("set debug libthread-db 0\n")
        fp.write("set debug threads off\n")
        fp.write("set interactive-mode off\n")
        fp.write("set print thread-events off\n")
        fp.write("set pagination off\n")
        fp.write("set confirm off\n")
        fp.write("file array_type.x\n")
        fp.write(f"b test_{TYPE}_{DIM}d\n")
        fp.write("run\n")
        fp.write("n\n")
        fp.write("n\n")
        fp.write("n\n")
        fp.write("np sum a\n")
        fp.write("exit\n")
    run(("gdb -q -x ./"+filename).split(" "))
run("rm -f array_type.x array_type.f90 gdb.scr*".split(" "))
