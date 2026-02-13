# Prosjektbeskrivelse – IT-utviklingsprosjekt (2IMI)

##  Prosjekttittel
**Wikipedia**

---

## Deltakere
- Navn 1 – Jonas


---

## 1. Prosjektidé og problemstilling

### Beskrivelse
Jeg skal lage en liten wikipedia som lar deg lage sider hvor du kan skrive informasjon om hva som helst. Det skal ha få regler og være en mer anarkistisk alternativ til Wikipedia

Det løser ikke et spesifkt problem som ikke er løst, men det lar folk skrive artikkler om hva de vil.

det lar mer folk spre ulike ting, derfor er det nyttig

- Hva er prosjektet?
- Hvilket problem løser det?
- Hvorfor er løsningen nyttig?

### Målgruppe
Hvem er løsningen laget for?
løsningen er laget for folk som har lyst til å skrive informasjon om alt fra deres rare hobbyer til å lage wikipedia artikkler om fantasy land

---

## 2. Funksjonelle krav

Systemet skal minst ha følgende funksjoner:

1. Funksjon 1  
    log in, muligheten til å logge in med en user til session
2. Funksjon 2  
    log out, fjerner sessions
3. Funksjon 3  
    admin dashboard, lar admins se brukere og fjerne users som bryter regler
4. Funksjon 4  
    mulgihet til å lage og redigere sider
5. Funksjon 5  
    mulighet til å søke for å finne sider

*(Legg til flere hvis nødvendig)*

---

## 3. Teknologivalg

### Programmeringsspråk
- HTML/CSS/Python

### Rammeverk / Plattform / Spillmotor
- Flask

### Database
- MariaDB

### Verktøy
- GitHub
- GitHub Projects (Kanban)
- Eventuelle andre verktøy

---

## 4. Datamodell

### Oversikt over tabeller

**Tabell 1:**
- Navn: Users
- Beskrivelse: alle brukere, deres email, passord(hashed), rolle og ligende

**Tabell 2:**
- Navn: Pages
- Beskrivelse: alle ulike sider, deres informasjon, deres innhold, navn, og skaperen. 

*(Minst 2–4 tabeller)*

### Eksempel på tabellstruktur
```sql
User(
 +-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| ID              | int(11)      | NO   | PRI | NULL    | auto_increment |
| Username        | varchar(75)  | NO   | UNI | NULL    |                |
| Password_hashed | varchar(225) | NO   |     | NULL    |                |
| Email           | varchar(100) | YES  |     | NULL    |                |
| Active          | tinyint(1)   | YES  |     | 1       |                |
| Role            | varchar(10)  | NO   |     | user    |                |
+-----------------+--------------+------+-----+---------+----------------+
)

pages (
    +-----------+--------------+------+-----+---------------------+-------------------------------+
| Field     | Type         | Null | Key | Default             | Extra                         |
+-----------+--------------+------+-----+---------------------+-------------------------------+
| ID        | int(11)      | NO   | PRI | NULL                | auto_increment                |
| Title     | varchar(255) | NO   | UNI | NULL                |                               |
| Slug      | varchar(255) | NO   | UNI | NULL                |                               |
| Content   | text         | NO   |     | NULL                |                               |
| CreatorID | int(11)      | YES  | MUL | NULL                |                               |
| CreatedAt | timestamp    | YES  |     | current_timestamp() |                               |
| UpdatedAt | timestamp    | YES  |     | current_timestamp() | on update current_timestamp() |
+-----------+--------------+------+-----+---------------------+-------------------------------+
)
