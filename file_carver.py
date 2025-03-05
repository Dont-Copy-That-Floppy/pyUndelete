import sys
import os
import mmap
import ctypes
import platform
import math
from collections import Counter
from lib import file_signatures


class FILE_CARVER:

    # --- Low-Level Access Functions ---
    def get_libc():
        """Load the C library depending on the operating system."""
        if platform.system() == "Windows":
            return ctypes.cdll.msvcrt
        else:
            return ctypes.CDLL("libc.so.6")


    libc = get_libc()
    try:
        libc.memmem.restype = ctypes.c_void_p
    except AttributeError:
        libc.memmem = None


    def recover_fragment(image_path, fragment, destination_folder):
        """
        Recovers a single file fragment from the drive/image.
        Given the fragment info (offset, size, extension), it reads the data and writes it out.
        """
        ext = fragment["extension"]
        offset = fragment["offset"]
        size = fragment["size"]
        with open(image_path, "rb") as f:
            f.seek(offset)
            data = f.read(size)
        file_name = f"recovered_{fragment['id']}.{ext}"
        dest_path = os.path.join(destination_folder, file_name)
        with open(dest_path, "wb") as out:
            out.write(data)
        return dest_path


    def scan_drive(self, image_path, signatures=file_signatures, gap_threshold=1024 * 1024):
        """
        Scans the given drive/image using the carving functions from file_carver.
        Instead of immediately writing recovered files, it collects file information.
        Returns a list of dictionaries with details about each found file.
        """
        found_files = []
        with open(image_path, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            file_counter = 0
            for sig in signatures:
                ext = sig["extension"]
                header = sig["header"]
                footer = sig["footer"]
                # Use the provided get_fragments function.
                fragments = self.get_fragments(mm, header, footer, gap_threshold)
                for frag in fragments:
                    start, end = frag
                    carved_data = mm[start:end]
                    if self.verify_file_integrity(carved_data, ext, header, footer):
                        file_counter += 1
                        found_files.append({"id": file_counter, "extension": ext, "offset": start, "size": end - start, "entropy": self..compute_entropy(carved_data)})
            mm.close()
        return found_files


    def find_all_with_memmem(self, mm_obj, needle):
        """
        Use the C library's memmem to search for all occurrences of needle
        in the memory-mapped object. Returns a list of offsets.
        """
        results = []
        base_addr = ctypes.addressof(ctypes.c_char.from_buffer(mm_obj))
        haystack_len = len(mm_obj)
        needle_len = len(needle)
        current_ptr = self.libc.memmem(ctypes.c_void_p(base_addr), haystack_len, needle, needle_len)
        while current_ptr:
            offset = current_ptr - base_addr
            results.append(offset)
            remaining_len = haystack_len - (offset + 1)
            if remaining_len <= 0:
                break
            current_ptr = self.libc.memmem(ctypes.c_void_p(current_ptr + 1), remaining_len, needle, needle_len)
        return results


    def find_all_python(self, data, needle):
        """Fallback Python implementation to search for all occurrences of needle."""
        results = []
        start = 0
        while True:
            idx = data.find(needle, start)
            if idx == -1:
                break
            results.append(idx)
            start = idx + 1
        return results


    def find_all_occurrences(self, mm_obj, needle):
        """Choose the memmem method if available; otherwise use the Python search."""
        if self.libc.memmem is not None:
            return self.find_all_with_memmem(mm_obj, needle)
        else:
            return self.find_all_python(mm_obj, needle)


    # --- Fragment Assembly ---
    def get_fragments(self, mm, header, footer, gap_threshold=1024 * 1024):
        """
        Returns a list of (start, end) tuples representing candidate file fragments.
        First, it finds contiguous fragments (header followed by footer). For headers without
        an immediately found footer, the region until the next header (or end of file) is marked
        as an orphan fragment. Orphan fragments separated by gaps smaller than gap_threshold are merged.
        """
        contiguous = []
        orphan = []
        headers = self.find_all_occurrences(mm, header)

        for idx, pos in enumerate(headers):
            footer_offset = mm.find(footer, pos + len(header))
            if footer_offset != -1:
                contiguous.append((pos, footer_offset + len(footer)))
            else:
                # If no footer is found, mark as orphan fragment until the next header or end of file.
                next_header = headers[idx + 1] if idx + 1 < len(headers) else len(mm)
                orphan.append((pos, next_header))

        # Merge orphan fragments if gap between them is below the threshold.
        merged_orphan = []
        if orphan:
            current_start, current_end = orphan[0]
            for frag in orphan[1:]:
                frag_start, frag_end = frag
                if frag_start - current_end < gap_threshold:
                    current_end = frag_end
                else:
                    merged_orphan.append((current_start, current_end))
                    current_start, current_end = frag
            merged_orphan.append((current_start, current_end))

        return contiguous + merged_orphan


    # --- File Integrity Verification Using Headers and Entropy ---
    def compute_entropy(self, data):
        """
        Computes the Shannon entropy (in bits per byte) of the given data.
        """
        if not data:
            return 0
        counter = Counter(data)
        length = len(data)
        entropy = 0
        for count in counter.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy


    def verify_file_integrity(self, data, ext, header, footer):
        """
        Verifies file integrity using a heuristic score based on:
        - Whether the data starts with the expected header and ends with the expected footer.
        - The Shannon entropy of the data.
        - A minimal file size threshold.
        Each factor contributes to an overall score. Only files scoring above a threshold are considered intact.
        """
        header_ok = data.startswith(header)
        footer_ok = data.endswith(footer)
        entropy = self.compute_entropy(data)
        size = len(data)

        # Set thresholds based on file extension.
        if ext in ["jpg", "jpeg"]:
            # JPEG files are usually compressed with high entropy.
            entropy_ok = 7.0 <= entropy <= 8.0
            size_ok = size > 1024  # At least 1KB
        elif ext == "png":
            entropy_ok = 7.0 <= entropy <= 8.0
            size_ok = size > 1024
        elif ext == "pdf":
            # PDFs can vary; use a broad entropy range.
            entropy_ok = 4.5 <= entropy <= 8.0
            size_ok = size > 1024
        elif ext == "gif":
            entropy_ok = 3.5 <= entropy <= 7.0
            size_ok = size > 512
        elif ext == "zip":
            entropy_ok = 7.0 <= entropy <= 8.0
            size_ok = size > 1024
        else:
            entropy_ok = entropy >= 3.0
            size_ok = size > 256

        # Heuristic scoring: header and footer are strong signals.
        score = 0.0
        if header_ok:
            score += 0.4
        if footer_ok:
            score += 0.4
        if entropy_ok:
            score += 0.2
        if not size_ok:
            score = 0.0  # Disqualify if size is too small

        # For our purposes, a score of 0.7 or higher indicates the file is likely intact.
        # (This threshold can be adjusted as needed.)
        return score >= 0.7


    # --- Main Carving Function ---
    def carve_files(self, image_path, output_dir, signatures, gap_threshold=1024 * 1024):
        """
        Carves files from a disk image (or binary file) using provided file signatures.
        It handles both contiguous fragments and orphan fragments (which may be merged if gaps are small).
        Before writing out a recovered file, it verifies the file's integrity using header/footer matching
        and Shannon entropy.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(image_path, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            file_counter = 0

            for sig in signatures:
                ext = sig["extension"]
                header = sig["header"]
                footer = sig["footer"]
                print(f"\nProcessing file type: {ext} (header: {header}, footer: {footer})")
                fragments = self.get_fragments(mm, header, footer, gap_threshold)

                for frag in fragments:
                    start, end = frag
                    carved_data = mm[start:end]
                    # Verify file integrity using our custom heuristic.
                    if self.verify_file_integrity(carved_data, ext, header, footer):
                        file_counter += 1
                        output_filename = os.path.join(output_dir, f"recovered_{file_counter}.{ext}")
                        with open(output_filename, "wb") as outf:
                            outf.write(carved_data)
                        print(f"Recovered file: {output_filename} (offsets {start} to {end}, entropy: {self.compute_entropy(carved_data):.2f})")
                    else:
                        print(f"Fragment at offsets {start}-{end} for {ext} failed integrity check (entropy: {self.compute_entropy(carved_data):.2f}).")
            mm.close()
