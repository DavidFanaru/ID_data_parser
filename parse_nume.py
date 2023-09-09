file_path = "output_test.txt"  # Replace with the path to your file
allowed_capital_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZȘȚÂĂÎ"  # Add the additional characters
found_13_digit_code = False

try:
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            
            if found_13_digit_code:
                # Check if the line contains only capital letters or additional characters
                if all(char in allowed_capital_letters for char in line):
                    print(f"Found line with only capital letters or additional characters: {line}")
                    break  # Stop searching once we find such a line
            else:
                # Check if the line contains a 13-digit code
                if line.isdigit() and len(line) == 13:
                    found_13_digit_code = True
                    print(f"Found a line with a 13-digit code: {line}")

except IOError as e:
    print(f"An error occurred while reading the file: {e}")
