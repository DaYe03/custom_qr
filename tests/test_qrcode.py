import pytest
from barcodes_generator.constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, ERROR_CORRECTION_LEVEL_H, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_L
from barcodes_generator import QRCode

def test_detect_mode_numeric():
    qr = QRCode()
    numeric_data = "1234567890"
    detected_mode = qr._detect_mode(numeric_data)
    assert detected_mode == MODE_NUMBER, f"Expected MODE_NUMBER ({MODE_NUMBER}) but got {detected_mode}"

def test_detect_mode_alphanumeric():
    qr = QRCode()
    alphanumeric_data = "HELLO WORLD 1234567890 $%*+-./:"
    detected_mode = qr._detect_mode(alphanumeric_data)
    assert detected_mode == MODE_ALPHANUMERIC, f"Expected MODE_ALPHANUMERIC ({MODE_ALPHANUMERIC}) but got {detected_mode}"

def test_detect_mode_kanji():
    qr = QRCode()
    kanji_data = "漢字ひ らがカタ カナ!"
    detected_mode = qr._detect_mode(kanji_data)
    assert detected_mode == MODE_KANJI, f"Expected MODE_KANJI ({MODE_KANJI}) but got {detected_mode}"

    qr = QRCode()
    byte_data = "Hello, 世界 !"
    detected_mode = qr._detect_mode(byte_data)
    assert detected_mode == MODE_BYTE, f"Expected MODE_BYTE ({MODE_BYTE}) but got {detected_mode}"

def test_get_minimum_version():
    qr = QRCode()
    data = "HELLO WORLD 1234567890 $%*+-./:"
    mode = MODE_ALPHANUMERIC
    version = qr._get_minimum_version(data, mode, ERROR_CORRECTION_LEVEL_L)
    assert version == 2, f"Expected version 2 but got {version}"
    version = qr._get_minimum_version(data, mode, ERROR_CORRECTION_LEVEL_M)
    assert version == 2, f"Expected version 2 but got {version}"
    version = qr._get_minimum_version(data, mode, ERROR_CORRECTION_LEVEL_Q)
    assert version == 3, f"Expected version 3 but got {version}"
    version = qr._get_minimum_version(data, mode, ERROR_CORRECTION_LEVEL_H)
    assert version == 3, f"Expected version 3 but got {version}"

def test_encode_numeric():
    qr = QRCode()
    numeric_data = "01234567"
    encoded_data = qr._encode_numeric(numeric_data)
    assert encoded_data == "000000110001010110011000011", f"Expected '000000110001010110011000011' but got {encoded_data}"

def test_encode_alphanumeric():
    qr = QRCode()
    alphanumeric_data = "AC-42"
    encoded_data = qr._encode_alphanumeric(alphanumeric_data)
    assert encoded_data == "0011100111011100111001000010", f"Expected '0011100111011100111001000010' but got {encoded_data}"

def test_encode_data():
    qr = QRCode()
    encoded_data = qr._encode_data("01234567", MODE_NUMBER, 1)
    assert encoded_data == "00010000001000000000110001010110011000011", f"Expected '00010000001000000000110001010110011000011' but got {encoded_data}"
    encoded_data = qr._encode_data("AC-42", MODE_ALPHANUMERIC, 1)
    assert encoded_data == "00100000001010011100111011100111001000010", f"Expected '00100000001010011100111011100111001000010' but got {encoded_data}"
