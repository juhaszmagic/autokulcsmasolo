# autokulcsmasolo.com

Az Autókulcs Másolás 0-24 weboldala. Statikus HTML, GitHub Pages szolgálja ki.

- A tartalom a `build.py` fájlban van; módosítás után: `python3 build.py`
- Stílus: `assets/style.css`, képek: `assets/img/`
- Az URL-ek megegyeznek a korábbi oldaléval (pl. `/arak/`, `/potkulcs/`), így a Google Ads hirdetések és a keresőtalálatok nem törnek el.

## Élesítés (domain átállítás)

1. `build.py`: `NOINDEX = False`, majd `python3 build.py`
2. `CNAME` fájl létrehozása ezzel a tartalommal: `autokulcsmasolo.com`
3. A domain DNS-ében a GitHub Pages címeire kell irányítani a domaint.
