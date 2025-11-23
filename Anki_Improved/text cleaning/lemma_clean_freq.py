from collections import defaultdict, OrderedDict

freqs = defaultdict(int)
order = {}  # store first occurrence line number

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

for idx, line in enumerate(lines):
    if ',' not in line:
        continue
    parts = line.strip().split(",", 1)
    if len(parts) != 2:
        continue
    lemma, freq = parts
    # skip words starting with uppercase
    if lemma and lemma[0].isupper():
        continue
    lemma = lemma.lower()
    freqs[lemma] += int(freq)
    if lemma not in order:
        order[lemma] = idx  # remember first occurrence position

# sort by first occurrence
sorted_items = sorted(freqs.items(), key=lambda x: order[x[0]])

# write results with proper UTF-8
with open("new lemma freq.txt", "w", encoding="utf-8") as out:
    for lemma, freq in sorted_items:
        out.write(f"{lemma},{freq}\n")

print(f"✅ Processed {len(freqs)} unique words")
print(f"📝 Output saved to: new lemma freq.txt")
