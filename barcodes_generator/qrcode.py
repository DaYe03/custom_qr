import numpy as np
from .constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, MODE_ECI, MODE_MIXED, ERROR_CORRECTION_LEVEL_L, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_H, EC_CODEWORDS
from .errorCorrection import ErrorCorrection
from .dataConverter import DataConverter
from PIL import Image

class QrCode:

    def __init__(self, version=None, error_correction=ERROR_CORRECTION_LEVEL_L):
        """
        Initialize the QR code object.

        :param version: Version of the QR code (1 to 40). If none, the version will be automatically selected.
        :type version: int, optional
        :param error_correction: Error correction level. Default is 'L'.
        :type error_correction: str, optional
        """
        self.version = version
        self.error_correction = error_correction
        self._codewords = None
        self._module_sequence = None
        self._matrix = None

    def generate(self, phrase):
        dataConverter = DataConverter(version= self.version, error_correction=self.error_correction)
        data_codewords = dataConverter.encode(phrase) # Encode the data
        self.version = dataConverter.get_version() # If the version was not provided, it will be set here
        # TODO: precompute for all the versions (cache) module sequence
        self._module_sequence = self._generate_module_sequence()  # Generate the module sequence after the version is set

        self._codewords = data_codewords + ErrorCorrection().getEDC(data_codewords, dataConverter.get_total_codewords()) # Add error correction codewords

        self._elaborate_codewords(data_codewords)

        self.get_optimal_mask() # Get the optimal mask for the QR code

    def get_matrix(self):
        return self._matrix
    
    def print_qr(self, matrix=None):
        # char_on = '█'  # Or you can use '1'
        char_on = '#'
        char_off = ' ' # Or you can use '0'
        for row in matrix:
            row_str = ''.join(char_on if cell == 1 else char_off for cell in row)
            print(row_str)
        print()

    def create_qr_image(self, filename='qr_code.png', module_size=10):
        """
        Create an image from the QR code matrix and save it to a file.

        :param matrix: 2D list or numpy array representing the QR code matrix.
        :param filename: Name of the file to save the image as.
        :param module_size: Size of each module (pixel) in the image.
        """
        size = len(self._matrix)
        # Create a new image with white background
        img = Image.new('1', (size * module_size, size * module_size), color=1)  # '1' for 1-bit pixels, black and white

        # Get the pixel map of the image
        pixels = img.load()

        for y in range(size):
            for x in range(size):
                color = 0 if self._matrix[y][x] == 1 else 1  # Black if module is 1, white if module is 0
                for i in range(module_size):
                    for j in range(module_size):
                        pixels[x * module_size + i, y * module_size + j] = color

        # Save the image
        img.save(filename)

    def _generate_module_sequence(self):
        size = self.get_size()
        matrix = np.zeros((size, size), dtype=int)
        
        # Fill fixed patterns and functional areas
        self._fill_area(matrix, 0, 0, 9, 9)  # Top-left finder pattern
        self._fill_area(matrix, 0, size - 8, 8, 9)  # Top-right finder pattern
        self._fill_area(matrix, size - 8, 0, 9, 8)  # Bottom-left finder pattern

        alignment_tracks = self._get_alignment_coordinates()
        last_track = len(alignment_tracks) - 1

        for row_index, row in enumerate(alignment_tracks):
            for column_index, column in enumerate(alignment_tracks):
                # Skipping the alignment near the finder patterns
                if (row_index == 0 and (column_index == 0 or column_index == last_track)) or \
                    (column_index == 0 and row_index == last_track):
                    continue
                
                # Fill area with the alignment pattern
                self._fill_area(matrix, row - 2, column - 2, 5, 5)

        # self._fill_area(matrix, size - 9, size - 9, 5, 5)  # Alignment pattern

        self._fill_area(matrix, 6, 9, self.version * 4, 1)  # Horizontal timing pattern
        self._fill_area(matrix, 9, 6, 1, self.version * 4)  # Vertical timing pattern
        
        # Dark module
        matrix[size - 8, 8] = 1

        # Version information
        if self.version >= 7:
            self._fill_area(matrix, 0,size - 11, 3, 6)
            self._fill_area(matrix, size - 11, 0, 6, 3)

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

    def _get_alignment_coordinates(self):
        if self.version == 1:
            return []

        intervals = self.version // 7 + 1
        distance = 4 * self.version + 4
        step = -(-distance // (intervals * 2)) * 2  

        return [6] + [distance + 6 - (intervals - 1 - index) * step for index in range(intervals)]
   
    def get_size(self):
        return self.version * 4 + 17

    def _elaborate_codewords(self, data_codewords):
        # 0 = total codewords, 1 = EC codewords per block, 2 = number of blocks in group 1, 3 = number of codewords in group 1, 4 = number of blocks in group 2, 5 = number of codewords in group 2
        table = EC_CODEWORDS[self.version][self.error_correction] 
        # split the data into blocks and elaborate the error correction for each block
        blocks = []
        ec_blocks = []
        codewords = []

        for i in range(table[2] + table[4]):
            if i < table[2]:
                block_size = table[3]
            else:
                block_size = table[5]
            blocks.append(data_codewords[:block_size])
            data_codewords = data_codewords[block_size:]
            ec_blocks.append(ErrorCorrection().getEDC(blocks[i], block_size+table[1]))

        # interleaving data and error correction codewords
        for c in range(table[3]):
            for j in range(table[2] + table[4]):
                codewords.append(blocks[j][c])
        for j in range(table[2], table[2] + table[4]):
            codewords.append(blocks[j][table[5] - 1])

        for c in range(table[1]):
            for j in range(table[2]+table[4]):
                codewords.append(ec_blocks[j][c])
        
        self._codewords = codewords

    def get_optimal_mask(self):
        best_matrix = None
        best_score = float('inf')
        for index in range(8):
            matrix = self._mask_matrix(index)
            penalty_score = self._get_penalty_score(matrix)
            if penalty_score < best_score:
                best_score = penalty_score
                best_matrix = matrix
                
        self._matrix = best_matrix
    
    def _mask_matrix(self, mask_index):
        matrix = self._get_masked_matrix(mask_index)
        self._place_format_information(matrix, mask_index)
        self._place_fixed_patterns(matrix)
        self._place_version_information(matrix)
        return matrix
    
    def _get_masked_matrix(self, mask_index):
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
        for index, (row, column) in enumerate(self._module_sequence):
            if index >> 3 >= len(self._codewords):
                break
            # Each codeword contains 8 modules, so shifting the index to the right by 3 gives the codeword's index
            codeword = self._codewords[index >> 3]
            bit_shift = 7 - (index & 7)
            module_bit = (codeword >> bit_shift) & 1
            # Apply the mask function to the module bit
            matrix[row][column] = module_bit ^ int(mask_fn(row, column))
        return matrix

    def _get_penalty_score(self, matrix):
        RULE_3_PATTERN = np.array([1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0], dtype=np.uint8)
        RULE_3_REVERSED_PATTERN = RULE_3_PATTERN[::-1]
        total_penalty = 0
        
        # Rule 1
        row_penalty = sum(self._get_line_penalty(row) for row in matrix)
        total_penalty += row_penalty
        
        column_penalty = sum(self._get_line_penalty(matrix[:, column_index]) for column_index in range(matrix.shape[1]))
        total_penalty += column_penalty
        
        # Rule 2
        blocks = 0
        size = matrix.shape[0]
        for row in range(size - 1):
            for column in range(size - 1):
                module = matrix[row, column]
                if (matrix[row, column + 1] == module and
                    matrix[row + 1, column] == module and
                    matrix[row + 1, column + 1] == module):
                    blocks += 1
        total_penalty += blocks * 3
        
        # Rule 3
        patterns = 0
        for index in range(size):
            row = matrix[index]
            for column_index in range(size - 11):
                if any(np.array_equal(pattern, row[column_index:column_index + 11]) for pattern in [RULE_3_PATTERN, RULE_3_REVERSED_PATTERN]):
                    patterns += 1
                    
            for row_index in range(size - 11):
                if any(np.array_equal(pattern, matrix[row_index:row_index + 11, index]) for pattern in [RULE_3_PATTERN, RULE_3_REVERSED_PATTERN]):
                    patterns += 1
        total_penalty += patterns * 40
        
        # Rule 4
        total_modules = size * size
        dark_modules = np.sum(matrix)
        percentage = dark_modules * 100 / total_modules
        mix_penalty = abs(int(percentage / 5 - 10)) * 10
        
        return total_penalty + mix_penalty

    def _get_line_penalty(self,line):
        count = 0
        counting = None
        penalty = 0
        
        for cell in line:
            if cell != counting:
                counting = cell
                count = 1
            else:
                count += 1
                if count == 5:
                    penalty += 3
                elif count > 5:
                    penalty += 1
                    
        return penalty

    def _place_format_information(self, matrix, mask_index):
        size = len(matrix)
        format_modules = self._get_format_modules(mask_index)
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

    def _place_version_information(self, matrix):
        size = len(matrix)

        if self.version < 7:
            return

        version_info = self._get_version_information()

        for index, bit in enumerate(version_info):
            row = index // 3
            col = index % 3
            
            # Update matrix at specific positions
            matrix[5 - row][size - 9 - col] = bit
            matrix[size - 11 + col][row] = bit

    def _get_version_information(self):
        VERSION_DIVISOR = [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1]
        version_bin_str = format(self.version, '06b') + '000000000000'
        # version_bin_str = format(26, '06b') + '000000000000'
        poly = [int(b) for b in version_bin_str]
        # Perform polynomial division
        poly_rest_result = ErrorCorrection().poly_rest(poly, VERSION_DIVISOR)
        return poly[:6] + poly_rest_result

    def _get_format_modules(self, mask_index):
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

    def _place_fixed_patterns(self, matrix):
        size = len(matrix)

        # Finder patterns
        for row, col in [(0, 0), (size - 7, 0), (0, size - 7)]:
            self._fill_area(matrix, row, col, 7, 7)
            self._fill_area(matrix, row + 1, col + 1, 5, 5, fill=0)
            self._fill_area(matrix, row + 2, col + 2, 3, 3)

        # Separators
        self._fill_area(matrix, 7, 0, 8, 1, fill=0)
        self._fill_area(matrix, 0, 7, 1, 7, fill=0)
        self._fill_area(matrix, size - 8, 0, 8, 1, fill=0)
        self._fill_area(matrix, 0, size - 8, 1, 7, fill=0)
        self._fill_area(matrix, 7, size - 8, 8, 1, fill=0)
        self._fill_area(matrix, size - 7, 7, 1, 7, fill=0)

        # Alignment pattern
        alignment_tracks = self._get_alignment_coordinates()
        last_track = len(alignment_tracks) - 1

        for row_index, row in enumerate(alignment_tracks):
            for column_index, column in enumerate(alignment_tracks):
                # Skipping the alignment near the finder patterns
                if (row_index == 0 and (column_index == 0 or column_index == last_track)) or \
                    (column_index == 0 and row_index == last_track):
                    continue
                
                # Fill a 5x5 area with `1`
                self._fill_area(matrix, row - 2, column - 2, 5, 5)
                # Clear a 3x3 area with `0`
                self._fill_area(matrix, row - 1, column - 1, 3, 3, 0)
                # Set the specific cell to `1`
                matrix[row][column] = 1
        # self._fill_area(matrix, size - 9, size - 9, 5, 5)
        # self._fill_area(matrix, size - 8, size - 8, 3, 3, fill=0)
        # matrix[size - 7][size - 7] = 1

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

    def _fill_area(self, matrix ,row, column, width, height, fill=1):
        fill_row = [fill] * width
        matrix[row:row + height, column:column + width] = fill_row
    