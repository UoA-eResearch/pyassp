import ctypes
from pathlib import Path

from enums import dtype_e
from structs import DOBJ, AOPTS, FMT_GD

# Load libassp
libname = Path().absolute() / 'libassp-1.1' / 'src' / '.libs' / 'libassp.so'
c_lib = ctypes.CDLL(str(libname))


def load_file(file: Path) -> ctypes.POINTER(DOBJ):
    assert file.exists(), f'File {file} does not exist'

    c_lib.allocDObj.restype = ctypes.POINTER(DOBJ)
    file_obj = c_lib.allocDObj()

    c_lib.asspFOpen.argtypes = (ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DOBJ))
    c_lib.asspFOpen.restype = ctypes.POINTER(DOBJ)

    fname = str(file).encode('utf-8')
    c_lib.asspFOpen(fname, 1, file_obj)

    return file_obj


def get_formants(input_path: Path, num_formants: int, window_size: float, gender: str, pre_emphasis: float):
    # Create options structure and set defaults
    opts = AOPTS()
    popts = ctypes.pointer(opts)
    c_lib.setFMTdefaults.argtypes = (ctypes.POINTER(AOPTS),)
    c_lib.setFMTdefaults(popts)

    opts.numFormants = num_formants
    opts.msSize = window_size
    assert gender in 'fmu', 'Expected gender to be m: male, f: female or u: unknown'
    opts.gender = ord(gender)
    opts.preEmph = pre_emphasis

    # Input file
    input_file = load_file(input_path)

    # Comput formants
    c_lib.computeFMT.argtypes = (ctypes.POINTER(DOBJ), ctypes.POINTER(AOPTS), ctypes.POINTER(DOBJ))
    c_lib.computeFMT.restype = ctypes.POINTER(DOBJ)
    result_pt = c_lib.computeFMT(input_file, popts, None)

    # Forest generics
    fmt_gd_pt = ctypes.POINTER(FMT_GD)
    fmt_gd = ctypes.cast(result_pt.contents.generic, fmt_gd_pt).contents

    num_frames = fmt_gd.endFrameNr - fmt_gd.begFrameNr

    # For now, print results to stdout
    for fr in range(num_frames):
        print(f'Frame {fr}')
        # TODO: return these values
        dd = result_pt.contents.ddl
        ptr = ctypes.c_void_p(result_pt.contents.dataBuffer)

        # Print LP1 value if present
        if dd.type == 'DT_LP1':
            d_ptr = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))
            print(f'    LP1: {d_ptr[0]}')
            ptr = ctypes.c_void_p(ptr.value + ctypes.sizeof(ctypes.c_double))
            dd = dd.next.contents

        # Frequency values
        i_pt = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_int16))
        for i in range(dd.numFields):
            print(f'    F{i}: {i_pt[i]}')
        offset = dd.numFields

        dd = dd.next.contents
        # Bandwidth values
        for i in range(dd.numFields):
            print(f'    B{i}: {i_pt[i + offset]}')

    # for f, _ in DOBJ._fields_:
    #     print(f'{f}: {getattr(result_pt.contents, f)}')


if __name__ == '__main__':
    # Iterate over all input files
    folder = Path().absolute() / 'wavs'

    for s_file in folder.iterdir():
        if s_file.suffix == '.wav':
            gender = 'f' if 'female' in s_file.name else 'm'
            print(s_file)
            get_formants(s_file, 2, 49.0, gender, 0.95)

    # TODO: also calculate rms and ksvf0 values
