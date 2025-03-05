import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import file_carver


class FileCarverApp:
    def __init__(self, master):
        self.master = master
        master.title("File Carver")

        self.drive_path = ""
        self.destination_path = ""
        self.found_files = []  # List to store found file fragments.

        self.create_widgets()

    def create_widgets(self):
        # --- Drive/Image selection ---
        drive_frame = ttk.Frame(self.master)
        drive_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(drive_frame, text="Drive/Image:").pack(side="left")
        self.drive_entry = ttk.Entry(drive_frame, width=50)
        self.drive_entry.pack(side="left", padx=5)
        ttk.Button(drive_frame, text="Browse", command=self.select_drive).pack(side="left")

        # --- Destination folder selection ---
        dest_frame = ttk.Frame(self.master)
        dest_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(dest_frame, text="Destination:").pack(side="left")
        self.dest_entry = ttk.Entry(dest_frame, width=50)
        self.dest_entry.pack(side="left", padx=5)
        ttk.Button(dest_frame, text="Browse", command=self.select_destination).pack(side="left")

        # --- Control buttons ---
        btn_frame = ttk.Frame(self.master)
        btn_frame.pack(padx=10, pady=5, fill="x")
        ttk.Button(btn_frame, text="Scan Drive", command=self.start_scan).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Recover Selected", command=self.recover_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save DB", command=self.save_db).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Load DB", command=self.load_db).pack(side="left", padx=5)

        # --- Treeview for displaying found files ---
        self.tree = ttk.Treeview(self.master, columns=("ID", "Type", "Offset", "Size", "Entropy"), show="headings", selectmode="extended")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Offset", text="Offset")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Entropy", text="Entropy")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def select_drive(self):
        path = filedialog.askopenfilename(title="Select Drive or Disk Image")
        if path:
            self.drive_path = path
            self.drive_entry.delete(0, tk.END)
            self.drive_entry.insert(0, path)

    def select_destination(self):
        path = filedialog.askdirectory(title="Select Destination Folder")
        if path:
            self.destination_path = path
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, path)

    def start_scan(self):
        if not self.drive_path:
            messagebox.showerror("Error", "Please select a drive/image file.")
            return
        # Start scanning in a separate thread.
        threading.Thread(target=self.scan_thread, daemon=True).start()

    def scan_thread(self):
        self.found_files = file_carver.scan_drive(self.drive_path)
        self.update_treeview()

    def update_treeview(self):
        # Clear the treeview.
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert each found file's details.
        for file_info in self.found_files:
            self.tree.insert("", tk.END, values=(file_info["id"], file_info["extension"], file_info["offset"], file_info["size"], f"{file_info['entropy']:.2f}"))

    def recover_selected(self):
        if not self.destination_path:
            messagebox.showerror("Error", "Please select a destination folder.")
            return
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select files to recover.")
            return
        for item in selected_items:
            file_info = self.tree.item(item, "values")
            fragment = {"id": int(file_info[0]), "extension": file_info[1], "offset": int(file_info[2]), "size": int(file_info[3])}
            recovered_path = file_carver.recover_fragment(self.drive_path, fragment, self.destination_path)
            print(f"Recovered: {recovered_path}")
        messagebox.showinfo("Info", "Recovery process initiated for selected files.")

    def save_db(self):
        if not self.found_files:
            messagebox.showerror("Error", "No files found to save.")
            return
        path = filedialog.asksaveasfilename(title="Save DB", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            with open(path, "w") as f:
                json.dump(self.found_files, f, indent=4)
            messagebox.showinfo("Info", f"Database saved to {path}")

    def load_db(self):
        path = filedialog.askopenfilename(title="Load DB", filetypes=[("JSON Files", "*.json")])
        if path:
            with open(path, "r") as f:
                self.found_files = json.load(f)
            self.update_treeview()
            messagebox.showinfo("Info", f"Loaded database from {path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileCarverApp(root)
    root.mainloop()
