from PIL import Image
import os

def numberToBinary(num):
    return format(num, '08b')

def binaryToNumber(bin):
    return int(bin, 2)

def encode(img, msg):
    pixels = img.load()
    width, height = img.size
    msgLength = len(msg)
    
    red, green, blue = pixels[0, 0]
    pixels[0, 0] = (msgLength, green, blue)

    binary_message = ''.join([numberToBinary(ord(char)) for char in msg])
    pixel_index = 0
    message_index = 0
    
    for i in range(msgLength * 8):
        x = pixel_index % width
        y = pixel_index // width
        
        red, green, blue = pixels[x, y]
        
        if i % 8 == 0:
            letterBinary = binary_message[message_index:message_index+8]
            green_binary = numberToBinary(green)[:7] + letterBinary[0]
            blue_binary = numberToBinary(blue)[:7] + letterBinary[1]
            red_binary = numberToBinary(red)[:7] + letterBinary[2]
            message_index += 3
        else:
            green_binary = numberToBinary(green)[:7] + letterBinary[3]
            blue_binary = numberToBinary(blue)[:7] + letterBinary[4]
            red_binary = numberToBinary(red)[:7] + letterBinary[5]

        pixels[x, y] = (binaryToNumber(red_binary), binaryToNumber(green_binary), binaryToNumber(blue_binary))
        
        pixel_index += 1

    img.save("encoded_image.png", 'PNG')

def decode(img):
    pixels = img.load()
    width, height = img.size
    red, green, blue = pixels[0, 0]
    msgLength = red
    binary_message = ""
    
    pixel_index = 1
    while len(binary_message) < msgLength * 8:
        x = pixel_index % width
        y = pixel_index // width
        
        red, green, blue = pixels[x, y]
        
        red_binary = numberToBinary(red)[7]
        green_binary = numberToBinary(green)[7]
        blue_binary = numberToBinary(blue)[7]

        binary_message += red_binary + green_binary + blue_binary
        
        pixel_index += 1

    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        decoded_message += chr(binaryToNumber(byte))

    return decoded_message

def main():
    choice = input("Do you want to (e)ncode or (d)ecode a message? ").strip().lower()
    
    if choice == 'e':
        image_path = input("Enter the path of the image to encode into: ")
        message = input("Enter the message to encode: ")
        
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print("Error: The specified image file was not found.")
            return
        
        encode(img, message)
        print("Message encoded and saved in 'encoded_image.png'.")

    elif choice == 'd':
        image_path = input("Enter the path of the encoded image: ")
        
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print("Error: The specified image file was not found.")
            return
        
        decoded_message = decode(img)
        print("Decoded message: ", decoded_message)

    else:
        print("Invalid choice. Please choose either 'e' for encoding or 'd' for decoding.")

if __name__ == '__main__':
    main()
