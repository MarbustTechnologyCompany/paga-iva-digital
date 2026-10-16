#!/usr/bin/env python3
"""
Genera data/providers.json desde el XLS del catastro del SRI
(Catastro de Prestadores de Servicios Digitales No Residentes).

Uso:
    python scripts/generar-datos.py <catastro.xlsx> <salida.json>

Agrupa las variantes del mismo proveedor (NETFLIX / Netflix / netflix ...) en
una sola entrada, conserva todos los alias para la busqueda, y marca si el banco
retiene el IVA (por defecto), solo sobre la comision (INGRESOS POR COMISION), o
no retiene (DOMICILIADO O EP / REGISTRADO SRI = SI).

Requiere: Python 3 + openpyxl  (pip install openpyxl)
"""
import sys, json, re, datetime, os
import openpyxl


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', (s or '').upper())


def display_name(aliases):
    """Elige el nombre a mostrar: prefiere casing natural (Netflix > NETFLIX > netflix)."""
    def score(a):
        has_lower = any(c.islower() for c in a)
        if a[:1].isupper() and has_lower:
            return 3
        if has_lower:
            return 2
        return 1
    return sorted(aliases, key=lambda a: (-score(a), sum(c.isupper() for c in a), len(a), a))[0]


def load_nice_names(out):
    """Mapa opcional {normKey: 'Nombre bonito'} junto al JSON de salida (nombres-bonitos.json)."""
    p = os.path.join(os.path.dirname(os.path.abspath(out)), 'nombres-bonitos.json')
    if not os.path.exists(p):
        return {}
    raw = json.load(open(p, encoding='utf-8'))
    return {k: v for k, v in raw.items() if not k.startswith('_')}


def main(path, out):
    nice = load_nice_names(out)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    data = list(ws.iter_rows(values_only=True))[1:]  # fila 0 = encabezados

    groups = {}  # (normkey, desc) -> dict
    for r in data:
        name = str(r[0] if r[0] is not None else '').strip()
        if not name:
            continue
        desc = str(r[1] if r[1] is not None else '').strip()
        comision = str(r[3] if r[3] is not None else '').strip().upper().startswith('INGRESOS')
        domiciliado = str(r[4] if r[4] is not None else '').strip().upper() == 'SI'
        registrado = str(r[5] if r[5] is not None else '').strip().upper() == 'SI'
        key = (norm(name), desc)
        g = groups.setdefault(key, {'aliases': [], 'desc': desc, 'c': False, 'e': False, 's': False})
        if name not in g['aliases']:
            g['aliases'].append(name)
        g['c'] = g['c'] or comision
        g['e'] = g['e'] or domiciliado
        g['s'] = g['s'] or registrado

    descs = []
    desc_idx = {}

    def di(d):
        if d not in desc_idx:
            desc_idx[d] = len(descs)
            descs.append(d)
        return desc_idx[d]

    provs = []
    for (_nk, _desc), g in groups.items():
        provs.append({
            'n': nice.get(_nk) or display_name(g['aliases']),
            'a': g['aliases'],
            'd': di(g['desc']),
            'c': g['c'], 'e': g['e'], 's': g['s'],
        })
    provs.sort(key=lambda p: p['n'].lower())

    obj = {
        'meta': {
            'fuente': 'SRI — Catastro de Prestadores de Servicios Digitales No Residentes',
            'fuenteUrl': 'https://www.sri.gob.ec/catastros',
            'snapshot': datetime.date.today().isoformat(),
            'ivaRate': 15,
            'totalRegistros': sum(len(p['a']) for p in provs),
            'totalProveedores': len(provs),
        },
        'd': descs,
        'p': provs,
    }
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))

    print('proveedores agrupados:', len(provs))
    print('descripciones unicas:', len(descs))
    print('registros (aliases):', obj['meta']['totalRegistros'])
    print('tamano JSON:', round(os.path.getsize(out) / 1024, 1), 'KB')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
