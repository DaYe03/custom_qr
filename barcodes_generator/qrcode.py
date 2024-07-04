MODE_NUMBER = 1
MODE_ALPHANUMERIC = 2
MODE_BYTE = 4
MODE_KANJI = 8
MODE_ECI = 7
MODE_MIXED = 0

ERROR_CORRECTION_LEVEL_L = 1
ERROR_CORRECTION_LEVEL_M = 2
ERROR_CORRECTION_LEVEL_Q = 3
ERROR_CORRECTION_LEVEL_H = 4

def binary_to_decimal(binary_string):
    # Controlla se la lunghezza della stringa è multipla di 8
    if len(binary_string) % 8 != 0:
        raise ValueError("La lunghezza della stringa binaria deve essere multipla di 8")
    
    # Inizializza una lista vuota per i gruppi di bit
    groups_of_8 = []
    
    # Loop attraverso la stringa binaria in gruppi di 8 bit
    for i in range(0, len(binary_string), 8):
        # Estrai il gruppo di 8 bit
        eight_bits = binary_string[i:i+8]
        # Converti il gruppo di 8 bit da binario a decimale
        decimal_value = int(eight_bits, 2)
        # Aggiungi il valore decimale alla lista dei gruppi
        groups_of_8.append(str(decimal_value))
    
    # Unisci tutti i gruppi decimali separati da spazi
    decimal_string = ' '.join(groups_of_8)
    
    return decimal_string

def main():
    encoded_data = ""
    phrase = "https://www.qrcode.com/"
    version = 2
    correction = ERROR_CORRECTION_LEVEL_M
    mode = detect_mode_basic(phrase)
    lenght_bits = get_lenght_bits(mode, version)
    encoded_data += f"{mode:04b}{len(phrase):0{lenght_bits}b}"
    if mode == MODE_BYTE:
        encoded_data += _encode_byte(phrase)
    encoded_data += "0000" # terminator
    
    #ci vogliono 28 data codewords per la versione 2
    byte = int((4 + lenght_bits + len(phrase) * 8 + 4) / 8)
    for i in range(28 - byte):
        encoded_data += "11101100" if i % 2 == 0 else "00010001"

    print(binary_to_decimal(encoded_data))
    print(encoded_data)


def detect_mode_basic(data):
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
    elif is_kanji_mode(data):
        return MODE_KANJI
    else:
        return MODE_BYTE

def is_kanji_mode(data : str) -> bool:
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

def get_lenght_bits(mode, version):
    CHAR_COUNT_INDICATOR = {
        MODE_NUMBER: [10, 12, 14],
        MODE_ALPHANUMERIC: [9, 11, 13],
        MODE_BYTE: [8, 16, 16],
        MODE_KANJI: [8, 10, 12]
    }
    if version < 10:
        return CHAR_COUNT_INDICATOR[mode][0]
    elif version < 27:
        return CHAR_COUNT_INDICATOR[mode][1]
    else:
        return CHAR_COUNT_INDICATOR[mode][2]
    
def _encode_byte(data : str):
    #if self._is_latin1(data):
    #    encoded_data = ''.join(f'{ord(char):08b}' for char in data)
    #else:
    #    encoded_data = ''.join(f'{byte:08b}' for byte in data.encode('utf-8'))
    encoded_data = ''.join(f'{ord(char):08b}' for char in data)
    return encoded_data


if __name__ == "__main__":
    main()