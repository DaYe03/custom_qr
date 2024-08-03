from barcodes_generator.constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, ERROR_CORRECTION_LEVEL_M
from barcodes_generator.qrcode import QrCode
from barcodes_generator.dataConverter import DataConverter

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
    qr = QrCode(version=2, error_correction=ERROR_CORRECTION_LEVEL_M)
    qr.generate("https://www.qrcode.com/")

    # dataConverter = DataConverter(error_correction=ERROR_CORRECTION_LEVEL_M)
    # encoded_data = dataConverter.encode("https://www.qrcode.com/")
    # print(encoded_data)
    # print(encoded_data)


if __name__ == "__main__":
    main()