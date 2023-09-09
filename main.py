import easyocr
import cv2
import parse

# Initialize the EasyOCR Reader with the Romanian language
reader = easyocr.Reader(['ro'])

# Replace 'your_image.jpg' with the path to your image file
image_path = cv2.imread("scancolor.png", 0) 

# Read text from the image
results = reader.readtext(image_path)

# Create a TXT file to store the extracted text
output_file = 'output_test.txt'

# Open the file in write mode and save the extracted text
with open(output_file, 'w', encoding='utf-8') as file:
    for detection in results:
        # text, confidence = detection[1], detection[2]
        # file.write(f"Text: {text}, Confidence: {confidence}\n")
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

parse.text_parse(output_file)

print(f"Extracted text saved to {output_file}")

