# Icon Converter

A simple GUI application to convert PNG images into various icon formats for Windows and MacOS.(Download the .exe file from the Standalone_for_windows folder)

## Features

- Drag and drop interface for easy image selection
- Preview of selected image
- Creates Windows icons in multiple sizes (16x16 to 512x512)
- Creates MacOS icons in multiple sizes (16x16 to 1024x1024)
- Progress bar showing conversion status
- Creates all icons in an 'assets' directory

## Requirements

- Python 3.6 or higher
- Pillow (PIL) library
- tkinterdnd2 library

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
```bash
pip install pillow==10.2.0
pip install tkinterdnd2==0.3.0
```

## Usage

1. Run the application:
```bash
python icon_converter_gui.py
```

2. Either drag and drop a PNG image onto the application window or click the "Browse Image" button to select an image
3. Click the "Convert" button to start the conversion process
4. The converted icons will be saved in the 'assets' directory

## Output Files

The application creates the following files in the 'assets' directory:

### Windows Icons
- `icon_16x16.ico`
- `icon_32x32.ico`
- `icon_48x48.ico`
- `icon_64x64.ico`
- `icon_128x128.ico`
- `icon_256x256.ico`
- `icon_512x512.ico`

### MacOS Icons
- `logo.icns` (contains all required sizes for MacOS)

### Original Image
- `logo.png` (copy of the input image)

## Notes

- The application only accepts PNG images as input
- On Windows systems, a placeholder .icns file will be created since the iconutil command is not available
- All icons are created with high-quality resampling for optimal appearance

## Author

R.H. Amezqueta 
