

## Overview
This project is a **Steganography Application** that allows hiding and extracting secret messages inside:
- Images
- Audio
- Video
- Text

The application includes both internal steganography algorithms and external tools such as:
- **SilentEye** (for Image + Audio)
- **DeEgger Embedder** Video Steganography Tool
The UI is built using **CustomTkinter**.

## How to Run the Project
1. Make sure you have Python 3.10 or newer installed.
2. Install required libraries:
   ```
   pip install customtkinter pillow numpy opencv-python
   ```
3. Run the application:
   ```
   python steganography_app.py
   ```

## Image Steganography
### Supported Methods
- LSB  
- Parity  
-Bitplane

### Buttons
- Hide Message  
- Extract Message  
-(SilentEye)  hide - Extract  

## Audio Steganography
### Supported Methods
- LSB Audio  
- Parity Audio  
- Echo Hiding    " has an issue in Extraction"

### Buttons
- Hide  
- Extract  
- (SilentEye)  hide - Extract  

## Video Steganography
Video hiding runs through an external tool:
- Open Video Steganography Tool

## Text Steganography
-Includes hiding, extraction, 
-ZW ,Parity,whitespace techniques 

## Known Issues
### Audio Extraction
There is a known issue where extraction may fail or produce incomplete/incorrect results.

## External Tools
- SilentEye  
- DeEgger Embedder  

## Notes
- Audio extraction still needs improvement.
- External tools must exist in the correct paths.
## 
 must install the tools in your pc and modify the path of the shortcut in the steganography_app.py on top  like " 
 
 DEEGGER_LNK_PATH = r"C:\Users\User\OneDrive - Benha University (Faculty Of Computers & Information Technolgy)\Desktop\project\video tools\DeEgger Embedder.lnk"

SILENTEYE_LNK_PATH = r"C:\Users\User\OneDrive - Benha University (Faculty Of Computers & Information Technolgy)\Desktop\project\video tools\SilentEye.lnk"
 
 " 