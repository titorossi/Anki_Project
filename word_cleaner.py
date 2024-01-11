
input_file = input('Please define an input file: ')
output_file = input('Please define an output file: ')

# Open the input file and add all lines that do not start with a digit to the output file
with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
    for line in fin:
        if line[0].isdigit():
            fout.write(line)

# Reopen the output file and remove all numbers from it
with open(output_file, 'r') as fin:
    lines = fin.readlines()

with open(output_file, 'w') as fout:
    for line in lines:
        fout.write(''.join(char for char in line if not char.isdigit()))

#Reopen the output file and remove all empty lines from it
with open(output_file, 'r') as fin:
    lines = fin.readlines()

with open(output_file, 'w') as fout:
    for line in lines:
        if line.strip() and not all(char in ';\n\r' for char in line):
            fout.write(line)

# Reopen the output file and remove all words after the first word from it
with open(output_file, 'r') as fin:
    lines = fin.readlines()

with open(output_file, 'w') as fout:
    for line in lines:
        words = line.split()
        if words:
            fout.write(words[0] + '\n')

