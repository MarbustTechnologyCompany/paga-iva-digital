# ¿Paga IVA Digital?

Herramienta web **gratuita y de código abierto** para saber, al instante, si un proveedor
digital extranjero te genera **retención del 15% de IVA** cuando le pagas con tarjeta de
crédito o débito en Ecuador.

No hay que descargar nada ni entrar al SRI: escribes el nombre del proveedor (tal como aparece
en tu estado de cuenta o como lo conoces) y la página te dice si el banco te retiene el IVA.

## ¿Por qué existe?

Desde 2020 la ley ecuatoriana grava con IVA los **servicios digitales importados**. Cuando le
pagas con tarjeta a un proveedor **no residente** que figura en el catastro del SRI, tu banco
está obligado a **retener el 15% del IVA** además del precio. Esta herramienta te deja conocer
ese costo **antes** de pagar, para que no te sorprenda en el estado de cuenta.

> **No es asesoría tributaria ni una invitación a dejar de pagar impuestos.** Su único fin es
> informar el IVA que la ley manda retener. La fuente es el catastro **público** del SRI.

**En vivo:** https://marbusttechnologycompany.github.io/paga-iva-digital/

## Cómo está hecho

- **Sitio 100% estático** (HTML + CSS + JS vanilla, sin framework, sin backend, sin base de datos).
- Los datos viven en `data/providers.json`, generado desde el catastro oficial del SRI.
- Se despliega en **GitHub Pages** (hosting gratuito).
- Diseño basado en el sistema visual de Wise (verde Forest Ink + lima, tipografía Inter).

## Resultados

| Etiqueta | Significado |
|---|---|
| ➕ 15% IVA | Proveedor no residente en el catastro: el banco retiene el 15% sobre el total. |
| 15% solo comisión | Plataforma intermediaria (delivery, marketplace): se retiene solo sobre su comisión. |
| ✓ Sin IVA adicional | Domiciliado en Ecuador o registrado en el SRI: factura/declara el IVA él mismo, no se retiene. |

## Actualizar los datos

El catastro del SRI se actualiza cada trimestre (enero, abril, julio, octubre).
Una **GitHub Action** (`.github/workflows/actualizar-catastro.yml`) lo mantiene al día
automáticamente: cada trimestre descarga el XLS vigente del SRI, regenera
`data/providers.json` y, si cambió, lo commitea (lo que redepliega Pages). También se
puede disparar a mano desde la pestaña *Actions*.

Para regenerarlo localmente:

```bash
# descarga el XLS desde https://www.sri.gob.ec/catastros (Servicios Digitales, versión XLS)
python scripts/generar-datos.py data/catastro-sri.xlsx data/providers.json
```

Requiere Python 3 y `openpyxl` (`pip install openpyxl`).

## Licencia

[MIT](LICENSE) — Marco Antonio Bustillos Quiroz · Marbust Technology Company.

## Fuente

[Catastro de Prestadores de Servicios Digitales No Residentes — SRI](https://www.sri.gob.ec/catastros)

---

Proyecto abierto de [Marbust Technology Company](https://marbust.com).
