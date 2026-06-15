# 🔴 Critical Bugs

### Imports & Sync

- [ ] FilmAffinity import does nothing.
- [ ] SensCritique review page not accessible / throws error.
- [ ] Collection sync identity bugs.
- [ ] Sync button shows error.
- [ ] Removed collection items are re-added after future syncs.

### Artwork & Metadata

- [ ] Some games display wrong title in lists but correct title on detail page. Exemple : Need for speed most wanted shows Need for speed on grid
- [ ] Searching on bnf works but clicking on an item shows error :
  - [ ] 127.0.0.1 - - [10/Jun/2026:17:17:39 +0200] "GET /health/ HTTP/1.0" 200 5329 "-" "Wget"
    127.0.0.1 - - [10/Jun/2026:17:17:44 +0200] "GET /medialist/comic HTTP/1.0" 200 71569 "http://localhost:8080/statistics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    172.18.0.1 - - [10/Jun/2026:17:17:44 +0200] "GET /medialist/comic HTTP/1.1" 200 10142 "http://localhost:8080/statistics" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    127.0.0.1 - - [10/Jun/2026:17:17:50 +0200] "GET /search?q=lucky+luke&media_type=comic HTTP/1.0" 200 155882 "http://localhost:8080/medialist/comic" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    172.18.0.1 - - [10/Jun/2026:17:17:50 +0200] "GET /search?q=lucky+luke&media_type=comic HTTP/1.1" 200 13077 "http://localhost:8080/medialist/comic" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    127.0.0.1 - - [10/Jun/2026:17:17:54 +0200] "GET /search?q=lucky%20luke&media_type=comic&source=bnf&layout=grid HTTP/1.0" 200 173408 "http://localhost:8080/search?q=lucky+luke&media_type=comic" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    172.18.0.1 - - [10/Jun/2026:17:17:54 +0200] "GET /search?q=lucky%20luke&media_type=comic&source=bnf&layout=grid HTTP/1.1" 200 15464 "http://localhost:8080/search?q=lucky+luke&media_type=comic" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    [2026-06-10 17:18:00 +0200] [41] [WARNING] Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))': /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb41191625w%22
    [2026-06-10 17:18:00 +0200] [41] [WARNING] Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))': /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb41191625w%22
    [2026-06-10 17:18:00 +0200] [41] [WARNING] Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))': /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb41191625w%22
    [2026-06-10 17:18:00 +0200] [41] [ERROR] Bibliothèque nationale de France request error: HTTPSConnectionPool(host='catalogue.bnf.fr', port=443): Max retries exceeded with url: /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb41191625w%22 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)')))
    [2026-06-10 17:18:00 +0200] [41] [WARNING] BnF metadata error for 'cb41191625w': There was an error contacting the Bibliothèque nationale de France API: HTTPSConnectionPool(host='catalogue.bnf.fr', port=443): Max retries exceeded with url: /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb41191625w%22 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))). Check the logs for more details.
    [2026-06-10 17:18:00 +0200] [41] [ERROR] bnf: Comic with ID cb41191625w not found
    [2026-06-10 17:18:00 +0200] [41] [ERROR] Bibliothèque nationale de France error: Comic with ID cb41191625w not found
    [2026-06-10 17:18:00 +0200] [41] [ERROR] Internal Server Error: /details/bnf/comic/cb41191625w/lucky-luke
    172.18.0.1 - - [10/Jun/2026:17:18:00 +0200] "GET /details/bnf/comic/cb41191625w/lucky-luke HTTP/1.1" 500 4737 "http://localhost:8080/search?q=lucky%20luke&media_type=comic&source=bnf&layout=grid" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    127.0.0.1 - - [10/Jun/2026:17:18:00 +0200] "GET /details/bnf/comic/cb41191625w/lucky-luke HTTP/1.0" 500 4737 "http://localhost:8080/search?q=lucky%20luke&media_type=comic&source=bnf&layout=grid" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    [2026-06-10 17:18:03 +0200] [41] [WARNING] Not Found: /favicon.ico
    127.0.0.1 - - [10/Jun/2026:17:18:03 +0200] "GET /favicon.ico HTTP/1.0" 404 3938 "http://localhost:8080/search?q=lucky%20luke&media_type=comic&source=bnf&layout=grid" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    172.18.0.1 - - [10/Jun/2026:17:18:03 +0200] "GET /favicon.ico HTTP/1.1" 404 1649 "http://localhost:8080/search?q=lucky%20luke&media_type=comic&source=bnf&layout=grid" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0"
    [2026-06-10 17:18:04 +0200] [41] [WARNING] Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))': /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb42732025d%22
    [2026-06-10 17:18:05 +0200] [41] [WARNING] Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))': /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb42732025d%22
    [2026-06-10 17:18:05 +0200] [41] [WARNING] Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))': /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb42732025d%22
    [2026-06-10 17:18:05 +0200] [41] [ERROR] Bibliothèque nationale de France request error: HTTPSConnectionPool(host='catalogue.bnf.fr', port=443): Max retries exceeded with url: /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb42732025d%22 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)')))
    [2026-06-10 17:18:05 +0200] [41] [WARNING] BnF metadata error for 'cb42732025d': There was an error contacting the Bibliothèque nationale de France API: HTTPSConnectionPool(host='catalogue.bnf.fr', port=443): Max retries exceeded with url: /api/SRU?version=1.2&operation=searchRetrieve&recordSchema=dublincore&maximumRecords=1&startRecord=1&query=bib.persistentId+adj+%22ark%3A%2F12148%2Fcb42732025d%22 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)'))). Check the logs for more details.
    [2026-06-10 17:18:05 +0200] [41] [ERROR] bnf: Comic with ID cb42732025d not found
    [2026-06-10 17:18:05 +0200] [41] [ERROR] Bibliothèque nationale de France error: Comic with ID cb42732025d not found
    [2026-06-10 17:18:05 +0200] [41] [ERROR] Internal Server Error: /details/bnf/comic/cb42732025d/lucky-luke-contre-joss-jamon-dessins-de-morris-scenario-de-r-goscinny

