import re
from typing import Tuple, Optional

import gdb  # pylint: disable=E0401
import gdb.types  # pylint: disable=E0401
import numpy as np

from .type_handler import TypeHandler, ScalarTypeHandler

COMPLEX_REGEX = re.compile("(\\S*) \\+ (\\S*) \\* I")


# class StdVector(TypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type).startswith("std::vector") and str(gdb_type.template_argument(0)) != "bool"

#     def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
#         size = int(gdb_value["_M_impl"]["_M_finish"] - gdb_value["_M_impl"]["_M_start"])
#         return (size,)

#     def contained_type(self, gdb_value: gdb.Value) -> gdb.Type:
#         return gdb_value.type.template_argument(0)

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return (gdb_value["_M_impl"]["_M_start"] + index[0]).dereference()


# class StdVectorBool(TypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type).startswith("std::vector") and str(gdb_type.template_argument(0)) == "bool"

#     def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
#         base_size = int(gdb_value["_M_impl"]["_M_finish"]["_M_p"] - gdb_value["_M_impl"]["_M_start"]["_M_p"])
#         size = 64 * base_size + int(gdb_value["_M_impl"]["_M_finish"]["_M_offset"])
#         print(size)
#         return (size,)

#     def contained_type(self, gdb_value: gdb.Value) -> gdb.Type:
#         return gdb_value.type.template_argument(0)

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         container_index = index[0]//64
#         offset = index[0] % 64
#         b64 = int((gdb_value["_M_impl"]["_M_start"]["_M_p"] + container_index).dereference())
#         value = bool(b64 & (1 << offset))

#         return gdb.Value(value)


# class StdArray(TypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type).startswith("std::array")

#     def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
#         size = int(gdb_value.type.template_argument(1))
#         return (size,)

#     def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
#         return gdb_value.type.template_argument(0)

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return gdb_value["_M_elems"][index[0]]


# class Pointer(TypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return gdb_type.code == gdb.TYPE_CODE_PTR

#     def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
#         return (None,)

#     def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
#         return gdb_value.type.target()

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return gdb_value[index[0]]


# class Array(TypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return gdb_type.code == gdb.TYPE_CODE_ARRAY

#     def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
#         size = gdb_value.type.range()[1] + 1
#         return (size, )

#     def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
#         return gdb_value.type.target()

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return gdb_value[index[0]]


# class Double(ScalarTypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type) == "double"

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return np.float64(gdb_value)


# class Float(ScalarTypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type) == "float"

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return np.float32(gdb_value)


# def extract_complex(gdb_value) -> complex:
#     complex_str = str(gdb_value["_M_value"])
#     complex_match = COMPLEX_REGEX.search(complex_str)
#     real, imag = complex_match.group(1), complex_match.group(2)
#     return float(real) + 1j * float(imag)


# class StdComplexDouble(ScalarTypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type) == "std::complex<double>"

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return np.complex128(extract_complex(gdb_value))


# class StdComplexFloat(ScalarTypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type) == "std::complex<float>"

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return np.complex64(extract_complex(gdb_value))


# class Integral(ScalarTypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type) in (
#             "char", "short", "int", "long", "long long",
#             "unsigned char", "unsigned short", "unsigned int", "unsigned long", "unsigned long long"
#         )

#     def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
#         return ()

#     def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
#         dtype = str(gdb.types.get_basic_type(gdb_value.type))
#         prefix = "u" if "unsigned" in dtype else "i"
#         if "char" in dtype:
#             size = "1"
#         elif "short" in dtype:
#             size = "2"
#         elif "int" in dtype:
#             size = "4"
#         else:
#             size = "8"

#         self.np_dtype = np.dtype(prefix + size)
#         return None

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return self.np_dtype.type(gdb_value)


# class Bool(ScalarTypeHandler):
#     @staticmethod
#     def can_handle(gdb_type: gdb.Type) -> bool:
#         return str(gdb_type) == "bool"

#     def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
#         return np.bool(gdb_value)


class FortranArray(TypeHandler):
    @staticmethod
    def can_handle(gdb_type: gdb.Type) -> bool:
        return np.any(
            [_ in str(gdb_type).lower() for _ in
             ["real(4)", "real(kind=4)",
              "real(8)", "real(kind=8)",
              "integer(4)", "integer(kind=4)",
              "integer(8)", "integer(kind=8)",
              "logical"]
             ])

    def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
        dims = (str(gdb_value.type).split(' ')[-1])[1:-1]
        shape = np.array(dims.split(',')).astype(int)
        return shape

    def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
        dtype = str(gdb.types.get_basic_type(gdb_value.type))
        if "logical" in dtype:
            size = "bool"
        elif "kind=4" in dtype:
            size = "f4"
        elif "kind=8" in dtype:
            size = "f8"
        else:
            size = "f4"

        self.np_dtype = np.dtype(size)
        return None

    def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
        if np.shape(index)[0] == 1:
            arr = np.array([gdb_value[i+1] for i in range(index[0])])
        if np.shape(index)[0] == 2:
            arr = np.zeros(index).T.astype(self.np_dtype)
            for i in range(index[0]):
                for j in range(index[1]):
                    arr[j,i] = gdb_value[j+1][i+1]
        if np.shape(index)[0] == 3:
            arr = np.zeros(index).T.astype(self.np_dtype)
            for i in range(index[0]):
                for j in range(index[1]):
                    for k in range(index[2]):
                        arr[k,j,i] = gdb_value[k+1][j+1][i+1]
        return arr.astype(self.np_dtype.type)

