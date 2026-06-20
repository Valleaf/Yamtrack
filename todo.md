# 🔴 Critical Bugs

### Imports & Sync

- [ ] FilmAffinity import does nothing.
- [ ] SensCritique review page not accessible / throws error.
- [ ] Collection sync identity bugs.
- [ ] Sync button shows error.
- [ ] Removed collection items are re-added after future syncs.

### Artwork & Metadata

- [ ] Some games display wrong title in lists but correct title on detail page. Exemple : Need for speed most wanted shows Need for speed on grid
- [ ] Searching on bnf works but no image
- [ ] Vagrant soldier ares when saved shows as 1076/flagrant-delire-les-gendarmes-tome-1 on the grid. Other similar problems sometimes

# 🟠 UI / UX Improvements

### Time

- [ ] Year and decade statistics by release year: It is empty

- Genres

- [ ] Genre for comics
- [ ] Tabs are there but no data
- [ ] most watched directors / artists used to work but breaks after a redis flush maybe ? Needs a persistent data .And same when i go on a director page, it doesn't know i've watched the movies unless i've clicked on it

Worl map should show the items when hovering on the circle (right now it shows country name + number o fitems)

Awards progress should be openable when clicked (in the sam page, like a dropdown?)

---

# 🟢 Features

### Filtering

- [ ] Global filtering system.
- [ ] Filter movies by genre.
- [ ] Filter music by genre.
- [ ] Filter books by genre.
- [ ] Filter games by genre.

### Collections

Dropped should count as completed for the collections and directors

- Planning

- [ ] Planning button available on the grids when searching.

### Backups

- [ ] Weekly automatic database backups : Mail ?

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

- [ ] see the films with something opening (same page)

more festivals, cesar, sundance, etc

### Custom Awards

- [ ] Personal GOTY collections (where i make my selection ).
- [ ] Personal best of each year /decade by media type. Easily selectable between own media already rated
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
- [ ] ios app for local use ?
- [ ] check features from https://github.com/dannyvfilms/Yamtrack

App : 



You have full filesystem access to my Yamtrack fork.

I want you to implement full Progressive Web App (PWA) support for Yamtrack so it can be installed on iPhone and Android from the browser and launched from the home screen like a native app.

### Requirements

1. Create a valid `manifest.json`

* Name: Yamtrack
* Short name: Yamtrack
* Display: standalone
* Start URL: /
* Theme/background colors matching the current Yamtrack UI
* Include 192x192 and 512x512 icons

1. Add all required meta tags to the global base template

* manifest link
* theme-color
* Apple mobile web app tags
* Apple touch icon
* viewport-fit=cover support

1. Add a Service Worker

* Register globally
* Cache static assets
* Cache CSS/JS/images
* Offline fallback for basic navigation
* Keep implementation simple and maintainable

1. Add iPhone-specific support

* Home screen installation support
* Proper status bar behavior
* Safe-area support for notches and home indicator

1. Create any required icon assets

* Reuse existing Yamtrack branding/logo if available
* Otherwise generate simple placeholder icons automatically

1. Verify all Django static paths work correctly in production Docker deployments.

### Important

* Read the existing project structure before making changes.
* Follow existing project conventions.
* Do not ask me for manual edits.
* Edit files directly.
* Show me every file changed.
* Explain any rebuild steps required afterwards.

### Validation

After implementation, tell me:

1. Which files were modified.
2. The URL I should open on my iPhone.
3. Exact steps to install Yamtrack on iPhone.
4. Any limitations of the current PWA implementation.

Also check whether Yamtrack already contains any PWA-related files and extend them instead of creating duplicates.
