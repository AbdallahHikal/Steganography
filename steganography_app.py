import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os
import wave
import struct

ZWSP = '\u200b'
ZWNJ = '\u200c'
END_MARKER = "#####END#####"

DEEGGER_LNK_PATH = r"C:\Users\User\OneDrive - Benha University (Faculty Of Computers & Information Technolgy)\Desktop\project\video tools\DeEgger Embedder.lnk"
SILENTEYE_LNK_PATH = r"C:\Users\User\OneDrive - Benha University (Faculty Of Computers & Information Technolgy)\Desktop\project\video tools\SilentEye.lnk"

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Application")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        window_width = 900
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)
        
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#1A1A1A")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(self.main_frame, text="Select File Type", font=("Roboto", 28, "bold"), text_color="#FFFFFF").pack(pady=30)
        
        button_style = {"font": ("Roboto", 16), "corner_radius": 15, "fg_color": "#00D4FF", "hover_color": "#33E4FF", "text_color": "#1A1A1A"}
        ctk.CTkButton(self.main_frame, text="Image", command=self.open_image_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Video", command=self.open_video_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Text", command=self.open_text_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Audio", command=self.open_audio_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def open_image_window(self):
        self.clear_frame(self.main_frame)
        
        # Create scrollable frame for image options
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#1A1A1A")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="Image Steganography", font=("Roboto", 24, "bold"), text_color="#FFFFFF").pack(pady=20)
        
        ctk.CTkButton(scroll_frame, text="Select Image", command=self.select_image, font=("Roboto", 14), corner_radius=10, fg_color="#00D4FF", hover_color="#33E4FF", text_color="#1A1A1A").pack(pady=10)
        
        self.image_path_label = ctk.CTkLabel(scroll_frame, text="No image selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.image_path_label.pack()
        
        ctk.CTkLabel(scroll_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.message_entry = ctk.CTkEntry(scroll_frame, width=600, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.message_entry.pack()
        
        ctk.CTkLabel(scroll_frame, text="Technique:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.technique = ctk.CTkOptionMenu(scroll_frame, values=["LSB", "Parity", "BitPlane"], font=("Roboto", 14))
        self.technique.set("LSB")
        self.technique.pack()
        
        ctk.CTkButton(scroll_frame, text="Hide Message", command=self.hide_image_message, font=("Roboto", 14), corner_radius=10, fg_color="#28A745", hover_color="#3CC45F", text_color="#FFFFFF").pack(pady=10)
        ctk.CTkButton(scroll_frame, text="Extract Message", command=self.extract_image_message, font=("Roboto", 14), corner_radius=10, fg_color="#FFC107", hover_color="#FFDB58", text_color="#1A1A1A").pack(pady=10)
        
        # SilentEye integration
        ctk.CTkLabel(scroll_frame, text="─── SilentEye Tool ───", font=("Roboto", 12), text_color="#888888").pack(pady=15)
        ctk.CTkButton(scroll_frame, text="Open SilentEye (Image)", command=self.open_silenteye, font=("Roboto", 14), corner_radius=10, fg_color="#9C27B0", hover_color="#BA68C8", text_color="#FFFFFF").pack(pady=5)
        
        ctk.CTkButton(scroll_frame, text="Back", command=self.back_to_main, font=("Roboto", 14), corner_radius=10, fg_color="#6C757D", hover_color="#ADB5BD", text_color="#FFFFFF").pack(pady=20)

    def open_audio_window(self):
        self.clear_frame(self.main_frame)
        
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#1A1A1A")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="Audio Steganography", font=("Roboto", 24, "bold"), text_color="#FFFFFF").pack(pady=20)
        
        ctk.CTkButton(scroll_frame, text="Select Audio (WAV)", command=self.select_audio, font=("Roboto", 14), corner_radius=10, fg_color="#00D4FF", hover_color="#33E4FF", text_color="#1A1A1A").pack(pady=10)
        
        self.audio_path_label = ctk.CTkLabel(scroll_frame, text="No audio selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.audio_path_label.pack()
        
        ctk.CTkLabel(scroll_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.audio_message_entry = ctk.CTkEntry(scroll_frame, width=600, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.audio_message_entry.pack()
        
        ctk.CTkLabel(scroll_frame, text="Technique:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.audio_technique = ctk.CTkOptionMenu(scroll_frame, values=["LSB", "Parity", "Phase", "Echo"], font=("Roboto", 14))
        self.audio_technique.set("LSB")
        self.audio_technique.pack()
        
        ctk.CTkButton(scroll_frame, text="Hide Message", command=self.hide_audio_message, font=("Roboto", 14), corner_radius=10, fg_color="#28A745", hover_color="#3CC45F", text_color="#FFFFFF").pack(pady=10)
        ctk.CTkButton(scroll_frame, text="Extract Message", command=self.extract_audio_message, font=("Roboto", 14), corner_radius=10, fg_color="#FFC107", hover_color="#FFDB58", text_color="#1A1A1A").pack(pady=10)
        
        # SilentEye integration
        ctk.CTkLabel(scroll_frame, text="─── SilentEye Tool ───", font=("Roboto", 12), text_color="#888888").pack(pady=15)
        ctk.CTkButton(scroll_frame, text="Open SilentEye (Audio)", command=self.open_silenteye, font=("Roboto", 14), corner_radius=10, fg_color="#9C27B0", hover_color="#BA68C8", text_color="#FFFFFF").pack(pady=5)
        
        ctk.CTkButton(scroll_frame, text="Back", command=self.back_to_main, font=("Roboto", 14), corner_radius=10, fg_color="#6C757D", hover_color="#ADB5BD", text_color="#FFFFFF").pack(pady=20)

    def open_video_window(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(self.main_frame, text="Video Steganography (DeEgger)", font=("Roboto", 24, "bold"), text_color="#FFFFFF").pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Select Video", command=self.select_video, font=("Roboto", 14), corner_radius=10, fg_color="#00D4FF", hover_color="#33E4FF", text_color="#1A1A1A").pack(pady=10)
        self.video_path_label = ctk.CTkLabel(self.main_frame, text="No video selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.video_path_label.pack()
        ctk.CTkLabel(self.main_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.video_message_entry = ctk.CTkEntry(self.main_frame, width=600, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.video_message_entry.pack()
        ctk.CTkButton(self.main_frame, text="Hide in Video (DeEgger)", command=self.hide_video_message, font=("Roboto", 14), corner_radius=10, fg_color="#28A745", hover_color="#3CC45F", text_color="#FFFFFF").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Extract from Video (DeEgger)", command=self.extract_video_message, font=("Roboto", 14), corner_radius=10, fg_color="#FFC107", hover_color="#FFDB58", text_color="#1A1A1A").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Back", command=self.back_to_main, font=("Roboto", 14), corner_radius=10, fg_color="#6C757D", hover_color="#ADB5BD", text_color="#FFFFFF").pack(pady=10)

    def open_text_window(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(self.main_frame, text="Text Steganography", font=("Roboto", 24, "bold"), text_color="#FFFFFF").pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Select Text File", command=self.select_text_file, font=("Roboto", 14), corner_radius=10, fg_color="#00D4FF", hover_color="#33E4FF", text_color="#1A1A1A").pack(pady=10)
        self.text_path_label = ctk.CTkLabel(self.main_frame, text="No text file selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.text_path_label.pack()
        ctk.CTkLabel(self.main_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.text_message_entry = ctk.CTkEntry(self.main_frame, width=600, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.text_message_entry.pack()
        ctk.CTkLabel(self.main_frame, text="Technique:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.text_technique = ctk.CTkOptionMenu(self.main_frame, values=["ZW", "Parity", "Whitespace"], font=("Roboto", 14))
        self.text_technique.set("ZW")
        self.text_technique.pack()
        ctk.CTkButton(self.main_frame, text="Hide Message", command=self.hide_text_message, font=("Roboto", 14), corner_radius=10, fg_color="#28A745", hover_color="#3CC45F", text_color="#FFFFFF").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Extract Message", command=self.extract_text_message, font=("Roboto", 14), corner_radius=10, fg_color="#FFC107", hover_color="#FFDB58", text_color="#1A1A1A").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Back", command=self.back_to_main, font=("Roboto", 14), corner_radius=10, fg_color="#6C757D", hover_color="#ADB5BD", text_color="#FFFFFF").pack(pady=10)

    def back_to_main(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(self.main_frame, text="Select File Type", font=("Roboto", 28, "bold"), text_color="#FFFFFF").pack(pady=30)
        button_style = {"font": ("Roboto", 16), "corner_radius": 15, "fg_color": "#00D4FF", "hover_color": "#33E4FF", "text_color": "#1A1A1A"}
        ctk.CTkButton(self.main_frame, text="Image", command=self.open_image_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Video", command=self.open_video_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Text", command=self.open_text_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Audio", command=self.open_audio_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.image_path_label.configure(text=os.path.basename(file_path))

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.video_path = file_path
            self.video_path_label.configure(text=os.path.basename(file_path))

    def select_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.text_path = file_path
            self.text_path_label.configure(text=os.path.basename(file_path))

    def select_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.audio_path = file_path
            self.audio_path_label.configure(text=os.path.basename(file_path))

    def open_silenteye(self):
        """Opens SilentEye application for image/audio steganography"""
        if os.path.exists(SILENTEYE_LNK_PATH):
            try:
                os.startfile(SILENTEYE_LNK_PATH)
                messagebox.showinfo("SilentEye", "SilentEye opened successfully!\n\nUse SilentEye to:\n• Hide messages in images and audio\n• Extract hidden messages\n• Use password protection\n• Apply encryption")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open SilentEye: {e}")
        else:
            messagebox.showerror("Error", "SilentEye shortcut not found!\n\nPlease update SILENTEYE_LNK_PATH in the code.")

    def build_binary_with_header(self, message):
        length = len(message.encode('utf-8'))
        header = format(length, '032b')
        payload = ''.join(format(b, '08b') for b in message.encode('utf-8'))
        return header + payload

    def bits_to_message_by_length(self, bits, byte_length):
        needed = byte_length * 8
        if len(bits) < needed:
            return None
        message = ''
        for i in range(0, needed, 8):
            byte = bits[i:i+8]
            message += chr(int(byte, 2))
        try:
            return bytes([ord(c) for c in message]).decode('utf-8', errors='replace')
        except Exception:
            return message

    # IMAGE METHODS
    def hide_image_message(self):
        if not hasattr(self, "image_path"):
            messagebox.showerror("Error", "Please select an image!")
            return
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        technique = self.technique.get()
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "output_image.png")
        try:
            img = Image.open(self.image_path).convert("RGB")
            if technique == "LSB":
                self.hide_lsb_image(img, message, output_path)
            elif technique == "Parity":
                self.hide_parity_image(img, message, output_path)
            else:
                self.hide_bitplane_image(img, message, output_path)
            messagebox.showinfo("Success", f"Message hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_image_message(self):
        if not hasattr(self, "image_path"):
            messagebox.showerror("Error", "Please select an image!")
            return
        technique = self.technique.get()
        try:
            img = Image.open(self.image_path).convert("RGB")
            if technique == "LSB":
                message = self.extract_lsb_image(img)
            elif technique == "Parity":
                message = self.extract_parity_image(img)
            else:
                message = self.extract_bitplane_image(img)
            messagebox.showinfo("Extracted Message", message or "No message found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hide_lsb_image(self, img, message, output_path):
        bits = self.build_binary_with_header(message)
        pixels = np.array(img, dtype=np.uint8).copy()
        flat_pixels = pixels.ravel()
        if len(bits) > len(flat_pixels):
            raise ValueError("Message too large for image")
        for i, bit in enumerate(bits):
            flat_pixels[i] = (int(flat_pixels[i]) & 0xFE) | int(bit)
        pixels = flat_pixels.reshape(pixels.shape)
        Image.fromarray(pixels).save(output_path)

    def extract_lsb_image(self, img):
        flat = np.array(img, dtype=np.uint8).ravel()
        bits = ''.join(str(int(x) & 1) for x in flat)
        if len(bits) < 32: return ''
        header_bits = bits[:32]
        length = int(header_bits, 2)
        total_bits_needed = 32 + length * 8
        if len(bits) < total_bits_needed:
            return ''
        message_bits = bits[32:32 + length * 8]
        return self.bits_to_message_by_length(message_bits, length)

    def hide_parity_image(self, img, message, output_path):
        bits = self.build_binary_with_header(message)
        pixels = np.array(img, dtype=np.uint8).copy()
        flat = pixels.ravel()
        if len(bits) > len(flat):
            raise ValueError("Message too large for image")
        for i, bit in enumerate(bits):
            b = int(flat[i])
            parity = bin(b).count('1') % 2
            if parity != int(bit):
                flat[i] ^= 1
        pixels = flat.reshape(pixels.shape)
        Image.fromarray(pixels).save(output_path)

    def extract_parity_image(self, img):
        flat = np.array(img, dtype=np.uint8).ravel()
        bits = ''.join(str(bin(int(x)).count('1') % 2) for x in flat)
        if len(bits) < 32: return ''
        header_bits = bits[:32]
        length = int(header_bits, 2)
        total_bits_needed = 32 + length * 8
        if len(bits) < total_bits_needed:
            return ''
        message_bits = bits[32:32 + length * 8]
        return self.bits_to_message_by_length(message_bits, length)

    def hide_bitplane_image(self, img, message, output_path, plane=1):
        bits = self.build_binary_with_header(message)
        pixels = np.array(img, dtype=np.int32).copy()
        flat = pixels.ravel()
        if len(bits) > len(flat):
            raise ValueError("Message too large for image")
        for i, bit in enumerate(bits):
            mask = 1 << plane
            if int(bit) == 1:
                flat[i] = int(flat[i]) | mask
            else:
                flat[i] = int(flat[i]) & (~mask)
        pixels = flat.reshape(pixels.shape)
        pixels = np.clip(pixels, 0, 255).astype(np.uint8)
        Image.fromarray(pixels).save(output_path)

    def extract_bitplane_image(self, img, plane=1):
        flat = np.array(img, dtype=np.uint8).ravel()
        bits = ''.join(str((int(b) >> plane) & 1) for b in flat)
        if len(bits) < 32: return ''
        length = int(bits[:32], 2)
        total = 32 + length * 8
        if len(bits) < total:
            return ''
        message_bits = bits[32:32 + length * 8]
        return self.bits_to_message_by_length(message_bits, length)

    # VIDEO METHODS
    def hide_video_message(self):
        if not hasattr(self, "video_path"):
            messagebox.showerror("Error", "Please select a video!")
            return
        message = self.video_message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        try:
            msg_file = self.create_message_file(message)
            self.open_deegger()
            info = ("DeEgger opened.\n\nIn DeEgger choose:\n"
                    f"Host file  → {self.video_path}\n"
                    f"Embed file → {msg_file}\n\nThen run Embed.")
            messagebox.showinfo("Open DeEgger", info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_video_message(self):
        extracted_path = filedialog.askopenfilename(title="Select extracted .txt from DeEgger", filetypes=[("Text files", "*.txt")])
        if not extracted_path:
            return
        try:
            msg = self.read_extracted_message(extracted_path)
            messagebox.showinfo("Extracted message", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_deegger(self):
        if os.path.exists(DEEGGER_LNK_PATH):
            try:
                os.startfile(DEEGGER_LNK_PATH)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open DeEgger: {e}")
        else:
            messagebox.showerror("Error", "DeEgger shortcut not found at configured path.")

    def create_message_file(self, message, output_path="embedded_message.txt"):
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        out = os.path.join(output_dir, output_path)
        with open(out, "w", encoding="utf-8") as f:
            f.write(message)
        return out

    def read_extracted_message(self, path):
        if not os.path.exists(path):
            return "Extracted message file not found!"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # TEXT METHODS
    def hide_text_message(self):
        if not hasattr(self, "text_path"):
            messagebox.showerror("Error", "Please select a text file!")
            return
        message = self.text_message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        technique = self.text_technique.get()
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "output_text.txt")
        try:
            with open(self.text_path, "r", encoding="utf-8") as f:
                cover_text = f.read()
            if technique == "ZW":
                hidden_text = self.hide_zw_text(cover_text, message)
            elif technique == "Parity":
                hidden_text = self.hide_parity_text(cover_text, message)
            else:
                hidden_text = self.hide_whitespace_text(cover_text, message)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(hidden_text)
            messagebox.showinfo("Success", f"Message hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_text_message(self):
        if not hasattr(self, "text_path"):
            messagebox.showerror("Error", "Please select a text file!")
            return
        technique = self.text_technique.get()
        try:
            with open(self.text_path, "r", encoding="utf-8") as f:
                text = f.read()
            if technique == "ZW":
                message = self.extract_zw_text(text)
            elif technique == "Parity":
                message = self.extract_parity_text(text)
            else:
                message = self.extract_whitespace_text(text)
            messagebox.showinfo("Extracted Message", message or "No message found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hide_zw_text(self, cover_text, message):
        message += "\0"
        bits = ''.join(format(ord(c), '08b') for c in message)
        result = list(cover_text)
        insert_pos = 0
        for bit in bits:
            while insert_pos < len(result) and result[insert_pos] == ' ':
                insert_pos += 1
            if insert_pos >= len(result):
                raise ValueError("Cover text too short")
            zw = ZWSP if bit == '1' else ZWNJ
            result.insert(insert_pos+1, zw)
            insert_pos += 2
        return ''.join(result)

    def extract_zw_text(self, text):
        bits = []
        for ch in text:
            if ch == ZWSP: bits.append('1')
            elif ch == ZWNJ: bits.append('0')
            if len(bits) % 8 == 0 and len(bits) > 0:
                byte = ''.join(bits[-8:])
                c = chr(int(byte, 2))
                if c == '\0':
                    whole = ''.join(chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits)-8, 8))
                    return whole
        return ''

    def hide_parity_text(self, cover_text, message):
        message += "\0"
        bits = ''.join(format(ord(c), '08b') for c in message)
        result = ''
        bit_index = 0
        word_count = 0
        for ch in cover_text:
            result += ch
            if ch in ' \n' and bit_index < len(bits):
                word_count += 1
                parity = word_count % 2
                if parity != int(bits[bit_index]):
                    result += ZWSP
                bit_index += 1
        if bit_index < len(bits):
            raise ValueError("Cover text too short")
        return result

    def extract_parity_text(self, text):
        bits = ''
        word_count = 0
        i = 0
        while i < len(text):
            if text[i] in ' \n':
                word_count += 1
                parity = word_count % 2
                if i + 1 < len(text) and text[i+1] == ZWSP:
                    parity = 1 - parity
                    i += 1
                bits += str(parity)
                if len(bits) % 8 == 0:
                    c = chr(int(bits[-8:], 2))
                    if c == '\0':
                        return ''.join(chr(int(bits[j:j+8], 2)) for j in range(0, len(bits)-8, 8))
            i += 1
        return ''

    def hide_whitespace_text(self, cover_text, message):
        message += "\0"
        bits = ''.join(format(ord(c), '08b') for c in message)
        lines = cover_text.splitlines(True)
        if len(bits) > len(lines):
            raise ValueError("Not enough lines in cover text")
        out = ''
        for i, line in enumerate(lines):
            if i < len(bits):
                out += line.rstrip('\n')
                out += ('\t' if bits[i] == '1' else ' ')
                out += '\n' if line.endswith('\n') else ''
            else:
                out += line
        return out

    def extract_whitespace_text(self, text):
        lines = text.splitlines()
        bits = ''
        for line in lines:
            if line.endswith('\t'):
                bits += '1'
            elif line.endswith(' '):
                bits += '0'
            if len(bits) % 8 == 0 and len(bits) > 0:
                c = chr(int(bits[-8:], 2))
                if c == '\0':
                    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits)-8, 8))
        return ''

    # AUDIO METHODS
    def hide_audio_message(self):
        if not hasattr(self, "audio_path"):
            messagebox.showerror("Error", "Please select an audio file (WAV)!")
            return
        message = self.audio_message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        technique = self.audio_technique.get()
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "output_audio.wav")
        try:
            if technique == 'LSB':
                self.hide_lsb_audio(self.audio_path, message, output_path)
            elif technique == 'Parity':
                self.hide_parity_audio(self.audio_path, message, output_path)
            elif technique == 'Phase':
                self.hide_phase_audio(self.audio_path, message, output_path)
            else: 
                self.hide_echo_audio(self.audio_path, message, output_path,delay_samples=120)    
            messagebox.showinfo("Success", f"Message hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_audio_message(self):
        if not hasattr(self, "audio_path"):
            messagebox.showerror("Error", "Please select an audio file (WAV)!")
            return

        technique = self.audio_technique.get()
        try:
            if technique == 'LSB':
                message = self.extract_lsb_audio(self.audio_path)
            elif technique == 'Parity':
                message = self.extract_parity_audio(self.audio_path)
            elif technique == 'Phase':
                message = self.extract_phase_audio(self.audio_path)
            else:  # Echo
                message = self.extract_echo_audio(self.audio_path)

            messagebox.showinfo("Extracted Message", message or "No message found")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def hide_lsb_audio(self, wav_path, message, output_path):
        bits = self.build_binary_with_header(message)
        with wave.open(wav_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())
        samples = bytearray(frames)
        if len(bits) > len(samples):
            raise ValueError('Message too long for audio')
        for i, bit in enumerate(bits):
            samples[i] = (samples[i] & 0xFE) | int(bit)
        with wave.open(output_path, 'wb') as wf:
            wf.setparams(params)
            wf.writeframes(bytes(samples))

    def extract_lsb_audio(self, wav_path):
        with wave.open(wav_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())
        samples = bytearray(frames)
        bits = ''.join(str(samples[i] & 1) for i in range(len(samples)))
        if len(bits) < 32: return ''
        length = int(bits[:32], 2)
        total = 32 + length * 8
        if len(bits) < total: return ''
        message_bits = bits[32:32 + length * 8]
        return self.bits_to_message_by_length(message_bits, length)

    def hide_parity_audio(self, wav_path, message, output_path):
        bits = self.build_binary_with_header(message)
        with wave.open(wav_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())
        samples = bytearray(frames)
        if len(bits) > len(samples): raise ValueError('Message too long')
        for i, bit in enumerate(bits):
            parity = bin(samples[i]).count('1') % 2
            if parity != int(bit): samples[i] ^= 1
        with wave.open(output_path, 'wb') as wf:
            wf.setparams(params)
            wf.writeframes(bytes(samples))

    def extract_parity_audio(self, wav_path):
        with wave.open(wav_path, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
        samples = bytearray(frames)
        bits = ''.join(str(bin(s).count('1') % 2) for s in samples)
        if len(bits) < 32: return ''
        length = int(bits[:32], 2)
        total = 32 + length * 8
        if len(bits) < total: return ''
        message_bits = bits[32:32 + length * 8]
        return self.bits_to_message_by_length(message_bits, length)

    # ------------------ Phase Encoding (supports mono 16-bit WAV) ------------------
    def hide_phase_audio(self, wav_path, message, output_path):
        bits = self.build_binary_with_header(message + "")
        try:
            with wave.open(wav_path, 'rb') as wav:
                params = wav.getparams()
                n_channels, sampwidth, framerate, n_frames, comptype, compname = params
                frames = wav.readframes(n_frames)
                if sampwidth != 2:
                    raise ValueError("Only 16-bit PCM WAV supported.")
                audio = np.frombuffer(frames, dtype=np.int16)
                # Convert stereo -> mono by averaging channels if needed
                if n_channels > 1:
                    audio = audio.reshape(-1, n_channels)
                    audio = np.mean(audio, axis=1).astype(np.int16)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading WAV file: {e}")
            return

        if len(bits) > audio.size // 2:
            messagebox.showerror("Error", "Message too large for this audio file.")
            return

        audio_fft = np.fft.fft(audio)
        magnitude = np.abs(audio_fft)
        phase = np.angle(audio_fft)

        max_bins = len(phase)//2
        if len(bits) > max_bins:
            messagebox.showerror("Error", "Message too large for available phase bins.")
            return

        for i, bit in enumerate(bits, start=1):
            phase[i] = 0.0 if bit == '0' else (np.pi / 2)
            phase[-i] = -phase[i]

        modified_fft = magnitude * np.exp(1j * phase)
        modified_audio = np.fft.ifft(modified_fft).real
        modified_audio = np.round(modified_audio).astype(np.int16)

        # write as mono (1 channel)
        try:
            with wave.open(output_path, 'wb') as out_wav:
                out_wav.setparams((1, 2, framerate, len(modified_audio), comptype, compname))
                out_wav.writeframes(modified_audio.tobytes())
            messagebox.showinfo("Success", f"Message hidden successfully in {output_path} (Phase Encoding).")
        except Exception as e:
            messagebox.showerror("Error", f"Error writing WAV file: {e}")

    def extract_phase_audio(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wav:
                n_channels, sampwidth, framerate, n_frames, comptype, compname = wav.getparams()
                frames = wav.readframes(n_frames)
                if sampwidth != 2:
                    raise ValueError("Only 16-bit PCM WAV supported.")
                audio = np.frombuffer(frames, dtype=np.int16)
                if n_channels > 1:
                    audio = audio.reshape(-1, n_channels)
                    audio = np.mean(audio, axis=1).astype(np.int16)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading WAV file: {e}")
            return "Error reading file"

        audio_fft = np.fft.fft(audio)
        phase = np.angle(audio_fft)

        max_bins = len(phase)//2
        raw_bits = []
        for i in range(1, max_bins):
            p = phase[i]
            if abs(p) < (np.pi/4):
                raw_bits.append('0')
            elif abs(abs(p) - (np.pi/2)) < (np.pi/4):
                raw_bits.append('1')
            else:
                raw_bits.append('0')

        if len(raw_bits) < 32:
            return ''

        header_bits = ''.join(raw_bits[:32])
        length = int(header_bits, 2)
        total_needed = 32 + length * 8
        if len(raw_bits) < total_needed:
            return ''
        payload_bits = ''.join(raw_bits[32:32 + length * 8])
        return self.bits_to_message_by_length(payload_bits, length)
    
    def hide_echo_audio(self, wav_path, message, output_path, delay_samples=120):
        # "Echo-like" method: تستخدم زوج من العينات بينهم delay لتخزين البِت
        message += "\0"
        bits = "".join(format(ord(c), "08b") for c in message)

        with wave.open(wav_path, "rb") as wf:
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())

        if params.sampwidth != 2:
            raise ValueError("Echo method expects 16-bit PCM WAV")

        fmt = "<" + "h" * (len(frames) // 2)
        samples = np.array(struct.unpack(fmt, frames), dtype=np.int16)

        step = delay_samples + 2
        max_bits = len(samples) // step
        if len(bits) > max_bits:
            raise ValueError("Message too long for audio (echo)")

        for i, bit in enumerate(bits):
            p = i * step
            idx = p + delay_samples
            if idx >= len(samples):
                break
            if bit == "1":
                samples[idx] = samples[p]
            else:
                samples[idx] = -samples[p]

        packed = struct.pack(fmt, *samples.tolist())
        with wave.open(output_path, "wb") as wf:
            wf.setparams(params)
            wf.writeframes(packed)

    def extract_echo_audio(self, wav_path, delay_samples=120):
        with wave.open(wav_path, "rb") as wf:
            n_channels, sampwidth, framerate, n_frames = wf.getparams()[:4]
            frames = wf.readframes(n_frames)

        if sampwidth != 2:
            raise ValueError("Echo method expects 16-bit PCM WAV")

        fmt = "<" + "h" * (len(frames) // 2)
        samples = np.array(struct.unpack(fmt, frames), dtype=np.int16)

        step = delay_samples + 2
        nbits = len(samples) // step
        bits = ""

        for i in range(nbits):
            p = i * step
            idx = p + delay_samples
            if idx >= len(samples):
                break
            a = int(samples[p])
            b = int(samples[idx])

            if a == 0 or b == 0:
                bit = "0"
            else:
                same_sign = (a >= 0 and b >= 0) or (a < 0 and b < 0)
                bit = "1" if same_sign else "0"

            bits += bit
            if len(bits) >= 8 and bits.endswith("00000000"):
                break

        message = ""
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            if len(byte) < 8:
                break
            c = chr(int(byte, 2))
            if c == "\0":
                return message
            message += c
        return message

    
if __name__ == "__main__":
    root = ctk.CTk()
    app = SteganographyApp(root)
    root.mainloop()
