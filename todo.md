# 🔴 Critical Bugs

### Imports & Sync

- [X] FilmAffinity import accepts raw HTML and ZIP exports and queues ratings/list files.
- [X] FilmAffinity ZIP exports are now extracted and queue ratings/list HTML files; direct HTML uploads remain supported.
- [X] SensCritique review page renders correctly; invalid nested discard form and underscore template variables were fixed.
- [X] Collection sync identity bugs. Sync failed: 401 Client Error: Unauthorized for url: https://api.igdb.com/v4/collections — root cause was `_fetch_igdb_collection`/`_search_igdb_collection` missing the retry-on-401 pattern used everywhere else in igdb.py; also fixed `get_access_token()` swallowing a real auth failure into an `UnboundLocalError` instead of a clear error.
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
- [X] Game awards goty list is wrong. Root cause: the igdb_ids in awards_data.py's three GOTY blocks (Game Awards, DICE, Golden Joystick) were never actually verified against IGDB — most pointed at completely unrelated games (e.g. 2022/2023 Elden Ring/Baldur's Gate 3 ids were transposed; 2018 God of War pointed at "WWF Royal Rumble"; 2016 Overwatch pointed at "Captain Blood"; 2014 Dragon Age: Inquisition pointed at "WarioWare D.I.Y."). Verified correct id for every winner via a direct IGDB search (debug_goty.py / resolve_goty.py, still in src/ for reuse) and rewrote all three GOTY winner lists.
- [X] Full awards_data.py verification sweep (beyond GOTY). ~90% of non-Oscar/non-GOTY entries had wrong TMDB/IGDB/MAL ids (never actually verified against the providers). Verified and fixed all ~130 entries via a title-search resolver (resolve_all_awards.py, kept in src/ for reuse) cross-checked against each winner's `# comment`. Oscar Best Picture (98/98) and manga awards were already correct. Also found and merged a duplicate `bafta_best_film` slug (two AWARDS entries with the same slug, different/conflicting winner lists — kept the more complete, now-verified 24-winner block, dropped the wrong 15-winner duplicate). One entry still flagged `# TODO verify` in the file: César 2021 "De leur vivant" resolves to a film with a 2011 release date, a 10yr gap from the ceremony year — worth a manual sanity check. hardcover/bnf book & comic award categories are still empty stubs (source not auto-searchable by this script) — separate backlog item to populate.
- [X] "Unknown title (ID xxxxx)" — cause: awards/curated-list entries fall back to that placeholder when nobody has tracked the item AND its provider metadata cache is cold (statistics page is intentionally cache-only, no live calls). Added `backfill_award_and_list_metadata_cache` task to warm the cache for every ID in awards_data.py/external_lists_data.py. Also found and removed a dead `sync_external_lists` Celery task + weekly beat schedule entry left over from the pre-0074-migration ExternalList models — would have crashed every week; may still need `docker compose exec yamtrack python manage.py shell -c "from django_celery_beat.models import PeriodicTask; PeriodicTask.objects.filter(name='sync_external_lists').delete()"` to remove the stale DB row since DatabaseScheduler doesn't auto-drop it from settings.py alone. Run the new backfill manually to clear existing Unknown titles:
  `docker compose exec yamtrack python manage.py shell -c "from app.tasks import backfill_award_and_list_metadata_cache; backfill_award_and_list_metadata_cache.delay()"`
- [X] Group lists / Awards by media type. `get_awards_progress`/`get_list_progress` now return entries grouped into `[{"media_type", "label", "entries": [...]}, ...]` (sorted by label, entries sorted by name within each group) via a shared `_group_progress_entries_by_media_type` helper, and the Awards & Lists tab renders one labeled sub-section per media type instead of one long mixed grid. Cache shape changed — requires a statistics cache bump after deploy: `docker compose exec yamtrack python manage.py shell -c "from django.contrib.auth import get_user_model; from app.statistics import invalidate_statistics_cache; [invalidate_statistics_cache(u.id) for u in get_user_model().objects.all()]"`
- [ ] Artist page should show albums rated
- [ ] Score on pages should be more noticeable

More lists to add later: additional verified publication/game/movie rankings and year-by-year snapshots.

pcgamer top 100

etc

top for each year from publications like idk skillup , ign, digital foundry, nofrag, etc

more lists for movies games etc

all disneys, all best international best picture, more festivals winners if htey have (venice, san sebastian, sundance, cannes, venise, berlin,cesar etc)

Check auto sync. For instance i had chad powers season 2 in my planned, but the poster and episodes did not show up until i manually synced.

Also i had the gentlemen as finished after season 1. Season 2 was announced and it did not go into planned,nor did the series change to in progress.

## Feature-first order

- [X] Finish regional-variant grouping for games (opt-in, conservative title suffix matching).
- [X] Add richer curated lists (more verified game/book lists); added AFI, IMDb, PC Gamer 2025 top-10 snapshots, Arthur C. Clarke novels, and SF Masterworks.
- [X] Audit and selectively bring over upstream feature improvements (home section controls, collection hierarchy, regional grouping, and existing calendar/export integrations).
- [X] Configurable home sections (hide In Progress or Planning rows).
- [X] Return to critical bugs after feature work; remaining infrastructure/data-provider issues are deferred.

Verification note: focused SensCritique review tests now render the page; two unrelated existing tests still fail during TMDB setup because the test fakeredis lacks the `SCRIPT` command. Statistics tests likewise contain legacy expectations and hit the same test-infrastructure limitation.
