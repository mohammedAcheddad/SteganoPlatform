# Steganography App

## Overview
Steganography App is a simple application that allows users to encode and decode hidden messages in PNG images using different transformation methods such as Discrete Cosine Transform (DCT) and Discrete Wavelet Transform (DWT).

## Features
- **Encoding:** Embed text messages into PNG images using DCT or DWT transformations.
- **Decoding:** Retrieve hidden messages from encoded PNG images using DCT or DWT transformations.
- **User Interface:** Intuitive user interface with drag-and-drop support for easy file selection.

## Requirements
- Python 3.x
- Required Python libraries: `numpy`, `pywt`, `pillow`, `opencv-python`, `tkinter`, `tkinterdnd2`, `customtkinter`, `stegano`, `scipy`

## How to Run
1. Install the required libraries using the following command:
pip install numpy pywt pillow opencv-python tkinter tkinterdnd2 customtkinter stegano scipy

2. Run the application:
python steganography_app.py


## Usage
1. Drag and drop a PNG image onto the application or click the button to choose a file.
2. Select whether to encode or decode data.
3. For encoding, enter the text message and choose the transformation method (DCT or DWT).
4. For decoding, the application will display the decoded message.

## Credits
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [PyWavelets](https://pywavelets.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [TkinterDnD2](https://pypi.org/project/tkinterdnd2/)
- [CustomTkinter](https://pypi.org/project/customtkinter/)
- [Stegano](https://pypi.org/project/stegano/)
- [SciPy](https://www.scipy.org/)

