# Prosjektbeskrivelse og  dokumentasjon

##  Prosjekttittel
**Wikipedia**

---

## 1. Prosjektidé og problemstilling

### Beskrivelse
Jeg skal lage en app som lar personen lage sider hvor de kan skrive artikler selv, logge inn med enten en admin konto eller normal user. 
- Hva er prosjektet ditt?

## Hva skal jeg gjøre på Eksamensdagen

- Beskriv det du har planlagt å gjøre med ord 
- Lag et godt og detaljert Kanban-board (github-projects) som du viser for sensor. Legg inn link her

---
## 2. Systembeskrivelse

**Formål med applikasjonen:**\
*Forklar hva du ønsket å oppnå med prosjektet.*

**Brukerflyt:**\
*Beskriv hvordan brukeren bruker løsningen -- fra startside til lagring
av data.*

**Teknologier brukt:**

-   Python / Flask\
-   MariaDB\
-   HTML / CSS / JS\
-   (valgfritt) Docker / Nginx / Gunicorn / Waitress osv.

------------------------------------------------------------------------

## 3. Server-, infrastruktur- og nettverksoppsett

### Servermiljø

*F.eks.: Ubuntu VM, Docker, fysisk server.*

### Nettverksoppsett

-   Nettverksdiagram
-   IP-adresser\
-   Porter\
-   Brannmurregler

Eksempel:

    Klient → Waitress → MariaDB

### Tjenestekonfigurasjon

-   systemctl / Supervisor\
-   Filrettigheter\
-   Miljøvariabler

------------------------------------------------------------------------

## 4. Prosjektstyring -- GitHub Projects (Kanban)

-   To Do / In Progress / Done\
-   Issues\
-   Skjermbilde (valgfritt)

Refleksjon: Hvordan hjalp Kanban arbeidet?

------------------------------------------------------------------------

## 5. Databasebeskrivelse

**Databaser:**
users - brukere til nettsiden
pages - artikkler i nettsiden
**Tabeller:**
```
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
```
```
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
```
**SQL-eksempel:**

``` sql
CREATE TABLE users (
    ID              INT(11)         NOT NULL AUTO_INCREMENT,
    Username        VARCHAR(75)     NOT NULL,
    Password_hashed VARCHAR(225)    NOT NULL,
    Email           VARCHAR(100)    DEFAULT NULL,
    Active          TINYINT(1)      DEFAULT 1,
    Role            VARCHAR(10)     NOT NULL DEFAULT 'user',
    PRIMARY KEY (ID),
    UNIQUE KEY (Username)
);
```
``` sql
CREATE TABLE pages (
    ID          INT(11)      NOT NULL AUTO_INCREMENT,
    Title       VARCHAR(255) NOT NULL,
    Slug        VARCHAR(255) NOT NULL,
    Content     TEXT         NOT NULL,
    CreatorID   INT(11)      DEFAULT NULL,
    CreatedAt   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ID),
    UNIQUE KEY (Title),
    UNIQUE KEY (Slug),
    KEY (CreatorID),
    FOREIGN KEY (CreatorID) REFERENCES users(ID) ON DELETE SET NULL
);
```



------------------------------------------------------------------------

## 6. Programstruktur

    Wikipedia/
    ├── app.py
    ├── templates/
    ├── static/
    └── venv
    └──.gitignore
    └──req.txt

Databasestrøm:

    HTML → Flask → MariaDB → Flask → HTML-tabell

------------------------------------------------------------------------

## 7. Kodeforklaring



------------------------------------------------------------------------

## 8. Sikkerhet og pålitelighet

-   .env\
-   Miljøvariabler\
-   Parameteriserte spørringer\
-   Validering\
-   Feilhåndtering

------------------------------------------------------------------------

## 9. Feilsøking og testing

-   Typiske feil\
-   Hvordan du løste dem\
-   Testmetoder

------------------------------------------------------------------------

## 10. Konklusjon og refleksjon

-   Hva lærte du?\
-   Hva fungerte bra?\
-   Hva ville du gjort annerledes?\
-   Hva var utfordrende?

------------------------------------------------------------------------

## 11. Kildeliste

-   w3schools\
-   flask.palletsprojects.com
