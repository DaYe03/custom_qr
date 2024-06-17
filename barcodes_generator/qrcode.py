from .constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, MODE_ECI, ERROR_CORRECTION_LEVEL_L, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_H

import re

class QRCode:
    CHAR_COUNT_INDICATOR = {
        MODE_NUMBER: [10, 12, 14],
        MODE_ALPHANUMERIC: [9, 11, 13],
        MODE_BYTE: [8, 16, 16],
        MODE_KANJI: [8, 10, 12]
    }

    CAPACITY_TABLE = {
        MODE_NUMBER: {
            ERROR_CORRECTION_LEVEL_L: [41, 77, 127, 187, 255, 322, 370, 461, 552, 652, 772, 883, 1022, 1101, 1250, 1408, 1548, 1725, 1903, 2061, 2232, 2409, 2620, 2812, 3057],
            ERROR_CORRECTION_LEVEL_M: [34, 63, 101, 149, 202, 255, 293, 365, 432, 513, 604, 691, 796, 871, 991, 1082, 1212, 1346, 1500, 1600, 1708, 1872, 2059, 2188, 2395],
            ERROR_CORRECTION_LEVEL_Q: [27, 48, 77, 111, 144, 178, 207, 259, 312, 364, 427, 489, 580, 621, 703, 775, 876, 948, 1063, 1159, 1224, 1358, 1468, 1588, 1718],
            ERROR_CORRECTION_LEVEL_H: [17, 34, 58, 82, 106, 139, 154, 202, 235, 288, 331, 374, 427, 468, 530, 602, 674, 746, 813, 919, 969, 1056, 1108, 1228, 1286]
        },
        MODE_ALPHANUMERIC: {
            ERROR_CORRECTION_LEVEL_L: [25, 47, 77, 114, 154, 195, 224, 279, 335, 395, 468, 535, 619, 667, 758, 854, 938, 1046, 1153, 1249, 1352, 1460, 1588, 1704, 1853],
            ERROR_CORRECTION_LEVEL_M: [20, 38, 61, 90, 122, 154, 178, 221, 262, 311, 366, 419, 483, 528, 600, 656, 734, 816, 909, 970, 1035, 1134, 1248, 1326, 1451],
            ERROR_CORRECTION_LEVEL_Q: [16, 29, 47, 67, 87, 108, 125, 157, 189, 221, 259, 296, 352, 376, 426, 470, 531, 574, 644, 702, 742, 823, 890, 963, 1041],
            ERROR_CORRECTION_LEVEL_H: [10, 20, 35, 50, 64, 84, 93, 122, 143, 174, 200, 227, 259, 283, 321, 365, 408, 452, 493, 557, 587, 640, 672, 744, 779]
        },
        MODE_BYTE: {
            ERROR_CORRECTION_LEVEL_L: [17, 32, 53, 78, 106, 134, 154, 192, 230, 271, 321, 367, 425, 458, 520, 586, 644, 718, 792, 858, 929, 1003, 1091, 1171, 1273],
            ERROR_CORRECTION_LEVEL_M: [14, 26, 42, 62, 84, 106, 122, 152, 180, 213, 251, 287, 331, 362, 412, 450, 504, 560, 624, 666, 711, 779, 857, 911, 997],
            ERROR_CORRECTION_LEVEL_Q: [11, 20, 32, 46, 60, 74, 86, 108, 130, 151, 177, 203, 241, 258, 292, 322, 364, 394, 442, 482, 509, 565, 611, 661, 715],
            ERROR_CORRECTION_LEVEL_H: [7, 14, 24, 34, 44, 58, 64, 84, 98, 119, 137, 155, 177, 194, 220, 250, 280, 310, 338, 382, 403, 439, 461, 511, 535]
        },
        MODE_KANJI: {
            ERROR_CORRECTION_LEVEL_L: [10, 20, 32, 48, 65, 82, 95, 118, 141, 167, 198, 226, 262, 282, 320, 361, 397, 442, 488, 528, 572, 618, 672, 721, 784],
            ERROR_CORRECTION_LEVEL_M: [8, 16, 26, 38, 52, 65, 75, 93, 111, 131, 155, 177, 204, 223, 254, 277, 310, 345, 384, 410, 438, 480, 528, 572, 618],
            ERROR_CORRECTION_LEVEL_Q: [7, 12, 20, 28, 37, 45, 53, 66, 80, 93, 109, 125, 149, 159, 180, 198, 224, 243, 272, 297, 314, 348, 376, 408, 442],
            ERROR_CORRECTION_LEVEL_H: [4, 8, 15, 21, 27, 36, 39, 52, 60, 74, 85, 96, 109, 120, 136, 154, 173, 191, 208, 235, 248, 270, 284, 315, 331]
        }
    }

    ALPHANUMERIC_TABLE = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
        'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
        'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36, '$': 37, '%': 38, '*': 39,
        '+': 40, '-': 41, '.': 42, '/': 43, ':': 44
    }

    def make (self, data : str, version = None, error_correction = ERROR_CORRECTION_LEVEL_H):
        encoded_data = self._encodeData(data, self._encode_data(data), self.version if self.version is not None else self._select_version(data, self._detect_mode(data)))
    
    def _get_minimum_version(self, data : str, mode, error_correction):
        for version in range(1, 41):
            if self.CAPACITY_TABLE[mode][error_correction][version - 1] >= len(data):
                return version
        raise ValueError("Data too long to fit in any version")

    def _encode_data(self, data : str, mode, version):
        if version is not None:
            if version < 10:
                i_char_count = 0
            elif version < 27:
                i_char_count = 1
            else:
                i_char_count = 2
        encoded_data = ""
        if mode == MODE_NUMBER:
            encoded_data = f"{MODE_NUMBER:04b}{len(data):0{self.CHAR_COUNT_INDICATOR[MODE_NUMBER][i_char_count]}b}{self._encode_numeric(data)}"
        elif mode == MODE_ALPHANUMERIC:
            # char_count = 4 + self.CHAR_COUNT_INDICATOR[MODE_ALPHANUMERIC][i_char_count] + 11 * (len(data) // 2) + 6 * (len(data) % 2)
            encoded_data = f"{MODE_ALPHANUMERIC:04b}{len(data):0{self.CHAR_COUNT_INDICATOR[MODE_ALPHANUMERIC][i_char_count]}b}{self._encode_alphanumeric(data)}"
        elif mode == MODE_BYTE:
            encoded_data = f"{MODE_BYTE:04b}{len(data):08b}{self._encode_byte(data)}"
        return encoded_data
    
    def _encode_numeric(self, data : str):
        encoded_data = ""
        for i in range(0, len(data), 3):
            chunk = data[i:i + 3]
            if len(chunk) == 3:
                encoded_data += f"{int(chunk):010b}"
            elif len(chunk) == 2:
                encoded_data += f"{int(chunk):07b}"
            else:
                encoded_data += f"{int(chunk):04b}"
        return encoded_data
    
    def _encode_alphanumeric(self, data : str):
        encoded_data = ""
        for i in range(0, len(data), 2):
            chunk = data[i:i + 2]
            if len(chunk) == 2:
                encoded_data = encoded_data + f"{self.ALPHANUMERIC_TABLE[chunk[0]]*45 + self.ALPHANUMERIC_TABLE[chunk[1]]:011b}" 
            elif len(chunk) == 1:
                encoded_data = encoded_data + f"{self.ALPHANUMERIC_TABLE[chunk]:06b}" 
        return encoded_data
    
    def _detect_mode(self, data : str):
        is_numeric = True
        is_alphanumeric = True
        for char in data:
            if not char.isdigit():
                is_numeric = False
            if char not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:":
                is_alphanumeric = False
            if not is_numeric and not is_alphanumeric:
                break
        if (is_numeric):
            return MODE_NUMBER
        elif (is_alphanumeric):
            return MODE_ALPHANUMERIC
        elif self._is_kanji_mode(data):
            return MODE_KANJI
        else:
            return MODE_BYTE
        
    def _is_kanji_mode(self, data : str) -> bool:
        try:
            sjis_encoded = data.encode('shift-jis')
        except UnicodeEncodeError:
            return False
        i = 0
        while i < len(data):
            if sjis_encoded[i:i+1] == b' ':     
                i += 1
                continue
            code = (sjis_encoded[i] << 8) + sjis_encoded[i + 1] # combines two bytes into one
            if (0x8140 <= code <= 0x9FFC) or (0xE040 <= code <= 0xEBBF):
                i += 2
            else:
                return False # if the character is not a kanji character means the data is not in kanji mode
        return True
