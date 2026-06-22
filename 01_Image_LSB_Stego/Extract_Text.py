from PIL import Image

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

    # Split into bytes
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]

        if len(byte) < 8:
            break

        chars.append(chr(int(byte, 2)))

        if ''.join(format(ord(c), '08b') for c in chars[-2:]) == '1111111111111110':
            return ''.join(chars[:-2])

    return ''.join(chars)

print(extract_message("stego.png"))
