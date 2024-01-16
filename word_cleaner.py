import re

input_file = input('Please define an input file: ')
output_file = input('Please define an output file: ')

# Open the input file and process lines as required, then write to the output file
with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w') as fout:
    for line in fin:
        
        # Skip lines starting with a digit
        if not line[0].isdigit():
            continue

        # Remove all digits from the line
        line = ''.join(char for char in line if not char.isdigit())

        # Skip lines that are empty or contain only semicolons after removing digits
        if not (line.strip() and not all(char in ';\n\r' for char in line)):
            continue

        # Extract the first word, remove unwanted symbols while keeping accented characters, and write it to the output file
        words = line.split()
        if words:
            first_word = re.sub(r'[^\w\s]', '', words[0], flags=re.UNICODE)
            fout.write(first_word + '\n')