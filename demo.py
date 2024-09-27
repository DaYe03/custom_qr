from custom_qr import QrCode, ERROR_CORRECTION_LEVEL_Q

qr = QrCode(); 

# Generate the QR code
matrix, version = qr.generate("https://www.qrcode.com/") # auto version and error correction level

# Print the QR code in the console
qr.print_qr_console(matrix) 

# Create the QR code image
img = qr.create_qr_image(matrix) 

# Display the QR code in a window, Press any key to close the window
qr.display_qr(img)

# Save the QR code as an image
qr.create_image_file(img, filename="qr.png") 

######################################################################################################################

qr = QrCode()
matrix, version = qr.generate("https://www.qrcode.com/", version=6, error_correction=ERROR_CORRECTION_LEVEL_Q) # Generate the QR code with a specific version and error correction level
img = qr.create_qr_image(matrix) # Create the QR code image

# Write the text on the QR code image
img_txt = qr.write_text(img, text="qrcode") 

qr.display_qr(img_txt) # Display the QR code in a window, Press any key to close the window
