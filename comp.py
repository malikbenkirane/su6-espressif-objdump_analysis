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
