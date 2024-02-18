def remove_duplicates(original_file_path, output_file_path):
    seen = set()  # A set to store already seen words
    unique_words = []  # A list to keep words in the original order

    # Read the original file
    with open(original_file_path, 'r', encoding='latin-1') as file:
        for line in file:
            word = line.strip()  # Remove any leading/trailing whitespace
            if word not in seen:
                seen.add(word)
                unique_words.append(word)

    # Write the unique words to a new file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for word in unique_words:
            file.write(word + '\n')

# Specify the path to your original file and the output file
original_file_path = r'C:\Users\titot\Desktop\PMW\Anki_Project\Texts\final_word_set.txt'
output_file_path = r'C:\Users\titot\Desktop\PMW\Anki_Project\Texts\final_words_no_duplicates.txt'

remove_duplicates(original_file_path, output_file_path)
