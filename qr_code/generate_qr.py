import numpy as np
from .constraints import MODE_NUMBER, MODE_ALPHANUMERIC, MODE_BYTE, MODE_KANJI, MODE_ECI, MODE_MIXED, ERROR_CORRECTION_LEVEL_L, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_H, EC_CODEWORDS, FONT_SIZE_LARGE_LARGE, FONT_SIZE_LARGE, FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, POSITION_BOTTOM_LEFT, POSITION_BOTTOM_RIGHT, POSITION_TOP_LEFT, POSITION_TOP_RIGHT, POSITION_MIDDLE
from .errorCorrection import ErrorCorrection
from .dataConverter import DataConverter

# TODO: cache all the module_sequence for each version
class GenerateQR:
    # def __init__(self):

    def generate(self, data, version = None, error_correction = ERROR_CORRECTION_LEVEL_L):
        encoded_data, version = self.get_encoded_data(data, version, error_correction)
        codewords = self.get_codewords(encoded_data, version, error_correction)
        module_sequence = self.get_module_sequence(codewords, version, error_correction)
        optimanl_mask = self.get_optimal_mask(codewords ,module_sequence, version, error_correction)
        return optimanl_mask, version

    def get_encoded_data(self, data, version, error_correction):
        dataConverter = DataConverter(version, error_correction)
        encoded_data = dataConverter.encode(data)
        return encoded_data, dataConverter.version

    def get_codewords(self, encoded_data, version, error_correction):
        table = EC_CODEWORDS[version][error_correction] 
        blocks = []
        ec_blocks = []
        codewords = []

        for i in range(table[2] + table[4]):
            if i < table[2]:
                block_size = table[3]
            else:
                block_size = table[5]
            blocks.append(encoded_data[:block_size])
            encoded_data = encoded_data[block_size:]
            ec_blocks.append(ErrorCorrection().getEDC(blocks[i], block_size+table[1]))

        for c in range(table[3]):
            for j in range(table[2] + table[4]):
                codewords.append(blocks[j][c])
        for j in range(table[2], table[2] + table[4]):
            codewords.append(blocks[j][table[5] - 1])
        for c in range(table[1]):
            for j in range(table[2]+table[4]):
                codewords.append(ec_blocks[j][c])
        
        return codewords

    def get_module_sequence(self, codewords, version, error_correction):
        size = 17 + 4 * version
        matrix = np.zeros((size, size), dtype=int)

        self._fill_area(matrix, 0, 0, 9, 9)  # Top-left finder pattern
        self._fill_area(matrix, 0, size - 8, 8, 9)  # Top-right finder pattern
        self._fill_area(matrix, size - 8, 0, 9, 8)  # Bottom-left finder pattern

        # Alignment patterns
        alignment_tracks = GenerateQR.get_alignment_coordinates(version)
        last_track = len(alignment_tracks) - 1 
        for row_index, row in enumerate(alignment_tracks):
            for column_index, column in enumerate(alignment_tracks):
                if (row_index == 0 and (column_index == 0 or column_index == last_track)) or \
                    (column_index == 0 and row_index == last_track):
                    continue
                self._fill_area(matrix, row - 2, column - 2, 5, 5)
        
        # Timing patterns
        self._fill_area(matrix, 6, 9, version * 4, 1)  # Horizontal timing pattern
        self._fill_area(matrix, 9, 6, 1, version * 4)  # Vertical timing pattern

        # Dark module
        matrix[size - 8, 8] = 1

        # Version information
        if version >= 7:
            self._fill_area(matrix, 0,size - 11, 3, 6)
            self._fill_area(matrix, size - 11, 0, 6, 3)

        row_step = -1
        row = size - 1
        column = size - 1
        sequence = []
        index = 0

        # elaborete the insertion sequence of the modules
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

    @staticmethod
    def get_alignment_coordinates(version):
        if version == 1:
            return []
        intervals = version // 7 + 1
        distance = 4 * version + 4
        step = -(-distance // (intervals * 2)) * 2  
        return [6] + [distance + 6 - (intervals - 1 - index) * step for index in range(intervals)]

    def _fill_area(self, matrix ,row, column, width, height, fill=1):
        fill_row = [fill] * width
        matrix[row:row + height, column:column + width] = fill_row

    def get_optimal_mask(self, codewords, module_sequence, version, error_correction):
        best_matrix = None
        best_score = float('inf')
        for index in range(8):
            matrix = self.get_mask_matrix(index, codewords, module_sequence, version, error_correction) 
            penalty_score = self.get_penalty_score(matrix) 
            if penalty_score < best_score:
                best_score = penalty_score
                best_matrix = matrix
        return best_matrix

    def get_mask_matrix(self, mask_index, codewords, module_sequence, version, error_correction):
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
        size = version * 4 + 17
        # apply codewords and mask
        mask_fn = MASK_FNS[mask_index]
        matrix = np.zeros((size, size), dtype=int)
        for index, (row, column) in enumerate(module_sequence):
            if index >> 3 >= len(codewords):
                break
            # Each codeword contains 8 modules, so shifting the index to the right by 3 gives the codeword's index
            codeword = codewords[index >> 3]
            bit_shift = 7 - (index & 7)
            module_bit = (codeword >> bit_shift) & 1
            # Apply the mask function to the module bit
            matrix[row][column] = module_bit ^ int(mask_fn(row, column))

        # calculate the format information
        FORMAT_DIVISOR = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1], dtype=int)
        FORMAT_MASK = np.array([1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], dtype=int)
        format_poly = np.zeros(15, dtype=int)
        if error_correction == ERROR_CORRECTION_LEVEL_L:
            error_index = 1
        elif error_correction == ERROR_CORRECTION_LEVEL_M:
            error_index = 0
        elif error_correction == ERROR_CORRECTION_LEVEL_Q:
            error_index = 3
        elif error_correction == ERROR_CORRECTION_LEVEL_H:
            error_index = 2
        format_poly[0] = error_index >> 1
        format_poly[1] = error_index & 1
        format_poly[2] = mask_index >> 2
        format_poly[3] = (mask_index >> 1) & 1
        format_poly[4] = mask_index & 1
        rest = ErrorCorrection().poly_rest(format_poly, FORMAT_DIVISOR)
        format_poly[5:] = rest
        masked_format_poly = np.bitwise_xor(format_poly, FORMAT_MASK)
        format_modules = masked_format_poly.tolist()

        # place format information
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
        
        # place fixed patterns
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
        alignment_tracks = GenerateQR.get_alignment_coordinates(version)
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
        # version information
        if version < 7:
            return matrix
        version_info = self.get_version_information(version)
        for index, bit in enumerate(version_info):
            row = index // 3
            col = index % 3
            # Update matrix at specific positions
            matrix[5 - row][size - 9 - col] = bit
            matrix[size - 11 + col][row] = bit
        return matrix

    def get_version_information(self, version):
        VERSION_DIVISOR = [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1]
        version_bin_str = format(version, '06b') + '000000000000'
        poly = [int(b) for b in version_bin_str]
        # Perform polynomial division
        poly_rest_result = ErrorCorrection().poly_rest(poly, VERSION_DIVISOR)
        return poly[:6] + poly_rest_result

    def get_penalty_score(self, matrix):
        RULE_3_PATTERN = np.array([1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0], dtype=np.uint8)
        RULE_3_REVERSED_PATTERN = RULE_3_PATTERN[::-1]
        total_penalty = 0
        
        # Rule 1
        row_penalty = sum(self.get_line_penalty(row) for row in matrix)
        total_penalty += row_penalty
        
        column_penalty = sum(self.get_line_penalty(matrix[:, column_index]) for column_index in range(matrix.shape[1]))
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

    def get_line_penalty(self, line):
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