Home page : if more than 15 items in a planning, they dont show up. Also tv shows planning, that do not have any seasons watched should go in the planning sections (Only with those criterias)

# 🟠 UI / UX Improvements

### People Pages

- [ ] Director  page movies per row , set to 8 by default
- [X] Show full discography/bibliography where possible.

Statistics

World map should be an actual map with dots, like rateyourmusiuc. Also not sure all media types source the country.

---

# 🟡 Statistics Expansion

### Time

- [ ] Year statistics. From the media, not only consumption
- [ ] Decade statistics.(Bar chart like senscritique maybe ?)From the media not only consumption
- [ ] Media timeline (all time).

### Genres

- [ ] Genre statistics for movies.
- [ ] Genre statistics for TV.
- [ ] Genre statistics for books.
- [ ] Genre statistics for music.
- [ ] Genre statistics for games.

---

# 🟢 Features

### Filtering

- [ ] Global filtering system.
- [ ] Filter movies by genre.
- [ ] Filter music by genre.
- [ ] Filter books by genre.
- [ ] Filter games by genre.

### Collections

- [ ] Collections filter by media type.
- [ ] Multiple series/franchises per item.
- [ ] worls maps vcountries name and

### Planning

- [ ] Planning button available on the grids.

### Backups

- [ ] Weekly automatic backups.

---

# 🏆 Curated Lists & Awards in a new tab

### External Lists

- [ ] Letterboxd Top 250.
- [ ] Show list on click
- [ ] Sight & Sound Top 250.
- [ ] Edgar Wright's 100 Favorites.
- [ ] BFI Best Films.
- [ ] 1001 Albums You Must Hear Before You Die.
- [ ] Other popular curated lists.

### Awards

- [ ] fill in the list

more festivals, cesar, sundance, etc

### Custom Awards

- [ ] Personal GOTY collections (where i make my selection ).
- [ ] Personal best of each year /decade by media type
- [ ] Personal best of by genre
- [ ] Personal Oscars/Awards.
- [ ] User-defined award lists.
- [ ]

---

# 🔵 Nice To Have

- [ ] Show score more prominently across pages.
- [ ] calendar with images
- [ ] Better visual indicators for ratings.
- [ ] Richer metadata throughout the application.
- [ ] Images in new releases and indiciation if it's a season finale or somehting
- [ ] time watched sums tv shows
- [ ]
