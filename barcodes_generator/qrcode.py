import numpy as np
from .constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, MODE_ECI, MODE_MIXED, ERROR_CORRECTION_LEVEL_L, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_H
from .errorCorrection import ErrorCorrection
from PIL import Image

class QrCode:
   
    def __init__(self, version=None, error_correction=ERROR_CORRECTION_LEVEL_L):
        self.version = version
        self.error_correction = error_correction

    def generate(self, phrase):
        # Encode the data
        mode = self.detect_mode_basic(phrase)
        length_bits = self.get_length_bits(mode, self.version)
        encoded_data = f"{mode:04b}{len(phrase):0{length_bits}b}"
        if mode == MODE_BYTE:
            encoded_data += self._encode_byte(phrase)
        encoded_data += "0000"  # terminal add at the end of all the data

        # Add padding bits
        byte = int((4 + length_bits + len(phrase) * 8 + 4) / 8)
        for i in range(28 - byte):
            encoded_data += "11101100" if i % 2 == 0 else "00010001"

        # Convert to bytes
        data = [int(encoded_data[i:i + 8], 2) for i in range(0, len(encoded_data), 8)]
        
        # Error correction
        n_blocks1 = 1
        n_blocks2 = 0
        n_data_codewords_block1 = 28
        n_data_codewords_block2 = 0
        ec_codewords_per_block = 16
        total_data_codewords = 44

        codewords = data + ErrorCorrection().getEDC(data, total_data_codewords)

        # TODO: precompute for all the versions (cache)
        module_sequence = self.generate_module_sequence()  # Generate the module sequence

        for mask_index in range(8):
            print("------------------------------------------------------")
            matrix = self.mask_matrix(mask_index, codewords, module_sequence)
            self.print_qr(matrix)
        
        self.create_qr_image(self.mask_matrix(2, codewords, module_sequence), filename='qr_code.png', module_size=10)


    # TODO: update to larger version
    def generate_module_sequence(self):
        matrix = np.zeros((self.get_size(), self.get_size()), dtype=int)
        size = self.get_size()
        
        # Fill fixed patterns and functional areas
        self.fill_area(matrix, 0, 0, 9, 9)  # Top-left finder pattern
        self.fill_area(matrix, 0, size - 8, 8, 9)  # Top-right finder pattern
        self.fill_area(matrix, size - 8, 0, 9, 8)  # Bottom-left finder pattern
        self.fill_area(matrix, size - 9, size - 9, 5, 5)  # Alignment pattern
        self.fill_area(matrix, 6, 9, self.version * 4, 1)  # Horizontal timing pattern
        self.fill_area(matrix, 9, 6, 1, self.version * 4)  # Vertical timing pattern
        
        # Dark module
        matrix[size - 8, 8] = 1
        
        row_step = -1
        row = size - 1
        column = size - 1
        sequence = []
        index = 0

        while column >= 0:
            if matrix[row, column] == 0:
                sequence.append((row, column))
            
            if index % 2 == 1:
                row += row_step
                if row == -1 or row == size:
                    row_step = -row_step
                    row += row_step
                    column -= 2 if column == 7 else 1
                else:
                    column += 1
            else:
                column -= 1
            
            index += 1
        return sequence
    


    def mask_matrix(self, mask_index, codewords, module_sequence):
        matrix = self.get_masked_matrix(mask_index, codewords, module_sequence)
        self.place_format_information(matrix, mask_index)
        self.place_fixed_patterns(matrix)
        return matrix

    def get_masked_matrix(self, mask_index, codewords, module_sequence):
        MASK_FNS = [
            lambda row, column: ((row + column) & 1) == 0,
            lambda row, column: (row & 1) == 0,
            lambda row, column: column % 3 == 0,
            lambda row, column: (row + column) % 3 == 0,
            lambda row, column: (((row >> 1) + column // 3) & 1) == 0,
            lambda row, column: ((row * column) & 1) + ((row * column) % 3) == 0,
            lambda row, column: ((((row * column) & 1) + ((row * column) % 3)) & 1) == 0,
            lambda row, column: ((((row + column) & 1) + ((row * column) % 3)) & 1) == 0,
        ]
        mask_fn = MASK_FNS[mask_index]
        matrix = np.zeros((self.get_size(), self.get_size()), dtype=int)
        for index, (row, column) in enumerate(module_sequence):
            if index >> 3 >= len(codewords):
                break
            # Each codeword contains 8 modules, so shifting the index to the right by 3 gives the codeword's index
            codeword = codewords[index >> 3]
            bit_shift = 7 - (index & 7)
            module_bit = (codeword >> bit_shift) & 1
            # Apply the mask function to the module bit
            matrix[row][column] = module_bit ^ int(mask_fn(row, column))
        return matrix
    

    def place_format_information(self, matrix, mask_index):
        size = len(matrix)
        format_modules = self.get_format_modules(mask_index)
        # Top-left
        matrix[8, :6] = format_modules[:6]
        matrix[8, 7:9] = format_modules[6:8]
        matrix[8, -8:] = format_modules[7:]
        matrix[7, 8] = format_modules[8]
        # Bottom-left
        for index in range(7):
            matrix[size - index - 1, 8] = format_modules[index]
        # Top-right
        for index in range(6):
            matrix[5 - index, 8] = format_modules[9 + index]

    def get_format_modules(self, mask_index):
        FORMAT_DIVISOR = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1], dtype=int)
        FORMAT_MASK = np.array([1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], dtype=int)
        format_poly = np.zeros(15, dtype=int)
        if self.error_correction == ERROR_CORRECTION_LEVEL_L:
            error_index = 1
        elif self.error_correction == ERROR_CORRECTION_LEVEL_M:
            error_index = 0
        elif self.error_correction == ERROR_CORRECTION_LEVEL_Q:
            error_index = 3
        elif self.error_correction == ERROR_CORRECTION_LEVEL_H:
            error_index = 2
        format_poly[0] = error_index >> 1
        format_poly[1] = error_index & 1
        format_poly[2] = mask_index >> 2
        format_poly[3] = (mask_index >> 1) & 1
        format_poly[4] = mask_index & 1
        rest = ErrorCorrection().poly_rest(format_poly, FORMAT_DIVISOR)
        format_poly[5:] = rest
        masked_format_poly = np.bitwise_xor(format_poly, FORMAT_MASK)
        return masked_format_poly.tolist()

    def place_fixed_patterns(self, matrix):
        size = len(matrix)

        # Finder patterns
        for row, col in [(0, 0), (size - 7, 0), (0, size - 7)]:
            self.fill_area(matrix, row, col, 7, 7)
            self.fill_area(matrix, row + 1, col + 1, 5, 5, fill=0)
            self.fill_area(matrix, row + 2, col + 2, 3, 3)

        # Separators
        self.fill_area(matrix, 7, 0, 8, 1, fill=0)
        self.fill_area(matrix, 0, 7, 1, 7, fill=0)
        self.fill_area(matrix, size - 8, 0, 8, 1, fill=0)
        self.fill_area(matrix, 0, size - 8, 1, 7, fill=0)
        self.fill_area(matrix, 7, size - 8, 8, 1, fill=0)
        self.fill_area(matrix, size - 7, 7, 1, 7, fill=0)

        # Alignment pattern
        self.fill_area(matrix, size - 9, size - 9, 5, 5)
        self.fill_area(matrix, size - 8, size - 8, 3, 3, fill=0)
        matrix[size - 7][size - 7] = 1

        # Timing patterns
        for pos in range(8, size - 8, 2):
            matrix[6, pos] = 1
            matrix[6, pos + 1] = 0
            matrix[pos, 6] = 1
            matrix[pos + 1, 6] = 0
        matrix[6, size - 7] = 1
        matrix[size - 7, 6] = 1

        # Dark module
        matrix[size - 8, 8] = 1

    def get_size(self):
        return self.version * 4 + 17
    
    def fill_area(self, matrix ,row, column, width, height, fill=1):
        fill_row = [fill] * width
        matrix[row:row + height, column:column + width] = fill_row

    def detect_mode_basic(self, phrase):
        is_numeric = True
        is_alphanumeric = True
        for char in phrase:
            if not char.isdigit():
                is_numeric = False
            if char not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:":
                is_alphanumeric = False
            if not is_numeric and not is_alphanumeric:
                break
        if is_numeric:
            return MODE_NUMBER
        elif is_alphanumeric:
            return MODE_ALPHANUMERIC
        elif self.is_kanji_mode(phrase):
            return MODE_KANJI
        else:
            return MODE_BYTE

    def is_kanji_mode(self, phrase):
        try:
            sjis_encoded = phrase.encode('shift-jis')
        except UnicodeEncodeError:
            return False
        i = 0
        while i < len(sjis_encoded):
            if sjis_encoded[i:i+1] == b' ':     
                i += 1
                continue
            code = (sjis_encoded[i] << 8) + sjis_encoded[i + 1] # combines two bytes into one
            if (0x8140 <= code <= 0x9FFC) or (0xE040 <= code <= 0xEBBF):
                i += 2
            else:
                return False # if the character is not a kanji character means the data is not in kanji mode
        return True 

    def get_length_bits(self, mode, version):
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

    def _encode_byte(self, phrase):
        return ''.join(f"{ord(char):08b}" for char in phrase)
    
    def print_qr(self, matrix):
        # char_on = '█'  # Or you can use '1'
        char_on = '#'
        char_off = ' ' # Or you can use '0'
        for row in matrix:
            row_str = ''.join(char_on if cell == 1 else char_off for cell in row)
            print(row_str)
        print()

    def create_qr_image(self,matrix, filename='qr_code.png', module_size=10):
        """
        Create an image from the QR code matrix and save it to a file.

        :param matrix: 2D list or numpy array representing the QR code matrix.
        :param filename: Name of the file to save the image as.
        :param module_size: Size of each module (pixel) in the image.
        """
        size = len(matrix)
        # Create a new image with white background
        img = Image.new('1', (size * module_size, size * module_size), color=1)  # '1' for 1-bit pixels, black and white

        # Get the pixel map of the image
        pixels = img.load()

        for y in range(size):
            for x in range(size):
                color = 0 if matrix[y][x] == 1 else 1  # Black if module is 1, white if module is 0
                for i in range(module_size):
                    for j in range(module_size):
                        pixels[x * module_size + i, y * module_size + j] = color

        # Save the image
        img.save(filename)