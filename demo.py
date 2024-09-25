from qr_code import QrCode
from qr_code import ERROR_CORRECTION_LEVEL_H, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_L 

qr = QrCode(); # auto version and error correction

# Generate the QR code
matrix, version = qr.generate("https://www.qrcode.com/")

# Print the QR code in the console
qr.print_qr_console(matrix) 

# Create the QR code image
img = qr.create_qr_image(matrix) 

# Display the QR code in a window, Press any key to close the window
qr.display_qr(img)

# Save the QR code as an image
qr.create_image_file(img, filename="qr.png") 

######################################################################################################################
# Generate the QR code with a specific version and error correction level
qr = QrCode(version=6, error_correction=ERROR_CORRECTION_LEVEL_Q)
matrix, version = qr.generate("https://www.qrcode.com/") # Generate the QR code
img = qr.create_qr_image(matrix) # Create the QR code image

# Write the text on the QR code image
qr.write_text(img, text="qrcode") 

qr.display_qr(img) # Display the QR code in a window, Press any key to close the window
