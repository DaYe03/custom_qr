import unittest
import os
import numpy as np
from custom_qr.qrCode import QrCode 

class TestQrCode(unittest.TestCase):
    def setUp(self):
        """Set up the QrCode object before each test."""
        self.qr = QrCode()
        self.version = 6

    def test_generate(self):
        """Test QR code generation."""
        data = "https://example.com"
        matrix, version = self.qr.generate(data)
        self.assertIsNotNone(matrix)  # Ensure matrix is not None
        self.assertEqual(matrix.shape[0], 21)  # Check the shape for version 1

    def test_create_qr_image(self):
        """Test creating a QR code image."""
        data = "https://example.com"
        matrix, version = self.qr.generate(data)
        img = self.qr.create_qr_image(matrix)
        self.assertIsInstance(img, np.ndarray)  # Check if returned image is a numpy array

    def test_print_qr_console(self):
        """Test printing QR code to console (assumed to be void)."""
        data = "https://example.com"
        matrix, version = self.qr.generate(data)
        self.qr.print_qr_console(matrix)  # This should execute without error

    def test_create_image_file(self):
        """Test creating an image file."""
        data = "https://example.com"
        matrix, version = self.qr.generate(data)
        img = self.qr.create_qr_image(matrix)
        self.qr.create_image_file(img, "test_qr.png")
        self.assertTrue(os.path.exists("test_qr.png"))  # Check if the file is created

    def test_write_text(self):
        """Test writing text on QR code."""
        data = "https://example.com"
        matrix, version = self.qr.generate(data)
        img = self.qr.create_qr_image(matrix)
        text_img = self.qr.write_text(img, "TMP")
        self.assertIsInstance(text_img, np.ndarray)  # Check if returned image is a numpy array

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists("test_qr.png"):
            os.remove("test_qr.png")  # Remove the created test image file
        if os.path.exists("example_qr_with_text.png"):
            os.remove("example_qr_with_text.png")  # Remove the text image file

if __name__ == '__main__':
    unittest.main()