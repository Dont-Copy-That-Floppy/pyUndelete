# pyUndelete

## Overview

pyUndelete is a forensic and recovery tool written in Python. It scans disk images or drives for recoverable file fragments using low-level carving techniques based on file signatures. The tool uses ctypes and mmap for efficient binary data access and implements integrity verification using header/footer matching and Shannon entropy analysis. A Tkinter-based GUI lets users select a drive, view detected file fragments, choose which files to recover, and save/load a database of the scan results.

## Features

- **Low-Level File Carving:**  
  Uses `ctypes` to access C library functions (e.g., `memmem`) and `mmap` to scan large binary files efficiently.
  
- **Fragment Assembly:**  
  Detects contiguous file fragments and merges orphan fragments based on a configurable gap threshold.
  
- **Integrity Verification:**  
  Applies heuristics such as header/footer matching, minimum file size, and Shannon entropy analysis to ensure file fragments are likely intact.
  
- **Extensive File Signatures:**  
  Supports a wide range of file types (images, archives, documents, executables, audio, video, fonts, etc.) defined in separate signature files.
  
- **User-Friendly GUI:**  
  A Tkinter interface allows users to:
  - Browse for a drive or disk image.
  - Display found file fragments in a table.
  - Highlight and select files for recovery.
  - Choose a destination folder for recovered files.
  - Save and load a JSON database of found files.

## Requirements

- **Python:** Version 3.6 or higher.
- **Tkinter:** Typically included with Python installations.
- **Standard Libraries:**  
  `sys`, `os`, `mmap`, `ctypes`, `platform`, `math`, `threading`, `json`, `tkinter`, `tkinter.ttk`

_No additional external packages are required._

## Project Structure

```
project/
├── main.py                 # Main Tkinter GUI application
├── file_carver.py          # Core file carving functions
├── lib/
│   └── file_signatures.py  # File signature definitions for various file types
└── README.md               # Project documentation
```

## Installation

1. **Clone or Download the Repository:**

   ```bash
   git clone https://github.com/Dont-Copy-That-Floppy/pyUndelete.git
   cd pyUndelete
   ```

2. **(Optional) Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   # On Unix/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Run the Application:**

   ```bash
   python main.py
   ```

## Usage

1. **Select Drive/Image:**  
   Click the **Browse** button to choose a disk image or drive file.

2. **Select Destination:**  
   Use the **Browse** button next to the Destination field to choose where recovered files will be saved.

3. **Scan the Drive:**  
   Click **Scan Drive** to start scanning. The tool will process the file and list detected file fragments in the Treeview.

4. **Recover Files:**  
   Select one or more fragments from the list and click **Recover Selected** to save them to the chosen destination.

5. **Database Management:**  
   - **Save DB:** Save the list of found file fragments as a JSON file.
   - **Load DB:** Reload a previously saved scan result to review or continue recovery.

## Customization

- **File Signatures:**  
  Update or add new file signatures by modifying `lib/file_signatures.py`.

- **Carving Logic & Integrity Checks:**  
  Adjust parameters (such as entropy thresholds or size checks) in `file_carver.py` to fine-tune recovery for your specific needs.

- **GUI Enhancements:**  
  Extend the Tkinter interface in `main.py` to add more features or improve usability.

## Limitations and Future Improvements

- **Fragmentation Handling:**  
  The current heuristics for merging orphan fragments may not cover all real-world cases. Future versions could integrate more advanced reassembly techniques.

- **File Verification:**  
  The integrity verification relies on simple heuristics. Incorporating more robust analysis or integrating forensic libraries could improve accuracy.

- **Extensibility:**  
  Additional file types or customized processing can be added as needed.

## Disclaimer

This tool is provided "as-is" and is intended for educational and research purposes only. Use it only on media for which you have proper authorization. The authors assume no responsibility for any damage or data loss resulting from its use.

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.