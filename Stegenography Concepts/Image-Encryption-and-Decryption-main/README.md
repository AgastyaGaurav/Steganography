Key Points:

Encryption Script (encrypt_image.py):

Input: It takes the secret message and passcode as input.

Image Loading: It loads the image from the specified path (mypic.jpg).

Message Encryption: It encrypts the secret message into the image's pixel values.

Output: It saves the encrypted image as encryptedImage.jpg and also stores the passcode in passcode.txt for later use in decryption.

Passcode Storage: The passcode is saved to a file (passcode.txt) so that the decryption script can use it.



Decryption Script (decrypt_image.py):

Input: The user is prompted to enter the passcode for decryption.

Passcode Verification: It reads the passcode from passcode.txt (which was saved by the encryption script) and checks if the entered passcode is correct.

Image Loading: It loads the encrypted image (encryptedImage.jpg).

Message Decryption: If the passcode is correct, it decrypts the message from the image.

Output: It prints the decrypted message.

How to Use:
Encryption: Run the encrypt_image.py script to encrypt a message into an image. This will create an encrypted image and save the passcode to passcode.txt.
Decryption: Run the decrypt_image.py script, input the passcode, and the original secret message will be decrypted and printed.
