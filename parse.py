import re
import json

def text_parse(output_file):

    # Initialize a list to store the whitelisted 2-letter words
    whitelist = []

    # Read the whitelist from the text file
    with open('seriebuletin.txt', 'r') as whitelist_file:
        for line in whitelist_file:
            word = line.strip()  # Remove leading/trailing whitespace
            whitelist.append(word)

    # Initialize variables to store the matched 2-letter word, 6-digit code, 13-digit code, sex, data_nastere, date range, and "Emis de"
    serie = None
    numar = None    
    cnp = None
    sex = None
    data_nastere = None
    data_valabilitate = None
    emis_de = None 
    nume = None
    prenume = None
    serienumar = None  # Initialize serienumar
    data_eliberarii = None
    data_expirarii  = None

    cnp_line = None  # Store the previous line
    nume_line = None
    prev_line = None
    nume_test = None
    prenume_test = None
    

    # Open and read the entire text file line by line
    with open(output_file, 'r') as file:
        for line in file:
            # Use regular expression to find 2-letter words
            matches = re.findall(r'\b[a-zA-Z]{2}\b', line)
            for match in matches:
                if match in whitelist:
                    serie = match
                    break  # Stop searching after the first match

            # Use regular expression to find a 6-digit code
            code_match = re.search(r'\b\d{6}\b', line)
            if code_match:
                numar = code_match.group()
            
            # Use regular expression to find a 13-digit code
            thirteen_digit_match = re.search(r'\b\d{13}\b', line)
            if thirteen_digit_match:
                cnp = thirteen_digit_match.group()

                # Determine the sex based on the first digit of the 13-digit code
                first_digit = int(cnp[0])
                if first_digit % 2 == 0:
                    sex = "F"  # Even first digit
                else:
                    sex = "M"  # Odd first digit

                # Extract and format the data_nastere from the 13-digit code
                data_nastere_digits = cnp[1:7]  # Extract digits 2 to 7
                year_prefix = ""

                if first_digit in [1, 2]:
                    year_prefix = "19"
                elif first_digit in [3, 4]:
                    year_prefix = "18"
                elif first_digit in [5, 6]:
                    year_prefix = "20"

                data_nastere = f"{data_nastere_digits[4:]}-{data_nastere_digits[2:4]}-{year_prefix}{data_nastere_digits[:2]}"


            # Use regular expression to find the date range in the format "12.10.20-10.11.2024"
            data_valabilitate_match = re.search(r'\b\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{4}\b', line)
            if data_valabilitate_match:
                data_valabilitate = data_valabilitate_match.group()

                # Split the date range into "Data eliberarii" and "Data expirarii"
                dates = data_valabilitate.split('-')
                if len(dates) == 2:
                    data_eliberarii = dates[0].replace('.', '-')
                    data_expirarii = dates[1].replace('.', '-')
                    
                    # Add "20" before the "20" in the year part
                    data_eliberarii_parts = data_eliberarii.split('-')
                    data_eliberarii_parts[2] = f"20{data_eliberarii_parts[2]}"
                    data_eliberarii = '-'.join(data_eliberarii_parts)

    with open(output_file, 'r') as file:
        for line in file:

            # Check if the current line contains the pattern "data_valabilitate"
            if data_valabilitate in line:
                emis_de = prev_line.strip()
                emis_de = emis_de.replace(".", "")

            
            # Check if the line, converted to lowercase, starts with "idrou"
            if line.lower().startswith("idrou"):
                # Store the next line as serienumar
                next_line = next(file)
                serienumar = next_line.strip()

            prev_line = line  # Store the current line as the previous line

    with open(output_file, 'r') as file:
        for line in file:
            if cnp in line:
                cnp_line = True
            if cnp_line:
                nume_test = line.strip()

                # Test if "nume_test" contains only capital letters (including "ȘȚÂĂÎ") and no digits
                if nume_test.isupper() and not re.search(r'\d', nume_test):
                    nume = nume_test
                    break  # Exit the loop as we found a valid "nume"


    with open(output_file, 'r') as file:
        for line in file:
            if nume_line:
                prenume_test = line.strip()
                print(prenume_test)

                # Test if "nume_test" contains only capital letters (including "ȘȚÂĂÎ") and no digits
                if prenume_test.isupper():
                    prenume = prenume_test
                    break  # Exit the loop as we found a valid "nume"

            if nume in line:
                nume_line = True
                        

    # Set "serie" to the first 2 characters of "serienumar" if "serie" is None
    if serie is None and serienumar:
        serie = serienumar[:2]
    if numar is None and serienumar:
        numar = serienumar[2:8]

    # Convert the matched words, codes, sex, data_nastere, date range, "Emis de," and "serienumar" to a dictionary
    result_dict = {
        "Serie": serie,
        "Numar": numar,
        "CNP": cnp,
        "Sex": sex,
        "Data nasterii": data_nastere,
        "Data eliberarii": data_eliberarii,
        "Data expirarii": data_expirarii,
        "Emis de": emis_de,
        "SerieNumar": serienumar,
        "Nume": nume,
        "Prenume": prenume
    }

    # Convert the dictionary to JSON
    output_json = json.dumps(result_dict, indent=4, ensure_ascii=False)

    # Save the JSON data to a file
    with open('output.json', 'w') as json_file:
        json_file.write(output_json)