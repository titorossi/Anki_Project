from collections import defaultdict, OrderedDict

freqs = defaultdict(int)
order = {}  # store first occurrence line number

with open("lemma-WITHOUTnumberssymbols-frequencies-paisa.txt", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        lemma, freq = line.strip().split(",")
        # skip words starting with uppercase
        if lemma and lemma[0].isupper():
            continue
        lemma = lemma.lower()
        freqs[lemma] += int(freq)
        if lemma not in order:
            order[lemma] = idx  # remember first occurrence position

# sort by first occurrence
sorted_items = sorted(freqs.items(), key=lambda x: order[x[0]])

# write results
with open("new lemma freq.txt", "w", encoding="utf-8") as out:
    for lemma, freq in sorted_items:
        out.write(f"{lemma},{freq}\n")
