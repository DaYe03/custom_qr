from .constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, EC_CODEWORDS, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_L, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_H
from urllib.parse import urlparse
import math

class DataConverter:        
    def __init__(self, version = None, error_correction = ERROR_CORRECTION_LEVEL_L) -> None:
        self._buffer = ""
        self.version = version
        self.error_correction = error_correction
        self.VALUE_GEN_MAP = {
            MODE_NUMBER: self._encode_numeric,
            MODE_ALPHANUMERIC: self._encode_alphanumeric,
            MODE_BYTE: self._encode_byte,
            MODE_KANJI: self._encode_kanji
        }

    def encode(self, data: str):
        # detect mode 
        data, encoding_mode = self._detect_mode(data)

        # encode data
        data_generator = self.VALUE_GEN_MAP[encoding_mode]
        data_generator(data)

        # determine version if not provided and raise error if data is too long
        if self.version is None:
            count_codewords = math.ceil(len(self._buffer) / 8)
            for version in range(1, 41):
                if EC_CODEWORDS[version][self.error_correction][0] >= count_codewords:
                    self.version = version
                    break
            if self.version is None:
                raise ValueError("Data is too long")
        elif self.version > 40 or self.version < 1:
            raise ValueError("Invalid version number")
        elif math.ceil(len(self._buffer) / 8) > EC_CODEWORDS[self.version][self.error_correction][0]:
            raise ValueError("Data is too long")
               
        # add mode indicator and character count indicator
        CHAR_COUNT_INDICATOR = {
            MODE_NUMBER: [10, 12, 14],
            MODE_ALPHANUMERIC: [9, 11, 13],
            MODE_BYTE: [8, 16, 16],
            MODE_KANJI: [8, 10, 12]
        }
        if self.version < 10:
            length_bits =  CHAR_COUNT_INDICATOR[encoding_mode][0]
        elif self.version < 27:
            length_bits = CHAR_COUNT_INDICATOR[encoding_mode][1]
        else:
            length_bits = CHAR_COUNT_INDICATOR[encoding_mode][2]
        self._add_onhead_buffer(len(data), length_bits)
        self._add_onhead_buffer(encoding_mode, 4)

        # add terminator
        self._add_buffer(0, 4)

        # add filler
        byte = int(len(self._buffer) / 8)
        for i in range(EC_CODEWORDS[self.version][self.error_correction][0] - byte):
            self._add_buffer(0b11101100 if i % 2 == 0 else 0b00010001, 8)

        return [int(self._buffer[i:i+8], 2) for i in range(0, len(self._buffer), 8)]
    
    def get_total_data_codewords(self):
        return EC_CODEWORDS[self.version][self.error_correction][0]
    
    def get_total_codewords(self):
        return EC_CODEWORDS[self.version][self.error_correction][0] + EC_CODEWORDS[self.version][self.error_correction][1]*(EC_CODEWORDS[self.version][self.error_correction][2]+EC_CODEWORDS[self.version][self.error_correction][4])
    
    def get_ec_codewords_per_block(self):
        return EC_CODEWORDS[self.version][self.error_correction][1]

    def get_version(self):
        return self.version

    def _detect_mode(self, data):
        if (urlparse(data).scheme in ('http', 'https') and urlparse(data).netloc != ''):
            data = data.upper()

        is_numeric = all(char.isdigit() for char in data)
        is_alphanumeric = all(char in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:" for char in data)
        if is_numeric:
            return data, MODE_NUMBER
        elif is_alphanumeric:
            return data, MODE_ALPHANUMERIC
        elif self._is_kanji_mode(data):
            return data, MODE_KANJI
        else:
            return data, MODE_BYTE

    def _is_kanji_mode(self, data):
        try:
            sjis_encoded = data.encode('shift-jis')
        except UnicodeEncodeError:
            return False
        
        i = 0
        while i < len(sjis_encoded):
            if sjis_encoded[i:i+1] == b' ':     
                i += 1
                continue
            if i + 1 >= len(sjis_encoded):
                return False
            code = (sjis_encoded[i] << 8) + sjis_encoded[i + 1]
            if (0x8140 <= code <= 0x9FFC) or (0xE040 <= code <= 0xEBBF):
                i += 2
            else:
                return False
        return True
    
    def _add_buffer(self, value:int, bit_length:int):
        self._buffer += f"{value:0{bit_length}b}"

    def _add_onhead_buffer(self, value:int, bit_length:int):
        self._buffer = f"{value:0{bit_length}b}" + self._buffer

    def _encode_numeric(self, data):
        for i in range(0, len(data), 3):
            chunk = data[i:i+3]
            if len(chunk) == 3:
                self._add_buffer(int(chunk), 10)
            elif len(chunk) == 2:
                self._add_buffer(int(chunk), 7)
            else:
                self._add_buffer(int(chunk), 4)

    def _encode_alphanumeric(self, data):
        ALPHANUMERIC_TABLE = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
            'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
            'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36, '$': 37, '%': 38, '*': 39,
            '+': 40, '-': 41, '.': 42, '/': 43, ':': 44
        }
        for i in range(0, len(data), 2):
            chunk = data[i:i + 2]
            if len(chunk) == 2:
                self._add_buffer(ALPHANUMERIC_TABLE[chunk[0]]*45 + ALPHANUMERIC_TABLE[chunk[1]], 11)
            elif len(chunk) == 1:
                self._add_buffer(ALPHANUMERIC_TABLE[chunk], 6)

    def _encode_byte(self, data: str):
        if self._is_latin1(data):
            for char in data:
                self._add_buffer(ord(char), 8)
        else:
            for byte in data.encode('utf-8'):
                self._add_buffer(byte, 8)

    def _is_latin1(self, char : str) -> bool:
        try:
            char.encode('latin-1')
        except UnicodeEncodeError:
            return False
        return True 
    
    def _encode_kanji(self, data: str):
        for char in data:
            sjis_encoded = char.encode('shift-jis')

            siji_value = (sjis_encoded[0] << 8) + sjis_encoded[1]
            if 0x8140 <= siji_value <= 0x9FFC:
                msb = sjis_encoded[0] - 0x81
                lsb = sjis_encoded[1] - 0x40
            elif 0xE040 <= siji_value <= 0xEBBF:
                msb = sjis_encoded[0] - 0xC1
                lsb = sjis_encoded[1] - 0x40
            else:
                raise ValueError(f"Invalid Shift-JIS value: {siji_value}")

            self._add_buffer((msb * 0xC0) + lsb, 13)
