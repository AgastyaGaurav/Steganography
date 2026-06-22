# Initial Step Installing the Open Lib Pillow 
# bash Command
pip install pillow

from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image

# ---------------- STEGANOGRAPHY BACKEND ---------------- #

def hide_message(image_path, secret_message, output_path):
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_message += '1111111111111110'  # End marker

    data_index = 0
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_message):
                img.save(output_path)
                return True

    return False


def extract_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()

    binary_data = ""
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            for i in range(3):
                binary_data += str(pixel[i] & 1)

    message = ""

    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]

        if len(byte) < 8:
            break

        char = chr(int(byte, 2))
        message += char

        if message.endswith(chr(255) + chr(254)):
            return message[:-2]

    return message

# ---------------- GUI FUNCTIONS ---------------- #

selected_image = ""


def browse_image():
    global selected_image
    selected_image = filedialog.askopenfilename(
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
    )

    if selected_image:
        image_label.config(text=selected_image)


def encode_data():
    if not selected_image:
        messagebox.showerror("Error", "Select an image first")
        return

    secret_text = text_box.get("1.0", END).strip()

    if not secret_text:
        messagebox.showerror("Error", "Enter a secret message")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")]
    )

    if save_path:
        success = hide_message(selected_image, secret_text, save_path)

        if success:
            messagebox.showinfo("Success", "Message hidden successfully!")
        else:
            messagebox.showerror("Error", "Image too small!")


def decode_data():
    if not selected_image:
        messagebox.showerror("Error", "Select an image first")
        return

    try:
        secret = extract_message(selected_image)

        result_box.delete("1.0", END)
        result_box.insert(END, secret)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- GUI DESIGN ---------------- #

root = Tk()
root.title("Image LSB Steganography")
root.geometry("700x500")
root.resizable(False, False)

title = Label(
    root,
    text="Image LSB Steganography",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

Button(
    root,
    text="Browse Image",
    command=browse_image,
    width=20,
    bg="lightblue"
).pack()

image_label = Label(root, text="No Image Selected", fg="blue")
image_label.pack(pady=5)

Label(root, text="Enter Secret Message").pack()

text_box = Text(root, height=8, width=60)
text_box.pack(pady=5)

Button(
    root,
    text="Hide Message",
    command=encode_data,
    width=20,
    bg="lightgreen"
).pack(pady=5)

Button(
    root,
    text="Extract Message",
    command=decode_data,
    width=20,
    bg="orange"
).pack(pady=5)

Label(root, text="Extracted Message").pack()

result_box = Text(root, height=8, width=60)
result_box.pack(pady=5)

root.mainloop()
