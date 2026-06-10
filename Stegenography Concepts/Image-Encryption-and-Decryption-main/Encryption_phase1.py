import cv2
import os

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

def save_image(image, output_path):
    """Save the modified image to a file."""
    cv2.imwrite(output_path, image)

def pixel_wrap(n, m, img):
    """Wrap the pixel index within the image bounds."""
    if m >= img.shape[1]:
        m = 0
        n += 1
    if n >= img.shape[0]:
        n = 0
        m = 0
    return n, m

def encrypt_message(img, msg):
    """Encrypt a message into the image."""
    n, m, z = 0, 0, 0
    for i in range(len(msg)):
        # Encrypt each character and store it in the image
        img[n, m, z] = d[msg[i]] % 256  # Ensure pixel values are within the 0-255 range
        m += 1
        n, m = pixel_wrap(n, m, img)  # Ensure the pixel index wraps around if necessary
        z = (z + 1) % 3  # Move between the R, G, B channels
    return img

# Main Program Flow

# Get user input for secret message and passcode
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Initialize the dictionaries for encryption/decryption
initialize_dictionaries()

# Load the image
img = load_image("mypic.jpg")  # Replace with the correct image path

# Ensure the message fits within the image's pixel space
if len(msg) > img.shape[0] * img.shape[1] * 3:
    print("Message is too long for the image!")
    exit()

# Encrypt the message into the image
img = encrypt_message(img, msg)

# Save the encrypted image and open it
save_image(img, "encryptedImage.jpg")
os.system("start encryptedImage.jpg")  # Open the image (Windows command)

# Save the passcode in a file for later use (optional)
with open("passcode.txt", "w") as f:
    f.write(password)

print("Encryption completed and saved as encryptedImage.jpg.")
