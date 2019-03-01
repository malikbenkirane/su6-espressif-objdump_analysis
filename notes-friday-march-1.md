j'ai toujour les mains dans le cambui sur l'identification des librairies

pas de progès significaif depuis la dernière fois

le code qui suit manipule le fichier `rom.addr.v6.ld` pour determiner les fonctions déclarés dans le second script de link (`rom.addr.v6.ld`)

```
#!/usr/local/bin/python3 -i
import os
import re

ld_filenames = [
    filename for filename in os.listdir()
    if 'rom.addr.v6.ld' in filename
]

lines = {
    filename:
    open(filename).readlines()
    for filename in ld_filenames
}

r = re.compile(r'PROVIDE\s*\(\s*([A-Za-z_]+)\s*=\s*(0x[0-9a-f]+)\s*\)')

matches = {
    filename: [r.match(line) for line in lines[filename]]
    for filename in ld_filenames
}

unmatched_symbols_index = {
    filename:
    [
        i for i, m in enumerate(matches[filename])
        if m is None
    ]
    for filename in ld_filenames
}

symbols = {
    filename: [m.groups() for m in matches[filename] if m is not None]
    for filename in ld_filenames
}


# interactive mode shortcuts (python -i env)
s = {
    'esp' if 'espressif' in filename else 'rb': symbols[filename]
    for filename in ld_filenames
}


# list symbols provided per table
def list_provided(symbols):

    assocs = {table: {} for table in symbols}

    for table in symbols:
        for symbol_assoc in symbols[table]:
            sname, saddr = symbol_assoc
            if sname not in assocs:
                assocs[table][sname] = [saddr]
            else:
                assocs[table][sname].append(saddr)
                
    return assocs

# list tables per symbol provided 
def symbols_availability(symbols):

    symbols_tables = {}
    for table in symbols:
        for symbol in symbols[table]:
            if symbol not in symbols_tables:
                symbols_tables[symbol] = [table]
            else:
                symbols_tables[symbol].append(table)
    return symbols_tables

# interactive mode shortcut (python -i env)
a = symbols_availability(s)

s = [l.replace('\n','') for l in open('assets/objdumps_no_dots.txt').readlines()][1:]

```

quelqule commentaires sur la démarche et la méthode dans `readme.md`

---



Dans un environnement microcontrolleur, on souhaite avoir \`a l'issu
des differentes passes de compilation un objet executable qui ne requiert
pas d'appels a des librairies externes (appels dynamiques).
L'objet \`a l'issu de la compilation doit tout aussi bien contenir
les fonctions des librairies externes et ses propres fonctions.
Il serait trop co\^uteux de mettre en place un mecanisme de chargement
dynamique dans un tel environnement.

*GNU project* qui maintient la base du compilateur `gcc`, qui
port\'e sur plusieurs architectures ([`pic32-gcc`][2], [`xt-gcc`][3]),
propose aussi dans le package *binutils* [(1)][1]
un mecanisme d'edition des liens [(2)][4] qui \'etend le langage
d'edition de liens d'AT&T's (*AT&T’s Link Editor Command Language*).

1. comparaison rom.v6.ld rboot et espressif

```
>>> set([len(p['esp'][x]) for x in p['esp']])
{1}
>>> set([len(p['rb'][x]) for x in p['rb']])
{1}
```

nombre de symboles (rb: rboot, esp: esp8266)
```
{t: len(p[t].keys()) for t in p}
{'rb': 286, 'esp': 287}
```

differences entre rb et esp (presence du symbole)
```
>>> pprint({s: a[s] for s in a if len(a[s]) < 2} )
{('Enable_QMode', '0x400044c0'): ['esp'],
 ('rcons', '0x3fffd0f0'): ['esp'],
 ('uart_div_modify', '0x400039d8'): ['rb']}
```

2. lister symboles de nonos-sdk/lib

difference `objdump -t` (ss) et `symbol_tables` (s)
```
>>> len(set(s) & set(ss))
99
>>> len(a.keys())
288
```


[1]: https://www.gnu.org/software/binutils/
[4]: https://sourceware.org/binutils/docs/ld/Overview.html#Overview

---

le tout que j'ai pushé sur https://github.com/malikbenkirane/su6-espressif-objdump_analysis

---



merci pour vos retours