import json

with open('Cert_Collisions2024_378981_386951_Golden.json') as f:
    data = json.load(f)

eras = {
    'CtoI': (379412,387121),
    'C': (379412, 380252),
    'D': (380253, 380947),
    'E': (380948, 381943),
    'F': (381944, 383779),
    'G': (383780, 385813),
    'H': (385814, 386408),
    'I': (386409, 387121)
}

for era, (lo, hi) in eras.items():
    subset = {k: v for k, v in data.items() if lo <= int(k) <= hi}
    out = f'Cert_Collisions2024_Era{era}_Golden.json'
    with open(out, 'w') as f:
        json.dump(subset, f, indent=4)
    print(f"Era {era} ({lo}–{hi}): {len(subset)} runs → {out}")
