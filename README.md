# Normantle

Semantle, på norsk!

Dette prosjektet er en norsk kopi av David Turners [Semantle](https://semantle.com/) og er laget med hjelp av [LTG Oslo](https://www.mn.uio.no/ifi/english/research/groups/ltg/) sine [word embeddings datasett](http://vectors.nlpl.eu/repository)

_Dette repoet er backenden for prosjektet. Frontenden kan du finner [her](https://github.com/LBlend/normantle-frontend)_

## Kjør selv

<details>
  <summary>Docker</summary>

1. Skriv denne kommandoen for å kjøre backenden.

```
docker run -d -p 5000:5000 -e PUZZLE_SECRET=<hemmelig nøkkel> --name normantle-backend ghcr.io/lblend/normantle:latest
```

Lag nøkkelen én gang, f.eks. med `openssl rand -hex 32`, og ta vare på den. Bytter du nøkkel får alle dager nye ord.

Vi anbefaler at du bruker kommandoen gitt ovenfor. Du står derimot fritt til å endre variabler til eget ønske om du vet hva du driver med.

</details>

<details>
  <summary>Manuelt</summary>

0. Last ned repoet og installer avhengigheter

- [uv](https://docs.astral.sh/uv/) (installerer Python 3.15 automatisk)
- wget og unzip

1. Kjør installasjonsskriptet

   ```
   sh setup.sh
   ```

2. Kjør APIet
   ```
   uv run --no-dev uvicorn src.main:app --host 0.0.0.0 --port 5000 --proxy-headers
   ```

</details>

_Det ligger også en [docker-compose](docker-compose.yml) fil i dette repoet som vil sette opp både backend og frontend gjennom Docker. Sett `PUZZLE_SECRET` som beskrevet over, og `API_ROOT` til adressen nettleseren skal bruke for å nå backenden. Standard er `http://localhost:5000`._

### Konfigurasjon

| Miljøvariabel           | Standardverdi     | Beskrivelse                                                                  |
| ----------------------- | ----------------- | ---------------------------------------------------------------------------- |
| `MODEL_PATH`            | `model/model.bin` | Sti til word2vec-modellen i binærformat                                      |
| `TZ`                    | `Europe/Oslo`     | Tidssonen som bestemmer når dagens ord byttes                                |
| `CORS_ORIGINS`          | `*`               | Kommaseparert liste over domener som får bruke APIet                         |
| `PUZZLE_SECRET`         |                   | Hemmelig nøkkel som bestemmer rekkefølgen på ordene. Ikke bytt den etter at spillet er i bruk |
| `RATE_LIMIT_PER_MINUTE` | `120`             | Maks antall forespørsler per IP-adresse per minutt. `0` skrur av begrensningen |
| `FORWARDED_ALLOW_IPS`   | Private nettverk  | Proxyer som får sette `X-Forwarded-For`. Gjelder Docker-imaget              |

Kjører du APIet bak en reverse proxy må den sende klientens IP-adresse videre, ellers deler alle spillere samme grense. For nginx:

```
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

### Utvikling

```
uv sync
uv run ruff check
uv run ruff format
```

For å lage den filtrerte modellen selv kan du kjøre `sh setup_filter.sh`.

## Et notat om valg av word2vec-modell og filtrering

### Valg av modell

Dette prosjektet tar i modell #93 fra LTG Oslo sitt [word embeddings repository](http://vectors.nlpl.eu/repository/). Grunnen til at denne modellen ble valgt over f.eks. en med større vokabulær har mye med de underliggende korpora. Etter litt anekdotisk eksperimentering kom det frem at modellene som tar i bruk NoWaC og NBDigital korpusene inneholdt mange ord som ikke er norske. Dette påvirket spillets gang til en såpass stor grad at disse ble valgt bort.

### Filtrering

Modellene inneholder mange ord som ikke passer seg til spillet. Dette er gjerne stopwords eller andre ord som forkortelser osv. For å "løse" dette har jeg valgt å filtrere bort alle ord som er stoppord ifølge NLTK-pakken samt ord som begynner med stor bokstav, inneholder andre tegn enn bokstaver eller er kortere enn tre bokstaver lange.

### Valg av dagens ord

Dagens ord trekkes fra ord nummer 150 til 3150 i modellen, som er sortert fra vanligst til minst vanlig. De 150 vanligste ordene hoppes over fordi de stort sett er fyllord som "mye", "måtte" og "ifølge". Ordene stokkes med `PUZZLE_SECRET` og deles ut ett om dagen, så det går over åtte år før et ord kommer igjen, og ingen kan regne ut fremtidige ord uten nøkkelen.

## Takk

Takk til [LtgOslo](https://www.mn.uio.no/ifi/english/research/groups/ltg/) som har publisert word2vec-modellen. Uten dem ville ikke dette prosjektet vært mulig.
