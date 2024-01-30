import ctypes


class EnumBase(int):
    _name = ''
    _values = {}

    def __init__(self, value):
        super().__init__()
        self.value = value


    def __new__(cls, value):
        if value not in cls._values.values():
            raise ValueError(f'{value} is not a valid {cls._name}')

        return super().__new__(cls, value)

    def __repr__(self):
        return f'{self.name} ({self.value})'

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, EnumBase):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        elif isinstance(other, str):
            assert other in self._values, f'{other} is not a valid {self._name}'
            return self._values[other] == self.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return list(self._values.keys())[list(self._values.values()).index(self.value)]


class fform_e(EnumBase):
    _name = 'fileFormat'

    _values = {
        'FF_ERROR': -1,
        'FF_UNDEF': 0,
        'FF_RAW': 1,
        'FF_ASP_A': 2,
        'FF_ASP_B': 3,
        'FF_XASSP': 4,
        'FF_IPDS_M': 5,
        'FF_IPDS_S': 6,
        'FF_AIFF': 7,
        'FF_AIFC': 8,
        'FF_CSL': 9,
        'FF_CSRE': 10,
        'FF_ESPS': 11,
        'FF_ILS': 12,
        'FF_KTH': 13,
        'FF_SWELL': 13,
        'FF_SNACK': 13,
        'FF_SFS': 14,
        'FF_SND': 15,
        'FF_AU': 15,
        'FF_NIST': 16,
        'FF_SPHERE': 16,
        'FF_PRAAT_S': 17,
        'FF_PRAAT_L': 18,
        'FF_PRAAT_B': 19,
        'FF_SSFF': 20,
        'FF_WAVE': 21,
        'FF_WAVE_X': 22,
        'FF_XLABEL': 23,
        'FF_YORK': 24,
        'FF_UWM': 25,
        'NUM_FILE_FORMATS': 26
    }


class fdata_e(EnumBase):
    _name = 'fileDataFormat'

    _values = {
        'FDF_ERROR': -1,
        'FDF_UNDEF': 0,
        'FDF_ASC': 1,
        'FDF_BIN': 2,
        'NUM_FILE_DATA_FORMATS': 3
    }


class dtype_e(EnumBase):
    _name = 'dataType'

    _values = {
        'DT_ERROR': -1,
        'DT_UNDEF': 0,
        'DT_TIME': 1,
        'DT_RECNR': 2,
        'DT_SMP': 3,
        'DT_MAG': 4,
        'DT_NRG': 5,
        'DT_PWR': 6,
        'DT_RMS': 7,
        'DT_ZCR': 8,
        'DT_PIT': 9,
        'DT_AC1': 10,
        'DT_LP1': 11,
        'DT_PROB': 12,
        'DT_ACF': 13,
        'DT_CCF': 14,
        'DT_LPC': 15,
        'DT_RFC': 16,
        'DT_ARF': 17,
        'DT_LAR': 18,
        'DT_LPCEP': 19,
        'DT_GAIN': 20,
        'DT_PQP': 21,
        'DT_FFB': 22,
        'DT_FBA': 23,
        'DT_FFR': 24,
        'DT_FBW': 25,
        'DT_FAM': 26,
        'DT_DFT': 27,
        'DT_FTAMP': 28,
        'DT_FTSQR': 29,
        'DT_FTPOW': 30,
        'DT_FTPHI': 31,
        'DT_FTFTS': 32,
        'DT_FTLPS': 33,
        'DT_FTCSS': 34,
        'DT_FTCEP': 35,
        'DT_MFCC': 36,
        'DT_FILTER': 37,
        'DT_TAG': 38,
        'DT_MRK': 39,
        'DT_LBL': 40,
        'DT_EPO': 41,
        'DT_PRD': 42,
        'DT_AMP': 43,
        'DT_DUR': 44,
        'DT_EGG': 45,
        'DT_EPG': 46,
        'DT_EMA': 47,
        'DT_XRM': 48,
        'DT_DATA_LOG': 49,
        'NUM_DATA_TYPES': 50
    }


# Conver to ctypes
class dform_e(EnumBase):
    _name = 'dataFormat'

    _values = {
        'DF_ERROR': -1,
        'DF_UNDEF': 0,
        'DF_BIT': 1,
        'DF_STR': 2,
        'DF_CHAR': 3,
        'DF_UINT8': 4,
        'DF_INT8': 5,
        'DF_UINT16': 6,
        'DF_INT16': 7,
        'DF_UINT24': 8,
        'DF_INT24': 9,
        'DF_UINT32': 10,
        'DF_INT32': 11,
        'DF_UINT64': 12,
        'DF_INT64': 13,
        'DF_REAL32': 14,
        'DF_REAL64': 15,
        'NUM_DATA_FORMATS': 16
    }


class dcode_e(EnumBase):
    _name = 'dataCoding'

    _values = {
        'DC_ERROR': -1,
        'DC_UNDEF': 0,
        'DC_LIN': 1,
        'DC_PCM': 1,
        'DC_BINOFF': 2,
        'DC_FNORM1': 3,
        'DC_ALAW': 4,
        'DC_uLAW': 5,
        'DC_ACE2': 6,
        'DC_ACE8': 7,
        'DC_MAC3': 8,
        'DC_MAC6': 9,
        'DC_DELTA': 10,
        'DC_ADPCM': 11,
        'DC_G721': 12,
        'DC_G722': 13,
        'DC_G723_3': 14,
        'DC_G723_5': 15,
        'DC_MS_ADPCM': 16,
        'DC_CL_ADPCM': 17,
        'DC_IDVI_ADPCM': 18,
        'DC_OKI_ADPCM': 19,
        'DC_IBM_ADPCM': 20,
        'DC_MPEG3': 21,
        'DC_MIX': 22,
        'DC_SAM': 23,
        'DC_XLBL': 24,
        'DC_TXY': 25,
        'DC_XYD': 26,
        'NUM_DATA_CODINGS': 27
    }


class wfunc_e(EnumBase):
    _name = 'windowFunction'

    _values = {
        'WF_ERROR': -1,
        'WF_NONE': 0,
        'WF_RECTANGLE': 1,
        'WF_TRIANGLE': 2,
        'WF_BARTLETT': 2,
        'WF_FEJER': 2,
        'WF_PARABOLA': 3,
        'WF_RIESZ': 3,
        'WF_WELCH': 3,
        'WF_COSINE': 4,
        'WF_COS': 4,
        'WF_COS_2': 5,
        'WF_HANN': 5,
        'WF_COS_3': 6,
        'WF_COS_4': 7,
        'WF_HAMMING': 8,
        'WF_BLACKMAN': 9,
        'WF_BLACK_X': 10,
        'WF_BLACK_3': 11,
        'WF_BLACK_M3': 12,
        'WF_BLACK_4': 13,
        'WF_BLACK_M4': 14,
        'WF_NUTTAL_3': 15,
        'WF_NUTTAL_4': 16,
        'WF_GAUSS2_5': 17,
        'WF_GAUSS3_0': 18,
        'WF_GAUSS3_5': 19,
        'WF_KAISER2_0': 20,
        'WF_KAISER2_5': 21,
        'WF_KAISER3_0': 22,
        'WF_KAISER3_5': 23,
        'WF_KAISER4_0': 24,
        'WF_NUM_FIX': 25,
        'WF_COS_A': 25,
        'WF_GEN_HAMM': 26,
        'WF_GAUSS_A': 27,
        'WF_KAISER_A': 28,
        'WF_KAISER_B': 29,
        'WF_KBD_A': 30,
        'WF_NUM_ALL': 31
    }