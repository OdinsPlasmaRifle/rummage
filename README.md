# Django MtG Card Crawler

MtG card searcher for South African online stores. The following stores are supported:

- Luckshack
- Dracoti
- Top Deck
- Sad Robot
- HQ Gaming
- The Warren
- A.I. Fest
- Battle Wizards
- Underworld Connections

# Setup

```
pip install -r requirements.txt
```

```
docker-compose up -d postgres
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py runserver 8080
```

