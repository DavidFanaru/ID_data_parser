import io
from PIL import Image
import base64

png_output = 'output.png'

# Convert bytearray to PNG
def bytearray_to_png(photobyte):
    try:
        if photobyte is None:
            raise ValueError("Input 'photobyte' is None or empty.")
        
        # Read the contents of idbyte.txt and assign it to byte_array
        # with open('idbyte.txt', 'rb') as file:
        # byte_array = photobyte

        file_bytea = photobyte
        image_data = base64.b64decode(file_bytea)
        image = Image.open(io.BytesIO(image_data))
        image.save(png_output, 'PNG')

        print("Image saved successfully:", png_output)

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except io.UnsupportedOperation as ue:
        print(f"UnsupportedOperation: {ue}")
    except Exception as e:
        print(f"An error occurred: {e}")





