import easyocr
import cv2
import os
import parse
import convert

# Constants
png_output = 'output.png'
output_file = 'output.txt'

def start_ocr(photobyte):
    try:
        # Convert byte_array to PNG and save it as output.png
        convert.bytearray_to_png(photobyte)

        # Initialize the EasyOCR Reader with the Romanian language
        reader = easyocr.Reader(['ro'])

        # Replace 'output.png' with the path to your image file
        image_path = cv2.imread(png_output, 0) 

        # Read text from the image
        results = reader.readtext(image_path)

        # Open the file in write mode and save the extracted text
        with open(output_file, 'w', encoding='utf-8') as file:
            for detection in results:
                # # text, confidence = detection[1], detection[2]
                # # file.write(f"Text: {text}, Confidence: {confidence}\n")
                text = detection[1]
                file.write(f"{text}\n")

        # Read the content of the file
        with open(output_file, 'r') as file:
            file_content = file.read()

        # Remove "[" and "]" characters from the content
        modified_content = file_content.replace('[', '').replace(']', '')

        # Open the file for writing (this clears its content)
        with open(output_file, 'w') as file:
            # Write the modified content back to the file
            file.write(modified_content)

        # Use text_parse function from parse.py to parse the text from the output.txt
        parse.text_parse(output_file)

        os.remove(png_output)
        os.remove(output_file)

    except KeyboardInterrupt:
        print("Conversion was interrupted.")
    except FileNotFoundError:
        print("File not found.")
    except cv2.error as e:
        print(f"OpenCV Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

