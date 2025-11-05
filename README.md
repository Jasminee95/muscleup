# MuscleUp Backend

Flask + MySQL + MongoDB prosjekt.

## Om prosjektet
Dette prosjektet er en treningsapp der brukere kan logge inn, søke etter øvelser, lagre favoritter i MySQL og bygge ukeplaner i MongoDB.

### MongoDB-integrasjon
Jeg har satt opp MongoDB lokalt og koblet prosjektet til databasen `muscleup_schedule`.
Jeg har laget en collection `plans` for treningsplaner som kan lagre økter og muskelgrupper.
Dette er foreløpig et utforskningssteg for å teste hvordan ukeplanen kan lagres dynamisk.

## Teknologier
- Flask (Python)
- MySQL
- MongoDB (lokal Compass)
- Flask-Login
- Flask-Bcrypt
- Flask-CORS