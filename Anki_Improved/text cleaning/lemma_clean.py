# Process the lemma file and keep frequency order
# Output saved as "new lemma.txt" in the same folder

seen = set()
unique_words = []

with open("lemma-WITHOUTnumberssymbols-frequencies-paisa.txt", "r", encoding="utf-8") as f:
    for line in f:
        lemma, _ = line.strip().split(",")
        # skip words starting with uppercase
        if lemma and lemma[0].isupper():
            continue
        lemma = lemma.lower()
        if lemma not in seen:
            seen.add(lemma)
            unique_words.append(lemma)

# write results in same order as input file
with open("new lemma.txt", "w", encoding="utf-8") as out:
    for word in unique_words:
        out.write(word + "\n")
