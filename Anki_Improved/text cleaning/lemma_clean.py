# Process the lemma file and keep frequency order
# Output saved as "new lemma.txt" in the same folder
# Fixes any double-encoded UTF-8 issues automatically

seen = set()
unique_words = []

# Read with latin-1 to preserve bytes, then fix encoding
try:
    with open("lemma-WITHOUTnumberssymbols-frequencies-paisa.txt", "r", encoding="latin-1") as f:
        content = f.read()
    # Fix double-encoded UTF-8
    content = content.encode('latin-1').decode('utf-8', errors='replace')
    lines = content.splitlines()
except:
    # Fallback to normal UTF-8 if file is already correct
    with open("lemma-WITHOUTnumberssymbols-frequencies-paisa.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

for line in lines:
    if ',' not in line:
        continue
    lemma, _ = line.strip().split(",", 1)
    # skip words starting with uppercase
    if lemma and lemma[0].isupper():
        continue
    lemma = lemma.lower()
    if lemma not in seen:
        seen.add(lemma)
        unique_words.append(lemma)

# write results in same order as input file with proper UTF-8
with open("new lemma.txt", "w", encoding="utf-8") as out:
    for word in unique_words:
        out.write(word + "\n")

print(f"✅ Processed {len(unique_words)} unique words")
print(f"📝 Output saved to: new lemma.txt")
