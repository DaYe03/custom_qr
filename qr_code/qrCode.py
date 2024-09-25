from .custom_qr import CustomQR
from .generate_qr import GenerateQR
from .constraints import ERROR_CORRECTION_LEVEL_H, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_L
import cv2

class QrCode:
    """
    QrCode class to generate and print QR code
    """	
    def __init__(self, version=None, error_correction=ERROR_CORRECTION_LEVEL_L):
        self.version = version
        self.error_correction = error_correction
        self.qr = GenerateQR()
        self.custom = CustomQR()
    
    def generate(self, data):
        return self.qr.generate(data, version=self.version, error_correction=self.error_correction)
    
    def create_qr_image(self, matrix, 
                        background=(255,255,255), 
                        block_style={"size": 10, "type" : 0, "color":[(0,0,0)]}, 
                        finder_style={"color":(0,0,0)},
                        alignment_style = None):
        return self.custom.draw_qr(matrix, background, block_style, finder_style, alignment_style)
    
    def print_qr_console(self, matrix):
        self.qr.print_qr(matrix)

    def display_qr(self, img):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def create_image_file(self, img, filename="qr.png"):
        cv2.imwrite(filename, img)
    
    def write_text(self, img, text, 
                    text_style={"color":(0,0,0), "size": "small", "bot": 0, "left": 0, "orientation": 0}, 
                    background=(255,255,255), block_size=10):
        return self.custom.write_text(img, text_style, background, block_size, text)