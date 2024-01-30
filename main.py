import ctypes
import pathlib
from _ctypes import POINTER

from ctypes import c_long, c_double, c_int, c_char, c_uint16, c_uint8, c_size_t
from structs import ENDIAN, DDESC, DOfreeFunc, DOBJ
from enums import fform_e, fdata_e, dcode_e, dform_e, dtype_e

class aopts(ctypes.Structure):
    _fields_ = [("options", c_long), ("beginTime", c_double), ("endTime", c_double), ("centreTime", c_double), ("msSize", c_double),
         ("msShift", c_double), ("msSmooth", c_double), ("bandwidth", c_double), ("resolution", c_double), ("gain", c_double),
         ("range", c_double), ("preEmph", c_double), ("alpha", c_double), ("threshold", c_double), ("maxF", c_double),
         ("minF", c_double), ("nomF1", c_double), ("voiAC1", c_double), ("voiMag", c_double), ("voiProb", c_double),
         ("voiRMS", c_double), ("voiZCR", c_double), ("hpCutOff", c_double), ("lpCutOff", c_double), ("stopDB", c_double),
         ("tbWidth", c_double), ("FFTLen", c_long), ("channel", c_int), ("gender", c_int), ("order", c_int),
         ("increment", c_int), ("numLevels", c_int), ("numFormants", c_int), ("precision", c_int), ("accuracy", c_int),
         ("type", c_char * 32), ("format", c_char * 32), ("winFunc", c_char * 32)]

    def __repr__(self):
        strs = '\t'.join([f'{k}={getattr(self, k)}' for k, _ in self._fields_])

        return f'AOPTS:\n{strs}'


if __name__ == '__main__':
    # Load libassp
    libname = pathlib.Path().absolute() / 'libassp-1.1' / 'src' / '.libs' / 'libassp.so'
    c_lib = ctypes.CDLL(libname)

    # Create options structure and set defaults
    opts = aopts()
    popts = ctypes.pointer(opts)
    c_lib.setFMTdefaults.argtypes = (ctypes.POINTER(aopts), )
    c_lib.setFMTdefaults(popts)
    # TODO: set options from parameters

    # From r code
    opts.numFormants = 2
    opts.msSize = 49.0
    opts.gender = ord('f')
    opts.preEmph = 0.95

    # Input file
    s_file = pathlib.Path().absolute() / 'wavs' / 'oldfemale-word-taa-R001M.wav'
    assert s_file.exists()

    c_lib.allocDObj.restype = ctypes.POINTER(DOBJ)
    input_obj = c_lib.allocDObj()

    c_lib.asspFOpen.argtypes = (ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DOBJ))
    c_lib.asspFOpen.restype = ctypes.POINTER(DOBJ)

    fname = str(s_file).encode('utf-8')
    c_lib.asspFOpen(fname, 1, input_obj)

    # Run forest - compute formants
    c_lib.computeFMT.argtypes = (ctypes.POINTER(DOBJ), ctypes.POINTER(aopts), ctypes.POINTER(DOBJ))
    c_lib.computeFMT.restype = ctypes.POINTER(DOBJ)
    out_pt = c_lib.computeFMT(input_obj, popts, None)

    ## Attempt to parse data in output
    dd = out_pt.contents.ddl
    ptr = ctypes.c_void_p(out_pt.contents.dataBuffer)

    # Print LP1 value
    if dd.type == 'DT_LP1':
        d_ptr = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))
        print(f'LP1: {d_ptr[0]}')
        ptr = ctypes.c_void_p(ptr.value + ctypes.sizeof(ctypes.c_double))
        dd = dd.next.contents

    # Frequency values
    i_pt = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_int16))
    for i in range(dd.numFields):
        print(f'F{i}: {i_pt[i]}')
    offset = dd.numFields

    dd = dd.next.contents
    # Bandwidth values
    for i in range(dd.numFields):
        print(f'B{i}: {i_pt[i + offset]}')

    # TODO: convert freq/bandwidth to fm values
