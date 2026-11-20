# Kino.db – Kino datubāzes pārvaldības sistēma

1. Projekta apraksts

Kino.db ir Python valodā izstrādāta kino datubāzes pārvaldības sistēma, kas izmanto SQLite datubāzi. Projekts paredzēts filmu, lietotāju, vērtējumu, atsauksmju un citas ar kino saistītas informācijas uzglabāšanai un pārvaldībai.

Lietotne nodrošina datu pievienošanu, apskati, meklēšanu, rediģēšanu un dzēšanu, izmantojot grafisko lietotāja saskarni.

2. Izmantotās tehnoloģijas
Python 3.x – lietotnes izstrāde.
SQLite3 – datu glabāšana un pārvaldība.
Tkinter – grafiskā lietotāja saskarne (ja izmantots projektā).
SQL – datubāzes vaicājumi.
Visual Studio Code – izstrādes vide.

3. Projekta struktūra
text
Kino.db/
│
├── app.py                # Grafiskā lietotāja saskarne
├── funkcijas.py          # Lietotnes funkcijas
├── Kino_skola.db         # SQLite datubāze
├── main.py               # Datubāzes izveide un inicializācija
├── terminal.py           # Termināļa funkcionalitāte
└── README.md             # Projekta dokumentācija

4. Datubāzes struktūra

Projektā tiek izmantota SQLite relāciju datubāze, kurā izveidotas 10 tabulas:

Tabula	Apraksts
movie	Informācija par filmām
users	Informācija par lietotājiem
rating	Filmu vērtējumi
reviews	Filmu atsauksmes
genre	Filmu žanri
director	Filmu režisori
actor	Filmu aktieri
movie_actor	Filmu un aktieru savstarpējās attiecības
comments	Komentāri par atsauksmēm
watchlist	Lietotāju skatāmo filmu saraksti
Tabulu savstarpējās attiecības
Filma var būt saistīta ar vienu žanru un režisoru.
Filmai var būt vairāki aktieri.
Viens aktieris var piedalīties vairākās filmās.
Lietotājs var pievienot filmu vērtējumus un atsauksmes.
Lietotāji var komentēt atsauksmes.
Katram lietotājam ir savs skatāmo filmu saraksts.

Datubāzē tiek izmantotas primārās un ārējās atslēgas, kā arī UNIQUE, NOT NULL un CHECK ierobežojumi datu integritātes nodrošināšanai.

5. Lietotnes funkcionalitāte

Grafiskajā saskarnē pieejamas šādas sadaļas:

Filmas
Lietotāji
Atsauksmes
Žanri
Režisori
Aktieri
Filmu aktieri
Komentāri
Skatāmo filmu saraksts

Galvenās iespējas:

Datu pievienošana un apskate.
Ierakstu meklēšana.
Informācijas rediģēšana un dzēšana.
Filmu vērtējumu un atsauksmju pārvaldība.
Datu saglabāšana SQLite datubāzē.
6. Projekta uzstādīšana un palaišana
Prasības
Instalēts Python 3.x.
Visual Studio Code vai cita Python izstrādes vide.
Git (projekta lejupielādei).

SQLite3 ir iekļauts Python standarta bibliotēkā, tāpēc papildu instalācija nav nepieciešama.

Lejupielāde

Atver termināli un izpildi:

bash
git clone https://github.com/ErnestsJ03/Kino.db.git
cd Kino.db

Palaišana

Vispirms inicializē datubāzi:

bash
python main.py


Pēc tam palaid grafisko lietotni:

bash
python app.py


Ja tiek izmantota cita Python palaišanas komanda, piemēram, Windows vidē:

bash
py main.py
py app.py

7. Datubāzes pieslēgšana

Savienojums ar SQLite datubāzi tiek izveidots, izmantojot Python sqlite3 moduli.

Piemērs no main.py:

python
import sqlite3

database = sqlite3.connect("Kino_skola.db")
cursor = database.cursor()

database.execute("PRAGMA foreign_keys = ON")


Datubāzes izmaiņas tiek saglabātas ar database.commit(), bet savienojums pēc darbību pabeigšanas tiek aizvērts ar database.close().


8. Datu drošība un iespējamās problēmas
Regulāri veidot datubāzes faila rezerves kopijas.
Izmantot parametrizētus SQL vaicājumus.
Pārbaudīt ievadīto datu pareizību.
Pārliecināties, ka datubāzes faila nosaukums kodā atbilst faktiskajam failam.
Pēc datu izmaiņām izpildīt database.commit().
Pārbaudīt ārējo atslēgu ierobežojumus, ja rodas datu savienošanas kļūdas.
9. Projekta autors

Ernests J.

GitHub: https://github.com/ErnestsJ03/Kino.db

Projekta versija: GOLD
