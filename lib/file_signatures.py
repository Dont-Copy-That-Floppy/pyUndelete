# file_signatures.py

"""
SIGNATURES: A list of dictionaries for various binary file formats.
Each dictionary includes:
  - "extension": the file extension (without the dot)
  - "header": the file's magic number (as bytes)
  - "footer": the expected file footer (as bytes) or None if not defined.

This collection includes image, archive/compression, document, executable,
audio, video, font, disk image, and miscellaneous binary file types.
"""

SIGNATURES = [
    # ---------------------------------------------------------------------------
    # IMAGE FILES
    # ---------------------------------------------------------------------------
    # JPEG
    {"extension": "jpg", "header": b"\xff\xd8", "footer": b"\xff\xd9"},
    # PNG
    {"extension": "png", "header": b"\x89PNG\r\n\x1a\n", "footer": b"IEND\xaeB`\x82"},
    # GIF (GIF87a)
    {"extension": "gif", "header": b"GIF87a", "footer": b";"},
    # GIF (GIF89a)
    {"extension": "gif", "header": b"GIF89a", "footer": b";"},
    # TIFF (little-endian)
    {"extension": "tiff", "header": b"II*\x00", "footer": None},
    # TIFF (big-endian)
    {"extension": "tiff", "header": b"MM\x00*", "footer": None},
    # BMP
    {"extension": "bmp", "header": b"BM", "footer": None},
    # ICO (Icon)
    {"extension": "ico", "header": b"\x00\x00\x01\x00", "footer": None},
    # WebP (Note: "WEBP" appears at offset 8)
    {"extension": "webp", "header": b"RIFF", "footer": None},
    # JPEG2000 (JP2)
    {"extension": "jp2", "header": b"\x00\x00\x00\x0cjP  \r\n\x87\n", "footer": None},
    # HEIC / HEIF / AVIF (ISO Base Media File Format variants)
    {"extension": "heic", "header": b"\x00\x00\x00\x18ftypheic", "footer": None},
    {"extension": "heif", "header": b"\x00\x00\x00\x18ftypheif", "footer": None},
    {"extension": "avif", "header": b"\x00\x00\x00\x18ftypavif", "footer": None},
    # OpenEXR
    {"extension": "exr", "header": b"\x76\x2f\x31\x01", "footer": None},
    # PCX
    {"extension": "pcx", "header": b"\x0A", "footer": None},
    # ---------------------------------------------------------------------------
    # COMPRESSION / ARCHIVE FILES
    # ---------------------------------------------------------------------------
    # ZIP (common container for many formats)
    {"extension": "zip", "header": b"PK\x03\x04", "footer": b"PK\x05\x06"},
    # RAR (v4)
    {"extension": "rar", "header": b"Rar!\x1A\x07\x00", "footer": None},
    # RAR (v5)
    {"extension": "rar5", "header": b"Rar!\x1A\x07\x01\x00", "footer": None},
    # 7z
    {"extension": "7z", "header": b"7z\xBC\xAF\x27\x1C", "footer": None},
    # GZIP
    {"extension": "gz", "header": b"\x1F\x8B", "footer": None},
    # BZIP2
    {"extension": "bz2", "header": b"BZh", "footer": None},
    # XZ
    {"extension": "xz", "header": b"\xfd7zXZ\x00", "footer": None},
    # LZMA
    {"extension": "lzma", "header": b"\x5D\x00\x00\x80\x00", "footer": None},
    # Unix Compress (.Z)
    {"extension": "Z", "header": b"\x1F\x9D", "footer": None},
    # LZIP
    {"extension": "lzip", "header": b"LZIP", "footer": None},
    # Microsoft Cabinet (CAB)
    {"extension": "cab", "header": b"MSCF", "footer": None},
    # ARJ
    {"extension": "arj", "header": b"\x60\xEA", "footer": None},
    # LZ4
    {"extension": "lz4", "header": b"\x04\x22\x4D\x18", "footer": None},
    # Zstandard (Zstd)
    {"extension": "zst", "header": b"\x28\xB5\x2F\xFD", "footer": None},
    # LZOP
    {"extension": "lzo", "header": b"LZOP", "footer": None},
    # ZPAQ
    {"extension": "zpaq", "header": b"ZPAQ", "footer": None},
    # ---------------------------------------------------------------------------
    # DOCUMENT FILES
    # ---------------------------------------------------------------------------
    # PDF
    {"extension": "pdf", "header": b"%PDF", "footer": b"%%EOF"},
    # Microsoft Office (OLE Compound File for DOC, XLS, PPT)
    {"extension": "doc", "header": b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "footer": None},
    {"extension": "xls", "header": b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "footer": None},
    {"extension": "ppt", "header": b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "footer": None},
    # Office Open XML (DOCX, XLSX, PPTX, and macro-enabled variants)
    {"extension": "docx", "header": b"PK\x03\x04", "footer": None},
    {"extension": "xlsx", "header": b"PK\x03\x04", "footer": None},
    {"extension": "pptx", "header": b"PK\x03\x04", "footer": None},
    {"extension": "docm", "header": b"PK\x03\x04", "footer": None},
    {"extension": "xlsm", "header": b"PK\x03\x04", "footer": None},
    {"extension": "pptm", "header": b"PK\x03\x04", "footer": None},
    # OpenDocument formats (ODT, ODS, ODP)
    {"extension": "odt", "header": b"PK\x03\x04", "footer": None},
    {"extension": "ods", "header": b"PK\x03\x04", "footer": None},
    {"extension": "odp", "header": b"PK\x03\x04", "footer": None},
    # EPUB (electronic publications)
    {"extension": "epub", "header": b"PK\x03\x04", "footer": None},
    # RTF (Rich Text Format)
    {"extension": "rtf", "header": b"{\\rtf", "footer": b"}"},
    # CHM (Compiled HTML Help)
    {"extension": "chm", "header": b"ITSF", "footer": None},
    # MOBI (Kindle eBook)
    {"extension": "mobi", "header": b"BOOKMOBI", "footer": None},
    # PostScript / EPS
    {"extension": "ps", "header": b"%!PS", "footer": None},
    {"extension": "eps", "header": b"%!PS", "footer": None},
    # XPS (XML Paper Specification)
    {"extension": "xps", "header": b"PK\x03\x04", "footer": None},
    # ---------------------------------------------------------------------------
    # EXECUTABLE FILES
    # ---------------------------------------------------------------------------
    # Windows PE (Portable Executable)
    {"extension": "exe", "header": b"MZ", "footer": None},
    # ELF (Linux Executable)
    {"extension": "elf", "header": b"\x7fELF", "footer": None},
    # Mach-O (macOS Executable) – multiple variants
    {"extension": "macho", "header": b"\xFE\xED\xFA\xCE", "footer": None},
    {"extension": "macho", "header": b"\xFE\xED\xFA\xCF", "footer": None},
    {"extension": "macho", "header": b"\xCE\xFA\xED\xFE", "footer": None},
    {"extension": "macho", "header": b"\xCF\xFA\xED\xFE", "footer": None},
    # ---------------------------------------------------------------------------
    # AUDIO FILES
    # ---------------------------------------------------------------------------
    # MP3 (ID3 tag based)
    {"extension": "mp3", "header": b"ID3", "footer": None},
    # WAV (RIFF with WAVE identifier at offset 8)
    {"extension": "wav", "header": b"RIFF", "footer": None},
    # FLAC
    {"extension": "flac", "header": b"fLaC", "footer": None},
    # OGG
    {"extension": "ogg", "header": b"OggS", "footer": None},
    # AAC (ADTS)
    {"extension": "aac", "header": b"\xFF\xF1", "footer": None},
    # ---------------------------------------------------------------------------
    # VIDEO FILES
    # ---------------------------------------------------------------------------
    # AVI (RIFF with AVI tag at offset 8)
    {"extension": "avi", "header": b"RIFF", "footer": None},
    # MP4 (various ftyp brands)
    {"extension": "mp4", "header": b"\x00\x00\x00\x18ftyp", "footer": None},
    # MKV (Matroska)
    {"extension": "mkv", "header": b"\x1A\x45\xDF\xA3", "footer": None},
    # MOV (QuickTime / MPEG-4 container with 'ftypqt')
    {"extension": "mov", "header": b"\x00\x00\x00\x18ftypqt", "footer": None},
    # ---------------------------------------------------------------------------
    # FONT FILES
    # ---------------------------------------------------------------------------
    # TrueType Font
    {"extension": "ttf", "header": b"\x00\x01\x00\x00", "footer": None},
    # OpenType Font
    {"extension": "otf", "header": b"OTTO", "footer": None},
    # WOFF
    {"extension": "woff", "header": b"wOFF", "footer": None},
    # WOFF2
    {"extension": "woff2", "header": b"wOF2", "footer": None},
    # ---------------------------------------------------------------------------
    # DISK IMAGES / VIRTUAL DISKS
    # ---------------------------------------------------------------------------
    # DMG (Apple Disk Image)
    {"extension": "dmg", "header": b"koly", "footer": None},
    # VHD (Virtual Hard Disk) – simplified signature
    {"extension": "vhd", "header": b"conectix", "footer": None},
    # VMDK (VMware Disk) – placeholder signature
    {"extension": "vmdk", "header": b"# Disk", "footer": None},
    # ---------------------------------------------------------------------------
    # MISCELLANEOUS / OTHER BINARY FILES
    # ---------------------------------------------------------------------------
    # SWF (Shockwave Flash)
    {"extension": "swf", "header": b"FWS", "footer": None},
    {"extension": "swf", "header": b"CWS", "footer": None},
    {"extension": "swf", "header": b"ZWS", "footer": None},
    # Serialized Java Object
    {"extension": "ser", "header": b"\xac\xed\x00\x05", "footer": None},
]
