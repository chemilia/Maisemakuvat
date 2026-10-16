# Maisemakuvat
## Sovelluksen toiminnot:
- Sovelluksessa käyttäjät pystyvät jakaa omia ottamia kuvia erilaisista maisemista ja kirjoittaa kuvauksia niista, esimerkiksi paikan nimi tai milloin kuvä on otettu.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään kuvia, muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt kuvat.
- Käyttäjä pystyy etsimään kuvia joko hakusanalla, luokittelulla tai molempia käyttäen.
- Käyttäjäsivu näyttää, montako kuvia käyttäjä on lähettänyt ja listan käyttäjän lisäämistä kuvista.
- käyttäjä pystyy valitsemaan esimerkiksi seutaavia luokitteluja:
  -  maiseman tyyppi: esim. vuoristo, meri, järvi...
  -  vuodenajat: kevät, kesä, syksy tai talvi
  -  vuosikymmenet: esim. 2010-luku, 2020-luku...
- Käyttäjä pystyy antaa kuville kommentin ja tykkäyksiä. Kuvien alla näkyy komentit ja kuinka monta tykkäystä on saanut kaikilta käyttäjiltä.

Tässä pääasiallinen tietokohde on kuvat ja toisssijainen tietokohde on kuvien komentti ja tykkäykset. 

## Sovelluksen asennus:
Asenna ```flask```-kirjaston:

```$ pip install flask```


Luo tietokannan taulut ja lisää alkutiedot:

```$ sqlite3 database.db < schema.sql```


Voit käynnistää sovelluksen näin:

```$ flask run```
