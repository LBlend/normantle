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

1. Kjør installasjonsskriptet

   ```
   sh setup.sh
   ```

_Merk deg at dette skriptet antar at PATH til python er satt til `python3`. Hvis dette ikke er tilfellet for deg, må du huske å endre skriptet eller PATHen din._

2. Kjør APIet
   ```
   uvicorn src.main:app --host 0.0.0.0 --port 5000 --proxy-headers
   ```

</details>

## Et notat om valg av word2vec-modell og filtrering

### Valg av modell

Dette prosjektet tar i modell #93 fra LTG Oslo sitt [word embeddings repository](http://vectors.nlpl.eu/repository/). Grunnen til at denne modellen ble valgt over f.eks. en med større vokabulær har mye med de underliggende korpora. Etter litt anekdotisk eksperimentering kom det frem at modellene som tar i bruk NoWaC og NBDigital korpusene inneholdt mange ord som ikke er norske. Dette påvirket spillets gang til en såpass stor grad at disse ble valgt bort.

### Filtrering

Modellene inneholder mange ord som ikke passer seg til spillet. Dette er gjerne stopwords eller andre ord som forkortelser osv. For å "løse" dette har jeg valgt å filtrere bort alle ord som er stoppord ifølge NLTK-pakken samt ord som inneholder store bokstaver eller er kortere enn tre bokstaver lange.

