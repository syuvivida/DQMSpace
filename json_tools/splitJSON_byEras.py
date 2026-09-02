import json

with open('Cert_Collisions2022_355100_362760_Golden.json') as f:
    data = json.load(f)

eras = {
    'CtoG': (355794, 362760),
    'C': (355794, 357486),
    'D': (357487, 359021),
    'E': (359022, 360331),
    'F': (360332, 362180),
    'G': (362350, 362760),
}

for era, (lo, hi) in eras.items():
    subset = {k: v for k, v in data.items() if lo <= int(k) <= hi}
    out = f'Cert_Collisions2022_Era{era}_Golden.json'
    with open(out, 'w') as f:
        json.dump(subset, f, indent=4)
    print(f"Era {era} ({lo}–{hi}): {len(subset)} runs → {out}")
