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
