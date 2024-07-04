from .constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, MODE_ECI, MODE_MIXED, ERROR_CORRECTION_LEVEL_L, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_H
import re
import codecs

class QRCode:

    def __init__ (self, version = None, error_correction = ERROR_CORRECTION_LEVEL_H):
        self.version = version
        self.error_correction = error_correction
        self.en = Encoder()

    def add_data(self, data : str, mode = None):
        self.en.add_data(data, mode)
        
    def make(self):
        # TODO: implement this method
        pass
    
    def get_minimum_version(self, error_correction):
        # TODO: implement this method
        # for i in range(1, 41):
        pass
            
    def total_module_by_version(self, version : int) -> int:
        if version < 1 or version > 40:
            return 0
        return (version * 4 + 17) ** 2
    
    def total_functional_module_by_version(self, version : int) -> int:
        first = 202
        second = 235
        if version < 1 or version > 40:
            return 0
        elif version == 1:
            return first
        elif version == 2:
            return second
        else:
            big_jump = version // 7
            small_jump = (version - 2 - big_jump) * 8
            big_jump = 123 * big_jump + 25 * (big_jump - 1) * big_jump
            return second + small_jump + big_jump
        
    def total_format_version_module_by_version(self, version : int) -> int:
        if version < 1 or version > 40:
            return 0
        elif version < 7:
            return 31
        else:
            return 67

    def total_data_module_by_version(self, version : int) -> int:
        return self.total_module_by_version(version) - self.total_functional_module_by_version(version) - self.total_format_version_module_by_version(version)
    
    def total_error_correction_module(self, version: int, error_correction: int) -> int:
        # TODO: implement this method
        pass

    def total_data_bits(self) -> int:
        # TODO: implement this method
        pass
  
