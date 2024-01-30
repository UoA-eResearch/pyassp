import ctypes
import pathlib

from structs import DOBJ, AOPTS

if __name__ == '__main__':
    # Load libassp
    libname = pathlib.Path().absolute() / 'libassp-1.1' / 'src' / '.libs' / 'libassp.so'
    c_lib = ctypes.CDLL(libname)

    # Create options structure and set defaults
    opts = AOPTS()
    popts = ctypes.pointer(opts)
    c_lib.setFMTdefaults.argtypes = (ctypes.POINTER(AOPTS),)
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
    c_lib.computeFMT.argtypes = (ctypes.POINTER(DOBJ), ctypes.POINTER(AOPTS), ctypes.POINTER(DOBJ))
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
