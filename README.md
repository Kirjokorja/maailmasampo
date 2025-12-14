# Maailmasampo

Maailmasampo on tietokantasovellus, joka on tarkoitettu maailmanrakennus- ja roolipelityökaluksi.

1. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
2. Käyttäjä pystyy kirjautumaan ulos sovelluksesta.
3. Käyttäjä pystyy luomaan uuden hankkeen eli pääasiallisen tietokohteen.
4. Tietokannassa on maailma-luokka hankkeelle.
5. Käyttäjä pystyy poistamaan luomansa hankkeen ja kaikki sen toissijaiset tietokohteet.
6. Käyttäjä pystyy muokkaamaan luomaansa hanketta ja kaikkia sen toissijaisia tietokohteita.
7. Käyttäjä pystyy antamaan oikeuksia muille käyttäjille luomaansa hankkeeseen.
8. Käyttäjä pystyy poistamaan oikeuksia muilta käyttäjiltä luomaansa hankeeseen.
9. Tietokannassa on seuraavat luokat toissijaisille tietokohteille:
   - alue
   - ympäristö
   - luonnonlaki
   - paikka
   - kulttuuri
   - yhteisö
   - laji
   - olento
   - henkilö
   - esine
   - menetelmä
10. Käyttäjä pystyy lisäämään toissijaisia tietokohteita hankkeeseen, johon hänellä on lisäysoikeudet.
11. Käyttäjä pystyy muokkaamaan lisäämiään toissijaisia tietokohteita hankkeessa, johon hänellä on muokkaamisoikeudet.
12. Käyttäjä pystyy poistamaan lisäämiään toissijaisia tietokohteita hankkeesta, johon hänellä on poistamisoikeudet.
13. Käyttäjä pystyy liittämään toissijaisia tietokohteita omiinsa sekä muiden käyttäjien toissijaisiin tietokohteisiin hankkeessa, johon hänellä on muokkaamisoikeudet.
14. Käyttäjä näkee sovellukseen luodut hankkeet ja niihin lisätyt toissijaiset tietokohteet. Käyttäjä näkee sekä itse lisäämänsä, että muiden käyttäjien lisäämät hankkeet ja toisssijaiset tietokohteet.
15. Käyttäjä pystyy etsimään tietokohteita hakusanalla tai tietokohteen luokalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.
16. Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tämän tunnuksen, tunnuksen luontiajankohdan, käyttöoikeudet.
17. Käyttäjän sisään- ja uloskirjautumisajankohtia, käyttäjän luomaia hankkeita ja lisäämiä tietokohteita sekä näiden lisäys-, poisto- ja muokkaamisajankohtia voi hakea päivämäärällä, käyttäjällä, toiminnolla tai kohteella.

## Sovelluksen asennus

Varmista, että sinulla on `Python 3.14` tai suurempi versio asennettuna koneellasi.
Hae repo koneellesi.

### 1. Poetrylla

Varmista, että sinulla on `Poetry 2.0.0` tai suurempi versio asennettuna koneellasi.
Asenna se repon juurihakemistossa komennolla*:

```
poetry install
```
Komento asentaa samalla kaikki tarvittavat riippuvuudet.

Mene juurihakemiston alta löytyvään `src`-hakemistoon. Vie sinne `sqlite`-tietokannan ohjelmatiedostot.
Alusta tietokanta `src`-hakemistoon komennoilla**:

```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

Nyt voit käynnistää sovelluksen komennolla:

```
flask run
```

### 2. Pipillä

Asenna `flask`-kirjasto repon juurihakemistossa komennolla*:

```
pip install flask
```

Mene juurihakemiston alta löytyvään `src`-hakemistoon. Vie sinne `sqlite`-tietokannan ohjelmatiedostot.
Alusta tietokanta `src`-hakemistoon komennoilla**:

```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

Nyt voit käynnistää sovelluksen komennolla:

```
flask run
```

*Jos käytät `Windows`-käyttöjärjestelmää, suosittelen käyttämään pääasiallisesti `PowerShell 7`:n komentokuorta.
`PowerShell 7` pitää asentaa kokemukseni mukaan `Windows`-järjestelmälle erikseen.

**Jos käytät `Windows`-käyttöjärjestelmää, joudut todennäköisesti käyttämään `Windows`-komentokuorta `PowerShell 7`:n komentokuoren sijaan.
En ole itse löytänyt komentomuotoa, jolla `sqlite3`:n komennot toimisivat `PowerShell 7`:llä.

## Sovelluksen testaus

Ajamalla tiedoston `seed.py` voit luodaa suurehkon määrän kohteita tietokantaan testausta varten.

## Loppupalautuksen toiminta

1. Sivutus on lisätty kaikkiin kyselyihin.

## Toisen sovituksen toiminta

1. Käyttäjän sivulla on listattu käyttäjän lisäämät tietokohteet.
2. Hankkeiden ja kohteiden haku on yhdistetty.

- Käyttäjän sivulta puuttuvat vielä käyttäjän omistamat hankkeet.

## Ensimmäisen sovituksen toiminta

1. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
2. Käyttäjä pystyy kirjautumaan ulos sovelluksesta.
3. Käyttäjä pystyy luomaan uuden hankkeen eli pääasiallisen tietokohteen.
4. Käyttäjä pystyy valitsemaan maailma-luokan hankkeelle.
5. Käyttäjä pystyy muokkaamaan ja poistamaan hankkeita.
7. Käyttäjä pystyy luomaan, muokkaamaan ja poistamaan toissijaisia tietokohteita.
8. Käyttäjä pystyy hakemaan hankkeita ja toissijaisia tietokohteita hakusanalla.
9. Käyttäjä pystyy hakemaan käyttäjiä hakusanalla.
