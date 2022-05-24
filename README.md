# Normantle

Semantle, på norsk!

Dette prosjektet er en norsk kopi av David Turners [Semantle](https://semantle.com/) og er laget med hjelp av [LTG Oslo](https://www.mn.uio.no/ifi/english/research/groups/ltg/) sine [word embeddings datasett](http://vectors.nlpl.eu/repository)

_Dette repoet er backenden for prosjektet. Frontenden kan du finner [her](https://github.com/LBlend/normantle-frontend)_

## Kjør selv

<details>
  <summary>Docker</summary>

Kommer en eller annen gang™

</details>

<details>
  <summary>Manuelt</summary>

0. Last ned repoet og installer avhengigheter

- Python 3.10+
- Pip

1. Kjør installasjon- og treningssskriptet

   ```
   sh setup.sh
   ```

_Merk deg at dette skriptet antar at PATH til python er satt til `python3`. Hvis dette ikke er tilfellet for deg, må du huske å endre skriptet eller PATHen din._

2. Kjør APIet
   ```
   uvicorn src.main:app --host 0.0.0.0 --port 5000 --proxy-headers
   ```

</details>
