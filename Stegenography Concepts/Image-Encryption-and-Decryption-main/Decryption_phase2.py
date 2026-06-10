import cv2

# Dictionary for encryption and decryption
d = {}
c = {}

def initialize_dictionaries():
    """Initialize dictionaries for character-to-integer and integer-to-character mapping."""
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

def load_image(image_path):
    """Load the image from a file."""
    return cv2.imread(image_path)

def pixel_wrap(n, m, img):
    """Wrap the pixel index within the image bounds."""
    if m >= img.shape[1]:
        m = 0
        n += 1
    if n >= img.shape[0]:
        n = 0
        m = 0
    return n, m

def decrypt_message(img, length_of_message):
    """Decrypt a message from the image."""
    message = ""
    n, m, z = 0, 0, 0
    for i in range(length_of_message):
        message += c[img[n, m, z]]
        m += 1
        n, m = pixel_wrap(n, m, img)  # Ensure the pixel index wraps around if necessary
        z = (z + 1) % 3  # Move between the R, G, B channels
    return message

# Main Program Flow

# Get user input for the passcode
input_passcode = input("Enter passcode for Decryption: ")

# Load the passcode from the file (this step assumes the passcode was saved during encryption)
with open("passcode.txt", "r") as f:
    correct_passcode = f.read().strip()

# Check if the passcode is correct
if input_passcode == correct_passcode:
    # Load the encrypted image
    img = load_image("encryptedImage.jpg")  # Path to the encrypted image

    # Decrypt the message (assuming the length of the original message is known)
    message = decrypt_message(img, len(input_passcode))  # Here, length is passed for simplicity
    print("Decrypted message:", message)
else:
    print("Incorrect passcode. Decryption failed.")
