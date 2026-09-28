# Rationale
- very first version of testing : test the `pycmd array np.sum` for all non-logical types

## Idea
 - using Fypp we generate a source `array_type.f90` containing a function doing the same job for a list a type and dimensions
 - we generate in a loop a gdb script which will stop on that function
 - we use `pycmd` and `sum` operator to test mapping on numpy types
 - we compare the printed value by the function and the value computed on the numpy array mapped to the fortran tensor


# Dependencies

- Gnu GDB
- gfortran (but maybe could be generalized to `ifx` or `pgf90`)
- Fypp

# how to use it
Running
```bash
export GFT_DIR=absolute/path/to/gdb_fortran_tools/
./runtests.py
```
must yield 
```bash
GFT_DIR variable    ✅ : /path/to/GFT_DIR
Preprocessing phase ✅
Compilation phase   ✅
i4_2d ............. ✅
i8_2d ............. ✅
r4_2d ............. ✅
r8_2d ............. ✅
c4_2d ............. ✅
c8_2d ............. ✅
i4_3d ............. ✅
i8_3d ............. ✅
r4_3d ............. ✅
r8_3d ............. ✅
c4_3d ............. ✅
c8_3d ............. ✅
i4_4d ............. ✅
i8_4d ............. ✅
r4_4d ............. ✅
r8_4d ............. ✅
c4_4d ............. ✅
c8_4d ............. ✅
i4_5d ............. ✅
i8_5d ............. ✅
r4_5d ............. ✅
r8_5d ............. ✅
c4_5d ............. ✅
c8_5d ............. ✅
i4_6d ............. ✅
i8_6d ............. ✅
r4_6d ............. ✅
r8_6d ............. ✅
c4_6d ............. ✅
c8_6d ............. ✅
```

# TODO
 - [ ] add test for logical using `np.anykkkk`
 - [X] compare the value computed by `sum(a)` and `np sum a`
 - [ ] add the 1d test (problem in fortran)
 - [ ] replace the ugly loop to insert MAX_DIM value in array_type.fpp
