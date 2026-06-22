from PIL import Image

def hide_message(image_path, secret_message, output_path):
    img = Image.open(image_path)
    pixels = img.load()

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b')
                             for char in secret_message)
    binary_message += '1111111111111110'  # End marker

    data_index = 0
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            for i in range(3):  # R, G, B
                if data_index < len(binary_message):
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_message):
                img.save(output_path)
                return

    img.save(output_path)

hide_message("input.png", "HELLO", "stego.png")
