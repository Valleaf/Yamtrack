# 🔴 Critical Bugs

### Imports & Sync

- [X] FilmAffinity import accepts raw HTML and ZIP exports and queues ratings/list files.
- [X] FilmAffinity ZIP exports are now extracted and queue ratings/list HTML files; direct HTML uploads remain supported.
- [X] SensCritique review page renders correctly; invalid nested discard form and underscore template variables were fixed.
- [ ] Collection sync identity bugs. Sync failed: 401 Client Error: Unauthorized for url: https://api.igdb.com/v4/collections
- [X] BnF loading is hardened against malformed cover headers and shortened ISBN-10 identifiers; provider tests pass.
- [X] Faster statistics: the page shell loads immediately, content is async, and per-user/date-range results are cached with a manual refresh.

- 
- 🔵 Nice To Have
  ---------------

- [X] Check features from https://github.com/dannyvfilms/Yamtrack and original [github.com/FuzzyGrim/Yamtrack](https://github.com/FuzzyGrim/Yamtrack); useful compatible updates were selectively brought over.
- [X] CSS refont for collections, give me options. Hybrid view, optional sub-series, and opt-in regional game grouping are implemented; broader matching remains conservative.
- [X] country map with side ranking; country entries now expand to clickable title searches
- [X] Music releases on the calendar page
- [X] Is there an automatic data extract? Export is available under Settings → Export Data.
- [X] Multi media collections (collections already support mixed media types)
- [X] JSON data export is available alongside CSV under Settings → Export Data.
- [X] Collection poster search offers selectable TMDB alternatives on the edit page.
- [X] Barry Trotter collection identity verified against the live library: collection source `hardcover_series`/`42629` contains all three matching Hardcover book IDs; current provider fetch returns positions 1–3.
- [X] Hardcover collection source is registered, searchable, syncable, and covered by focused tests; older stored rows may need one manual Sync to backfill positions.
- [X] Hardcover series can now be searched and selected from the collection picker; sync/fetch is covered by focused tests.
- [X] Update the README with collection, calendar, statistics, and curated-list features.
- [X] Arthur C. Clarke novels and SF Masterworks are included as Hardcover-backed curated book lists.
- [ ] Unrated items ? Show a page for it.
- [ ] Game awards goty list is wrong.
- [ ] Some lists have Unknown title(ID xxxxx)
- [ ] Group lists / Awards by media type
- [ ] Artist page should show albums rated
- [ ] Score on pages should be more noticeable

More lists to add later: additional verified publication/game/movie rankings and year-by-year snapshots.

pcgamer top 100

etc

top for each year from publications like idk skillup , ign, digital foundry, nofrag, etc

more lists for movies games etc

## Feature-first order

- [X] Finish regional-variant grouping for games (opt-in, conservative title suffix matching).
- [X] Add richer curated lists (more verified game/book lists); added AFI, IMDb, PC Gamer 2025 top-10 snapshots, Arthur C. Clarke novels, and SF Masterworks.
- [X] Audit and selectively bring over upstream feature improvements (home section controls, collection hierarchy, regional grouping, and existing calendar/export integrations).
- [X] Configurable home sections (hide In Progress or Planning rows).
- [X] Return to critical bugs after feature work; remaining infrastructure/data-provider issues are deferred.

Verification note: focused SensCritique review tests now render the page; two unrelated existing tests still fail during TMDB setup because the test fakeredis lacks the `SCRIPT` command. Statistics tests likewise contain legacy expectations and hit the same test-infrastructure limitation.
