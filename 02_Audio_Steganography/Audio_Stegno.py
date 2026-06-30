import os
import wave
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ---------------- CORE STEGANOGRAPHY LOGIC ----------------

def encode_audio(input_audio_path, output_audio_path, secret_message):
    song = wave.open(input_audio_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    secret_message += "###"
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    
    if len(binary_message) > len(frame_bytes):
        song.close()
        raise ValueError("Audio file is too small for this message!")

    for i, bit in enumerate(binary_message):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(bit)
        
    modified_frames = bytes(frame_bytes)

    with wave.open(output_audio_path, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(modified_frames)
        
    song.close()


def decode_audio(encoded_audio_path):
    song = wave.open(encoded_audio_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    extracted_bits = [str(frame_bytes[i] & 1) for i in range(len(frame_bytes))]
    extracted_bits = "".join(extracted_bits)

    all_bytes = [extracted_bits[i:i+8] for i in range(0, len(extracted_bits), 8)]

    decoded_message = ""
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if decoded_message.endswith("###"):
            break

    song.close()
    return decoded_message[:-3]


# ---------------- GUI APPLICATION ----------------

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Steganography Studio")
        self.root.geometry("550x400")
        self.root.resizable(False, False)
        
        # Create Tabs (Encode / Decode)
        tab_control = ttk.Notebook(root)
        
        self.encode_tab = ttk.Frame(tab_control)
        self.decode_tab = ttk.Frame(tab_control)
        
        tab_control.add(self.encode_tab, text='  Hide Message (Encode)  ')
        tab_control.add(self.decode_tab, text='  Extract Message (Decode)  ')
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.setup_encode_tab()
        self.setup_decode_tab()

    # --- Encode Tab Layout & Actions ---
    def setup_encode_tab(self):
        # File Selection
        ttk.Label(self.encode_tab, text="Select Carrier WAV File:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.encode_input_entry = ttk.Entry(self.encode_tab, width=40)
        self.encode_input_entry.grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(self.encode_tab, text="Browse", command=self.browse_encode_input).grid(row=0, column=2, padx=5, pady=10)

        # Secret Message Input
        ttk.Label(self.encode_tab, text="Enter Secret Message:").grid(row=1, column=0, sticky="nw", padx=10, pady=5)
        self.message_text = tk.Text(self.encode_tab, width=38, height=8, wrap="word")
        self.message_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Action Button
        self.encode_btn = ttk.Button(self.encode_tab, text="Encode and Save As...", command=self.process_encoding)
        self.encode_btn.grid(row=2, column=1, pady=20, sticky="e")

    def browse_encode_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Wav Files", "*.wav")])
        if file_path:
            self.encode_input_entry.delete(0, tk.END)
            self.encode_input_entry.insert(0, file_path)

    def process_encoding(self):
        input_file = self.encode_input_entry.get()
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid carrier WAV file.")
            return
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide.")
            return
            
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wav Files", "*.wav")])
        if output_file:
            try:
                encode_audio(input_file, output_file, message)
                messagebox.showinfo("Success", f"Message hidden successfully!\nSaved to: {os.path.basename(output_file)}")
                self.message_text.delete("1.0", tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # --- Decode Tab Layout & Actions ---
    def setup_decode_tab(self):
        # File Selection
        ttk.Label(self.decode_tab, text="Select Stego WAV File:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.decode_input_entry = ttk.Entry(self.decode_tab, width=40)
        self.decode_input_entry.grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(self.decode_tab, text="Browse", command=self.browse_decode_input).grid(row=0, column=2, padx=5, pady=10)

        # Decode Button
        ttk.Button(self.decode_tab, text="Extract Secret Message", command=self.process_decoding).grid(row=1, column=1, pady=10, sticky="w")

        # Result Output
        ttk.Label(self.decode_tab, text="Hidden Message:").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        self.result_text = tk.Text(self.decode_tab, width=38, height=8, wrap="word", state="disabled")
        self.result_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")

    def browse_decode_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Wav Files", "*.wav")])
        if file_path:
            self.decode_input_entry.delete(0, tk.END)
            self.decode_input_entry.insert(0, file_path)

    def process_decoding(self):
        input_file = self.decode_input_entry.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid audio file.")
            return
            
        try:
            hidden_msg = decode_audio(input_file)
            
            # Enable text box, clear old text, insert new text, disable text box (read-only)
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", hidden_msg if hidden_msg else "[No hidden message found or file corrupted]")
            self.result_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode audio. Reason: {str(e)}")


# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
