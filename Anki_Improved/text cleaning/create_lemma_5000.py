"""
Create lemma files from the cleaned new lemma.txt file
"""

with open('new lemma.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total words in new lemma.txt: {len(lines)}')

# Show some examples with accents to verify encoding
print('\nSample words with accents (first 100 lines):')
count = 0
for i, line in enumerate(lines[:100]):
    word = line.strip()
    if any(c in word for c in ['à', 'è', 'é', 'ì', 'ò', 'ù']):
        print(f'  Line {i+1}: {word}')
        count += 1
        if count >= 5:
            break

# Create lemma 5000.txt with first 5000 words
with open('../lemma 5000.txt', 'w', encoding='utf-8') as out:
    for line in lines[:5000]:
        out.write(line)

print(f'\n✅ Created ../lemma 5000.txt with first 5000 words')

# Create lemma 5001-10k.txt with words 5001-10000
if len(lines) >= 10000:
    with open('../lemma 5001-10k.txt', 'w', encoding='utf-8') as out:
        for line in lines[5000:10000]:
            out.write(line)
    print(f'✅ Created ../lemma 5001-10k.txt with words 5001-10000')
else:
    remaining = len(lines) - 5000
    with open('../lemma 5001-10k.txt', 'w', encoding='utf-8') as out:
        for line in lines[5000:]:
            out.write(line)
    print(f'✅ Created ../lemma 5001-10k.txt with {remaining} remaining words')

print(f'📝 Files are properly UTF-8 encoded with correct accented characters')
