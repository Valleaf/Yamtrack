"""Static curated-list fixtures used by the statistics list-progress section.

Mirrors app/awards_data.py exactly, just with "items" (ranked, no specific
year) instead of "winners" (dated). Each entry in LISTS describes one
curated list. ``items`` is a list of per-entry dicts. The ID key name
follows the pattern ``{source}_id`` (e.g. ``tmdb_id``, ``musicbrainz_id``).
``rank`` is the position within the list (1 = top), used only for display
ordering in the detail dropdown.

No live API calls are made from here or from the statistics page -- IDs
must be hand-resolved and committed, same workflow as awards_data.py.

TMDB IDs       : https://www.themoviedb.org/movie/<id>
MusicBrainz IDs: https://musicbrainz.org/release-group/<uuid> (release-group MBID)

Entries below are seeded with the well-known top of each list as comments
so the shape/order is right -- uncomment and fill in the real ID once
you've looked it up. Add more rows the same way.
"""

LISTS = [
    # ------------------------------------------------------------------ #
    #  Letterboxd Top 250 Narrative Feature Films                          #
    #  Source: https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/
    #  Note: this list is recalculated periodically from user ratings, so   #
    #  treat it as a snapshot as of whenever you last checked it.          #
    # ------------------------------------------------------------------ #
    {
        "slug": "letterboxd_top250",
        "name": "Letterboxd Top 250",
        "icon": "🎞️",
        "media_type": "movie",
        "source": "tmdb",
        "items": [
            # {"rank": 1, "tmdb_id": None},   # The Godfather
            # {"rank": 2, "tmdb_id": None},   # Parasite
            # {"rank": 3, "tmdb_id": None},   # Spider-Man: Across the Spider-Verse
            # {"rank": 4, "tmdb_id": None},   # Interstellar
            # {"rank": 5, "tmdb_id": None},   # Fight Club
            # Add tmdb_ids from themoviedb.org -- list order changes, re-check periodically
        ],
    },

    # ------------------------------------------------------------------ #
    #  Sight & Sound Greatest Films of All Time (2022 Critics' Poll)       #
    #  Source: https://www2.bfi.org.uk/sight-and-sound/greatest-films-all-time
    # ------------------------------------------------------------------ #
    {
        "slug": "sight_sound_top250",
        "name": "Sight & Sound Top 250 (2022)",
        "icon": "📽️",
        "media_type": "movie",
        "source": "tmdb",
        "items": [
            # {"rank": 1, "tmdb_id": None},   # Jeanne Dielman, 23 Quai du Commerce, 1080 Bruxelles
            # {"rank": 2, "tmdb_id": None},   # Vertigo
            # {"rank": 3, "tmdb_id": None},   # Citizen Kane
            # {"rank": 4, "tmdb_id": None},   # Tokyo Story
            # {"rank": 5, "tmdb_id": None},   # In the Mood for Love
            # {"rank": 6, "tmdb_id": None},   # 2001: A Space Odyssey
            # {"rank": 7, "tmdb_id": None},   # Beau Travail
            # {"rank": 8, "tmdb_id": None},   # Mulholland Drive
            # {"rank": 9, "tmdb_id": None},   # Man with a Movie Camera
            # {"rank": 10, "tmdb_id": None},  # Singin' in the Rain
            # Add tmdb_ids from themoviedb.org -- verify titles 11+ against the BFI list
        ],
    },

    # ------------------------------------------------------------------ #
    #  Edgar Wright's Favourite Films                                      #
    #  Source: Edgar Wright's published favourites list (verify exact      #
    #  edition/length before committing -- several versions circulate)     #
    # ------------------------------------------------------------------ #
    {
        "slug": "edgar_wright_favorites",
        "name": "Edgar Wright's Favorites",
        "icon": "🎬",
        "media_type": "movie",
        "source": "tmdb",
        "items": [
            # {"rank": 1, "tmdb_id": None},   # Confirm exact source list before populating
            # Add tmdb_ids from themoviedb.org
        ],
    },

    # ------------------------------------------------------------------ #
    #  BFI Greatest Films                                                  #
    #  Source: confirm which BFI list (this often overlaps with/is the     #
    #  same poll as Sight & Sound above -- check before duplicating)       #
    # ------------------------------------------------------------------ #
    {
        "slug": "bfi_best_films",
        "name": "BFI Best Films",
        "icon": "🇬🇧",
        "media_type": "movie",
        "source": "tmdb",
        "items": [
            # {"rank": 1, "tmdb_id": None},   # Confirm exact source list before populating
            # Add tmdb_ids from themoviedb.org
        ],
    },

    # ------------------------------------------------------------------ #
    #  1001 Albums You Must Hear Before You Die                            #
    #  Source: https://1001albumsgenerator.com/ or the book's official list#
    #  Uses MusicBrainz release-group MBIDs (matches the music tracker)    #
    # ------------------------------------------------------------------ #
    {
        "slug": "1001_albums",
        "name": "1001 Albums You Must Hear Before You Die",
        "icon": "💿",
        "media_type": "music",
        "source": "musicbrainz",
        "items": [
            # {"rank": 1, "musicbrainz_id": None},   # e.g. Sgt. Pepper's Lonely Hearts Club Band
            # Add musicbrainz_ids (release-group MBID) from musicbrainz.org
        ],
    },
]
