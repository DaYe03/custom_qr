from qr_code import QrCode
from qr_code import ERROR_CORRECTION_LEVEL_H, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_L 


qr = QrCode(version=6, error_correction=ERROR_CORRECTION_LEVEL_Q)
matrix = qr.generate("https://www.qrcode.com/")
qr.print_qr(matrix) # Print the QR code in the console
qr.create_qr_image(matrix) # Save the QR code as an image

qr = QrCode() # auto version and error correction
matrix = qr.generate("https://www.qrcode.com/")
qr.print_qr(matrix) # Print the QR code in the console
qr.create_qr_image(matrix, filename="qr.png") # Save the QR code as an image
