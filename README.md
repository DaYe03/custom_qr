WORK IN PROGRESS

<!-- ## QR Code Library

This library provides functionality to generate QR codes and a wide variety of options to customize them.

### Installation

1. **Clone the Repository**  
   Clone the repository using the following command:

   ```sh
   git clone https://github.com/DaYe03/QrCode-library.git
   ```

2. **Install Required Dependencies**
Install the dependencies listed in `requirements.txt`:

   ``` sh
   pip install -r requirements.txt
   ```

3. **Verify Installation**
You can verify that the dependencies have been installed correctly by running:

   ``` sh
   pip list
   ```

This command will display a list of installed packages, allowing you to check that `numpy` and `pillow` are included

**NOTE:it is reccomended to use a virtual environment**

### Usage

Here’s how you can use the library to generate QR codes:

1. **Import the Library**

``` python
from qr_code import QrCode
from qr_code import ERROR_CORRECTION_LEVEL_H, ERROR_CORRECTION_LEVEL_Q, ERROR_CORRECTION_LEVEL_M, ERROR_CORRECTION_LEVEL_L
```

2. **Create a QR Code**
You can create a QR code with a specified version or use the default version:

``` python
qr = QrCode(version=6)
```

Or simply:

``` python
qr = QrCode()
```

3. **Set Error Correction Level**
Set the error correction level or leave it as default (level L):

``` python
qr.set_error_correction_level(ERROR_CORRECTION_LEVEL_H)
```

4. **Generate Matrix**
Generate the QR code matrix for a given data:

``` python
matrix = qr.generate("https://www.qrcode.com/")
```

5. **Print QR Code to Console**
Print the QR code matrix to the console:

``` python
qr.print_qr(matrix)
```

6. **Save QR Code as Image**
Save the QR code matrix as an image file:

``` python
qr.create_qr_image(matrix)
```

### Contributing

Feel free to contribute to this project by submitting issues or pull requests.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

- - -

Feel free to adjust the instructions according to your specific needs or additional setup steps. -->