# Manage a list of data which one node can be encoded in different mode but if a node has a specific mode it will be encoded in that mode
# The encoding is optimized as specified in the QR Code standard ISO/IEC 18004:2015 appendix J
class Encoder: 
    CHAR_COUNT_INDICATOR = {
        MODE_NUMBER: [10, 12, 14],
        MODE_ALPHANUMERIC: [9, 11, 13],
        MODE_BYTE: [8, 16, 16],
        MODE_KANJI: [8, 10, 12]
    }

    def __init__(self):
        self._data = [] # data to be encoded
        self._mode = [] # mode of the data 
        self._character_count = [] # character count of the data

    def add_data(self, data : str, mode = None):
        if mode is None:
            self._mode.append(MODE_MIXED)
        else:
            self._mode.append(mode)
        self._data.append(data)

    def encode(self, version: int):
        encoded_data = ""
        for i in range(len(self._data)):
            # initial mode
            
            

    # def total_bits(self, version: int) -> int:
    #     total_bits = 0
    #     if version < 10:
    #         version_i = 0
    #     elif version < 27:
    #         version_i = 1
    #     else:
    #         version_i = 2

    #     for i in range(len(self._data)):
    #         total_bits += 4 + Encoder.CHAR_COUNT_INDICATOR[self._mode[i]][version_i]
    #         if self._mode[i] == MODE_NUMBER:
    #             if self._character_count[i] % 3 == 1:
    #                 total_bits += 4
    #             elif self._character_count[i] % 3 == 2:
    #                 total_bits += 7
    #             total_bits += (self._character_count[i] // 3) * 10
    #         elif self._mode[i] == MODE_ALPHANUMERIC:
    #             total_bits += (self._character_count[i] // 2) * 11 + (self._character_count[i] % 2) * 6
    #         elif self._mode[i] == MODE_BYTE:
    #             total_bits += self._character_count[i] * 8
    #         elif self._mode[i] == MODE_KANJI:
    #             total_bits += self._character_count[i] * 13
    #     return total_bits

    # def get_data_encoded(self, version: int):
    #     # TODO: test this
    #     data = ""
    #     for i in range(len(self._data)):
    #         data += f"{self._mode[i]:04b}" # add mode indicator
    #         data += f"{format(self._character_count[i], f'0{Encoder.CHAR_COUNT_INDICATOR[self._mode[i]][version]}b')}" # add character count indicator
    #         data += self._data[i] # add data
    #     return data

    # def _detect_mode(self, data : str):
    #     is_numeric = True
    #     is_alphanumeric = True
    #     for char in data:
    #         if not char.isdigit():
    #             is_numeric = False
    #         if char not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:":
    #             is_alphanumeric = False
    #         if not is_numeric and not is_alphanumeric:
    #             break
    #     if (is_numeric):
    #         return MODE_NUMBER
    #     elif (is_alphanumeric):
    #         return MODE_ALPHANUMERIC
    #     elif self._is_kanji_mode(data):
    #         return MODE_KANJI
    #     else:
    #         return MODE_BYTE

    # def _is_kanji_mode(self, data : str) -> bool:
    #     try:
    #         sjis_encoded = data.encode('shift-jis')
    #     except UnicodeEncodeError:
    #         return False
    #     i = 0
    #     while i < len(data):
    #         if sjis_encoded[i:i+1] == b' ':     
    #             i += 1
    #             continue
    #         code = (sjis_encoded[i] << 8) + sjis_encoded[i + 1] # combines two bytes into one
    #         if (0x8140 <= code <= 0x9FFC) or (0xE040 <= code <= 0xEBBF):
    #             i += 2
    #         else:
    #             return False # if the character is not a kanji character means the data is not in kanji mode
    #     return True

    # def _encode_numeric(self, data : str):
    #     encoded_data = ""
    #     for i in range(0, len(data), 3):
    #         chunk = data[i:i + 3]
    #         if len(chunk) == 3:
    #             encoded_data += f"{int(chunk):010b}"
    #         elif len(chunk) == 2:
    #             encoded_data += f"{int(chunk):07b}"
    #         else:
    #             encoded_data += f"{int(chunk):04b}"
    #     self._data.append(encoded_data)
    #     self._character_count.append(len(data))

    # def _encode_alphanumeric(self, data : str):
    #     ALPHANUMERIC_TABLE = {
    #         '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    #         'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
    #         'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
    #         'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36, '$': 37, '%': 38, '*': 39,
    #         '+': 40, '-': 41, '.': 42, '/': 43, ':': 44
    #     }
    #     encoded_data = ""
    #     for i in range(0, len(data), 2):
    #         chunk = data[i:i + 2]
    #         if len(chunk) == 2:
    #             encoded_data += f"{ALPHANUMERIC_TABLE[chunk[0]]*45 + ALPHANUMERIC_TABLE[chunk[1]]:011b}"
    #         elif len(chunk) == 1:
    #             encoded_data += f"{ALPHANUMERIC_TABLE[chunk]:06b}"
    #     self._data.append(encoded_data)
    #     self._character_count.append(len(data))

    # def _encode_byte(self, data : str):
    #     encoded_data = ""
    #     if self._is_latin1(data):
    #         encoded_data = ''.join(f'{ord(char):08b}' for char in data)
    #     else:
    #         encoded_data = ''.join(f'{byte:08b}' for byte in data.encode('utf-8'))
    #     self._data.append(encoded_data)
    #     self._character_count.append(int(len(encoded_data)/8))

    # def _is_latin1(self, char : str) -> bool:
    #     try:
    #         char.encode('latin-1')
    #     except UnicodeEncodeError:
    #         return False
    #     return True

    # def _encode_kanji(self, data : str) -> str:
    #     encoded_data = ""
    #     for char in data:
    #         sjis_encoded = char.encode('shift-jis')

    #         siji_value = (sjis_encoded[0] << 8) + sjis_encoded[1]
    #         if 0x8140 <= siji_value <= 0x9FFC:
    #             msb = sjis_encoded[0] - 0x81
    #             lsb = sjis_encoded[1] - 0x40
    #         elif 0xE040 <= siji_value <= 0xEBBF:
    #             msb = sjis_encoded[0] - 0xC1
    #             lsb = sjis_encoded[1] - 0x40
    #         else:
    #             raise ValueError(f"Invalid Shift-JIS value: {siji_value}")

    #         encoded_value  = (msb * 0xC0) + lsb
    #         encoded_data += f"{encoded_value:013b}"
    #     self._data.append(encoded_data)
    #     self._character_count.append(len(data))

    # def __str__(self) -> str:
    #     return f"Data: {self._data}, Mode: {self._mode}, Character Count: {self._character_count}"
