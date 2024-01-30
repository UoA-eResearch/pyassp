from ctypes import *

from enums import wfunc_e


# convert above to ctypes
class ENDIAN(Union):
    _fields_ = [('word',  c_uint16), ('byte', c_uint8 * 2)]


class DDESC(Structure):
    pass

DDESC._fields_ = [("ident", c_char_p), ("unit", c_char * 8), ("factor", c_char * 4), ("type", c_int),
                ("format", c_int), ("coding", c_int), ("orientation", ENDIAN), ("numBits", c_uint16),
                ("zeroValue", c_uint32), ("offset", c_size_t), ("numFields", c_size_t), ("ascFormat", c_char * 8),
                ("sepChars", c_char * 4), ("next", POINTER(DDESC))]

DOfreeFunc = CFUNCTYPE(None, c_void_p)

class DOBJ(Structure):
    _fields_ = [("filePath", c_char_p), ("fp", c_void_p), ("openMode", c_int), ("fileFormat", c_int),
                ("fileData", c_int), ("fileEndian", ENDIAN), ("version", c_long), ("headerSize", c_long),
                ("sampFreq", c_double), ("dataRate", c_double), ("frameDur", c_long), ("recordSize", c_size_t),
                ("startRecord", c_long), ("numRecords", c_long), ("Time_Zero", c_double), ("Start_Time", c_double),
                ("sepChars", c_char * 4), ("eol", c_char * 4), ("ddl", DDESC), ("generic", POINTER(c_int)),
                ("doFreeGeneric", POINTER(DOfreeFunc)), ("dataBuffer", c_void_p), ("doFreeDataBuf", POINTER(DOfreeFunc)),  # check null ptr
                ("maxBufRecs", c_long), ("bufStartRec", c_long), ("bufNumRecs", c_long), ("bufNeedsSave", c_int8),
                ("userData", POINTER(c_int)), ]


class FMT_GD(Structure):
    _fields_ = [("ident", c_char * 32), ("options", c_long), ("frameSize", c_long), ("begFrameNr", c_long),
                ("endFrameNr", c_long), ("winFunc", c_int), ("nomF1", c_double), ("rmsSil", c_double),
                ("preEmph", c_double), ("lpOrder", c_int), ("numFormants", c_int), ("channel", c_int),
                ("writeOpts", c_int), ("accuracy", c_int)]