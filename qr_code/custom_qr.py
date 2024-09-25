import cv2
import numpy as np
from .generate_qr import GenerateQR
from .charset import small

class CustomQR:
    """
    Draw a QR code with custom blocks, custom finder, custom  and text

    draw_qr(matrix, background, block_style, finder_style, alignment_style): 
        Draw a QR code with custom blocks, custom finder, custom alignment and custom text
    
    write_text(img, text_style, background, block_size, text):
        Write a text on the QR code

    struct block_style:
        size: int
        type: int       # 0: square, 1: circle
        color: list of tuples
    
    struct finder_style:
        color: tuple
    
    struct alignment_style:
        color: tuple
    
    struct text_style:
        color: tuple
        size: str    # "small"
        bot: int
        left: int
        orientation: int
    """	
    def draw_qr(self, matrix, 
                background = (255,255,255), 
                block_style = {"size": 10, "type" : 0, "color":[(0,0,0)]}, 
                finder_style = {"color":(0,0,0)}, 
                alignment_style = None):
        # if alignment_style is not defined, use the finder style
        if alignment_style is None:
            alignment_style = finder_style

        block_size = block_style["size"]
        real_size = len(matrix) * block_size
        matrix_size = len(matrix)

        img = np.full((real_size, real_size, 3), background, dtype=np.uint8) # Create the image 
        
        img = self._draw_blocks(img, matrix, block_style, background) # Draw the modules/blocks
        self._draw_finder(img, matrix_size, finder_style, block_size, background) # Draw the finder patterns
        self._draw_alignment(img, matrix_size, alignment_style, block_size, background) # Draw the alignment patterns

        return img
    
    def write_text(self, img, text_style, background, block_size, text):
        if not self.check_space(img, text, block_size, text_style):
            return -1 # not enough space
        
        color = text_style["color"]
        size = text_style["size"]
        bot = text_style["bot"]
        left = text_style["left"]
        orientation = text_style["orientation"]

        if size == "small":
            charset = small
        if orientation == 1:
            text = text[::-1]
        for i, character in enumerate(text):
            if character in charset:
                char = charset[character]
                box_width = self.write_char(img, char, bot, left, block_size, color, background, orientation)
                if orientation == 0:
                    left += box_width
                elif orientation == 1:
                    left -= box_width
        return 0
    
    def write_char(self, img, char, bot, left, block_size, color, background, orientation):
        box_height, box_width = char.shape

        box = np.full((box_height * block_size, box_width * block_size, 3), background, dtype=np.uint8)
        color_block = np.full((block_size, block_size, 3), color, dtype=np.uint8)
        for i in range(char.shape[0]):
            for j in range(char.shape[1]):
                if char[i][j] == 1:
                    box[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = color_block


        w_margin = np.full((block_size, box_width * block_size, 3), background, dtype=np.uint8)
        if bot > 0:
            # add the margin to the bottom of the box
            box = np.concatenate((box, w_margin), axis=0)
            box_height += 1 # update the height of the box with the margin
            bot -= 1
        if (bot + box_height) * block_size < img.shape[0]:
            # add the margin to the top of the box
            box = np.concatenate((w_margin, box), axis=0)
            box_height += 1
        

        h_margin = np.full((box_height * block_size, block_size, 3), background, dtype=np.uint8)
        
        if orientation == 0:
            if left > 0:
                box = np.concatenate((h_margin, box), axis=1)
                box_width += 1
                left -= 1 
            if (left + box_width) * block_size < img.shape[1]:
                box = np.concatenate((box, h_margin), axis=1)
                box_width += 1
            img_left_start = left * block_size
            img_left_end = img_left_start + box.shape[1]
        elif orientation == 1:
            right = left - box_width
            if right > 0:
                box = np.concatenate((h_margin,box), axis=1)
                box_width += 1
                right -= 1
            if left > 0:
                box = np.concatenate((box, h_margin), axis=1)
                box_width += 1
                left += 1
            img_left_end = left * block_size
            img_left_start = right * block_size

        img_bot_start = img.shape[0] - (bot * block_size) - box.shape[0]
        img_bot_end = img.shape[0] - (bot * block_size)
        img[img_bot_start:img_bot_end, img_left_start:img_left_end] = box

        return char.shape[1] + 1 # add 1 to consider the space between characters   

    def check_space(self, img, text, box_size, text_style):
        size = text_style["size"]
        bot = text_style["bot"]
        left = text_style["left"]
        orientation = text_style["orientation"]

        matrix_len = int(img.shape[0] // box_size)

        if orientation == 0:
            margin = left
        elif orientation == 1:
            margin = matrix_len - left

        total_width = 0
        total_height = 0
        if size == "small":
            for i, c in enumerate(text):
                if c in small:
                    char_height, char_width = small[c].shape
                    # if i == 0 and left != 0:
                    #     total_width += left
                    if i == 0 and margin != 0:
                        total_width += margin
                    if i != 0 : # sum the space between characters
                        total_width += 1
                    total_width += char_width
                    
                    total_height = max (total_height, char_height)

        if orientation == 0:
            return matrix_len - (total_height + bot) >= 0 and matrix_len - (total_width + left) >= 0
        elif orientation == 1:
            return matrix_len - (total_height + bot) >= 0 and left - total_width >= 0

    def _draw_blocks(self, img, matrix, block_style, background):
        if block_style["type"] == 0: # square
            self._draw_blocks_square(img, matrix, block_style)
        elif block_style["type"] == 1: # circle
            self._draw_blocks_circle(img, matrix, block_style, background)
        return img

    def _draw_blocks_square(self, img, matrix, block_style):
        block_size = block_style["size"]
        colors = block_style["color"]
        color_len = len(colors)

        colored_block = np.array(colors[0], dtype=np.uint8) if color_len == 1 else None

        for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    if matrix[i][j] == 1:
                        if color_len > 1:
                            color = colors[(i * matrix.shape[1] + j) % color_len]
                            colored_block = np.array(color, dtype=np.uint8)
                        img[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = colored_block
    
    def _draw_blocks_circle(self, img, matrix, block_style, background):
        block_size = block_style["size"]
        colors = block_style["color"]
        color_len = len(colors)

        radius = int(block_size // 2.1)

        # Pre-generate the colored circles
        colored_circles = []
        for color in colors:
            colored_circle = np.full((block_size, block_size, 3), background, dtype=np.uint8)
            colored_circle = cv2.circle(colored_circle, (block_size//2, block_size //2), radius, color, -1, cv2.LINE_AA)
            colored_circles.append(colored_circle)

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i][j] == 1:
                    color_index = (i * matrix.shape[1] + j) % color_len
                    top_left_x = j * block_size
                    top_left_y = i * block_size
                    img[top_left_y:top_left_y + block_size, top_left_x:top_left_x + block_size] = colored_circles[color_index]
    
    def _draw_finder(self, img, length, finder_style, block_size, background):
        color = finder_style['color']
        finder_positions = [(0,0), (0, length-7), (length-7, 0)]

        finder = np.full((7*block_size, 7*block_size, 3), color, dtype=np.uint8)
        finder[block_size: 6*block_size, block_size: 6* block_size] = background
        finder[2*block_size: 5*block_size, 2*block_size: 5*block_size] = color

        for row, col in finder_positions:
            top_left_x = row * block_size
            top_left_y = col * block_size
            bottom_right_x = (row + 7) * block_size
            bottom_right_y = (col + 7) * block_size

            img[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = finder
    
    def _draw_alignment(self, img, length, alignment_style, block_size, background):
        color = alignment_style['color']

        alignment_tracks = GenerateQR.get_alignment_coordinates(int((length-21)/4)+1)
        last_track = len(alignment_tracks) - 1

        alignment = np.full ((5*block_size, 5*block_size, 3), color, dtype=np.uint8)
        alignment[block_size:4*block_size, block_size:4*block_size] = background
        alignment[2*block_size:3*block_size, 2*block_size:3*block_size] = color

        for row_index, row in enumerate(alignment_tracks):
            for column_index, column in enumerate(alignment_tracks):
                # Skipping the alignment near the finder patterns
                if (row_index == 0 and (column_index == 0 or column_index == last_track)) or \
                   (column_index == 0 and row_index == last_track):
                    continue
                
                top_left_x = (column - 2)* block_size
                top_left_y = (row - 2) * block_size
                bottom_right_x = (column + 5 - 2) * block_size
                bottom_right_y = (row + 5 - 2) * block_size

                img[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = alignment
                

