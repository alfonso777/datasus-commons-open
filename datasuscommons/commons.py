from enum import Enum

class DATASUS_SYSTEM(str, Enum):
    SIA             =   "sia"
    SIH             =   "sih"
    SCNES           =   "scnes"
    CNES            =   "cnes"
    SIGTAP          =   "sigtap"

    @classmethod
    def from_value(cls, value):
        return cls._value2member_map_.get(value, None)

class DATASUS_SUBSYSTEM(str, Enum):
    SCNES_ARQUIVOS          =   "scnes_arquivos"
    SCNES_TERCEIROS_BRASIL  =   "scnes_terceiros_brasil"
    SCNES_S_UPSVAL          =   "scnes_s_upsval" 
    SCNES_DEFAULT           =   "scnes_default"

    @classmethod
    def from_value(cls, value):
        return cls._value2member_map_.get(value, None)


class DATASUS_REGEX_SYSTEM():
    @classmethod
    def get_name_regex_by_system(cls, system: DATASUS_SYSTEM, subsystem: DATASUS_SUBSYSTEM = None ) -> str:
        if system is None:
            return None
        elif system in [DATASUS_SYSTEM.SIA, DATASUS_SYSTEM.SIH, DATASUS_SYSTEM.CNES]:
            return r"(\w+)(\d{4,6})_?(\w*)"
        elif system == DATASUS_SYSTEM.SIGTAP:
            return r"([a-zA-Z]+)_?(\d{6})_?(v?\d*)"
        elif system == DATASUS_SYSTEM.SCNES and subsystem in  [DATASUS_SUBSYSTEM.SCNES_S_UPSVAL, DATASUS_SUBSYSTEM.SCNES_TERCEIROS_BRASIL]:
            return r"([a-zA-Z_-]+_?\d{1,2})_(\d{4,6})_?(\d*)"
        elif system == DATASUS_SYSTEM.SCNES:
            return r"([a-zA-Z_-]+)(\d{6})_?(\d*)"
        else:
            return None

    @classmethod
    def get_subsystem_uf_regex_by_system(cls, system: DATASUS_SYSTEM, subsystem: DATASUS_SUBSYSTEM = None ) -> str:
        if system is None:
            return None
        elif system in [DATASUS_SYSTEM.SIA, DATASUS_SYSTEM.SIH, DATASUS_SYSTEM.CNES]:
            return r"(\w+)(\w{2})"
        elif system == DATASUS_SYSTEM.SCNES and subsystem in  [DATASUS_SUBSYSTEM.SCNES_S_UPSVAL, DATASUS_SUBSYSTEM.SCNES_TERCEIROS_BRASIL]:
            return r"([a-zA-Z_-]+)_?(\d{1,2})"
        else:
            return None


UF_MAP = {
    'RO': 11,
    'AC': 12,
    'AM': 13,
    'RR': 14,
    'PA': 15,
    'AP': 16,
    'TO': 17,
    'MA': 21,
    'PI': 22,
    'CE': 23,
    'RN': 24,
    'PB': 25,
    'PE': 26,
    'AL': 27,
    'SE': 28,
    'BA': 29,
    'MG': 31,
    'ES': 32,
    'RJ': 33,
    'SP': 35,
    'PR': 41,
    'SC': 42,
    'RS': 43,
    'MS': 50,
    'MT': 51,
    'GO': 52,
    'DF': 53
}
