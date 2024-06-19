import pytest
from barcodes_generator.constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, ERROR_CORRECTION_LEVEL_H, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_L
from barcodes_generator import QRCode, Encoder

def test_detect():
    en = Encoder()
    detected_mode = en._detect_mode("1234567890")
    assert detected_mode == MODE_NUMBER, f"Expected MODE_NUMBER ({MODE_NUMBER}) but got {detected_mode}"

    en = Encoder()
    detected_mode = en._detect_mode("HELLO WORLD 1234567890 $%*+-./:")
    assert detected_mode == MODE_ALPHANUMERIC, f"Expected MODE_ALPHANUMERIC ({MODE_ALPHANUMERIC}) but got {detected_mode}"

    en = Encoder()
    detected_mode = en._detect_mode("漢字ひ らがカタ カナ!")
    assert detected_mode == MODE_KANJI, f"Expected MODE_KANJI ({MODE_KANJI}) but got {detected_mode}"

    en = Encoder()
    detected_mode = en._detect_mode("Hello, 世界 !")
    assert detected_mode == MODE_BYTE, f"Expected MODE_BYTE ({MODE_BYTE}) but got {detected_mode}"

def test_encode():
    en = Encoder()
    
    # Test con dati numerici
    numeric_data = "01234567"
    en.add_data(numeric_data)
    expected_output = "Data: ['000000110001010110011000011'], Mode: [1], Character Count: [8]"
    assert str(en) == expected_output

    # Test con dati alfanumerici
    en = Encoder()
    alphanumeric_data = "AC-42"
    en.add_data(alphanumeric_data)
    expected_output = "Data: ['0011100111011100111001000010'], Mode: [2], Character Count: [5]"
    assert str(en) == expected_output

    # Test con dati UTF-8
    en = Encoder()
    utf_byte_data = "Hello, 世界 !"
    en.add_data(utf_byte_data)
    expected_output = "Data: ['010010000110010101101100011011000110111100101100001000001110010010111000100101101110011110010101100011000010000000100001'], Mode: [4], Character Count: [15]"
    assert str(en) == expected_output

    # Test con dati Latin-1
    en = Encoder()
    latin1_byte_data = "Hello, World!"
    en.add_data(latin1_byte_data)
    expected_output = "Data: ['01001000011001010110110001101100011011110010110000100000010101110110111101110010011011000110010000100001'], Mode: [4], Character Count: [13]"
    assert str(en) == expected_output

    # Test con dati Kanji
    en = Encoder()
    kanji_data = "点茗"
    en.add_data(kanji_data)
    expected_output = "Data: ['01101100111111101010101010'], Mode: [8], Character Count: [2]"
    assert str(en) == expected_output

def test_module_size():
    qr = QRCode()
    assert qr.total_module_by_version(40) == 177*177, f"Expected {177*177} but got {qr.total_module_by_version(40)}"
    assert qr.total_functional_module_by_version(40) == 1614, f"Expected 1614 but got {qr.total_functional_module_by_version(40)}"
    assert qr.total_format_version_module_by_version(40) == 67, f"Expected 67 but got {qr.total_format_version_module_by_version(40)}"
    assert qr.total_data_module_by_version(40) == 177*177 - 1614 - 67, f"Expected {177*177 - 1614 - 67} but got {qr.total_data_module_by_version(40)}"

def test_total_bits():
    en = Encoder()
    en.add_data("12345")
    assert en.total_bits(1) == 14+10+7

    en = Encoder()
    en.add_data("HELLO")
    assert en.total_bits(1) == 13+22+6
    
    en = Encoder()
    en.add_data("H世")
    assert en.total_bits(1) == 12 + 32

    en = Encoder()
    en.add_data("Hello")
    assert en.total_bits(1) == 12 + 40

    en = Encoder()
    kanji_data = "点茗"
    en.add_data(kanji_data)
    assert en.total_bits(1) == 12+26

    