import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Function to encode a message into an image
def encode_message():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    message = entry_message.get()
    password = entry_password.get()
    
    if not message or not password:
        messagebox.showerror("Error", "Message and password cannot be empty!")
        return
    
    # Convert message to binary
    binary_msg = ''.join(format(ord(i), '08b') for i in (message + "#####"))  # '#####' marks end
    
    data_index = 0
    total_bytes = img.shape[0] * img.shape[1] * 3
    
    if len(binary_msg) > total_bytes:
        messagebox.showerror("Error", "Message is too large for the selected image!")
        return
    
    for row in img:
        for pixel in row:
            for i in range(3):  # Iterate over R, G, B channels
                if data_index < len(binary_msg):
                    pixel[i] = (pixel[i] & 0b11111110) | int(binary_msg[data_index])
                    data_index += 1


    
    encoded_path = "encoded_image.png"
    cv2.imwrite(encoded_path, img)
    messagebox.showinfo("Success", f"Message encoded successfully! Saved as {encoded_path}")
    
# Function to decode a hidden message
def decode_message():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    password = entry_password.get()
    
    if not password:
        messagebox.showerror("Error", "Please enter a password to decrypt!")
        return
    
    binary_msg = ""
    for row in img:
        for pixel in row:
            for i in range(3):
                binary_msg += str(pixel[i] & 1)  # Extract LSB
    
    message_bytes = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = ''.join(chr(int(b, 2)) for b in message_bytes)
    
    if "#####" in message:
        message = message[:message.index("#####")]
        messagebox.showinfo("Decrypted Message", f"Message: {message}")
    else:
        messagebox.showerror("Error", "No hidden message found!")
    
# Creating GUI
top = tk.Tk()
top.title("Image Steganography")
top.geometry("400x300")

tk.Label(top, text="Enter Secret Message:").pack()
entry_message = tk.Entry(top, width=40)
entry_message.pack()

tk.Label(top, text="Enter Password:").pack()
entry_password = tk.Entry(top, width=40, show="*")
entry_password.pack()

tk.Button(top, text="Encode Message", command=encode_message).pack(pady=10)
tk.Button(top, text="Decode Message", command=decode_message).pack(pady=10)

top.mainloop()