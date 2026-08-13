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
            {"rank": 1, "tmdb_id": 44012},   # Jeanne Dielman, 23, quai du Commerce, 1080 Bruxelles (1976)
            {"rank": 2, "tmdb_id": 426},   # Vertigo (1958)
            {"rank": 3, "tmdb_id": 15},   # Citizen Kane (1941)
            {"rank": 4, "tmdb_id": 18148},   # Tokyo Story (1953)
            {"rank": 5, "tmdb_id": 843},   # In the Mood for Love (2000)
            {"rank": 6, "tmdb_id": 62},   # 2001: A Space Odyssey (1968)
            {"rank": 7, "tmdb_id": 14626},   # Beau Travail (1998)
            {"rank": 8, "tmdb_id": 1018},   # Mulholland Drive (2001)
            {"rank": 9, "tmdb_id": 26317},   # Man with a Movie Camera (1929)
            {"rank": 10, "tmdb_id": 872},   # Singin' in the Rain (1951)
            {"rank": 11, "tmdb_id": 631},   # Sunrise: A Song of Two Humans (1927)
            {"rank": 12, "tmdb_id": 238},   # The Godfather (1972)
            {"rank": 13, "tmdb_id": 776},   # The Rules of the Game (1939)
            {"rank": 14, "tmdb_id": 499},   # Cléo from 5 to 7 (1962)
            {"rank": 15, "tmdb_id": 3114},   # The Searchers (1956)
            {"rank": 16, "tmdb_id": 27040},   # Meshes of the Afternoon (1943)
            {"rank": 17, "tmdb_id": 30017},   # Close-Up (1990)
            {"rank": 18, "tmdb_id": 797},   # Persona (1966)
            {"rank": 19, "tmdb_id": 28},   # Apocalypse Now (1979)
            {"rank": 20, "tmdb_id": 346},   # Seven Samurai (1954)
            {"rank": 21, "tmdb_id": 780},   # The Passion of Joan of Arc (1928)
            {"rank": 22, "tmdb_id": 20530},   # Late Spring (1949)
            {"rank": 23, "tmdb_id": 10227},   # PlayTime (1967)
            {"rank": 24, "tmdb_id": 925},   # Do the Right Thing (1989)
            {"rank": 25, "tmdb_id": 20108},   # Au Hasard Balthazar (1966)
            {"rank": 26, "tmdb_id": 3112},   # The Night of the Hunter (1955)
            {"rank": 27, "tmdb_id": 42044},   # Shoah (1985)
            {"rank": 28, "tmdb_id": 46919},   # Daisies (1966)
            {"rank": 29, "tmdb_id": 103},   # Taxi Driver (1976)
            {"rank": 30, "tmdb_id": 531428},   # Portrait of a Lady on Fire (2019)
            {"rank": 31, "tmdb_id": 1396},   # Mirror (1975)
            {"rank": 32, "tmdb_id": 539},   # Psycho (1960)
            {"rank": 33, "tmdb_id": 422},   # 8½ (1963)
            {"rank": 34, "tmdb_id": 43904},   # L'Atalante (1934)
            {"rank": 35, "tmdb_id": 5801},   # Pather Panchali (1955)
            {"rank": 36, "tmdb_id": 901},   # City Lights (1931)
            {"rank": 37, "tmdb_id": 832},   # M (1931)
            {"rank": 38, "tmdb_id": 239},   # Some Like It Hot (1959)
            {"rank": 39, "tmdb_id": 269},   # Breathless (1960)
            {"rank": 40, "tmdb_id": 567},   # Rear Window (1954)
            {"rank": 41, "tmdb_id": 1563},   # Sans Soleil (1982)
            {"rank": 42, "tmdb_id": 284},   # The Apartment (1960)
            {"rank": 43, "tmdb_id": 992},   # Sherlock Jr. (1924)
            {"rank": 44, "tmdb_id": 266},   # Contempt (1963)
            {"rank": 45, "tmdb_id": 643},   # Battleship Potemkin (1925)
            {"rank": 46, "tmdb_id": 78},   # Blade Runner (1982)
            {"rank": 47, "tmdb_id": 86814},   # News from Home (1977)
            {"rank": 48, "tmdb_id": 216},   # Ali: Fear Eats the Soul (1974)
            {"rank": 49, "tmdb_id": 713},   # The Piano (1993)
            {"rank": 50, "tmdb_id": 147},   # The 400 Blows (1959)
            {"rank": 51, "tmdb_id": 48035},   # Ordet (1955)
            {"rank": 52, "tmdb_id": 80560},   # Wanda (1970)
            {"rank": 53, "tmdb_id": 3175},   # Barry Lyndon (1975)
            {"rank": 54, "tmdb_id": 213},   # North by Northwest (1959)
            {"rank": 55, "tmdb_id": 17295},   # The Battle of Algiers (1966)
            {"rank": 56, "tmdb_id": 1398},   # Stalker (1979)
            {"rank": 57, "tmdb_id": 27432},   # Killer of Sheep (1977)
            {"rank": 58, "tmdb_id": 548},   # Rashomon (1950)
            {"rank": 59, "tmdb_id": 5156},   # Bicycle Thieves (1948)
            {"rank": 60, "tmdb_id": 129},   # Spirited Away (2001)
            {"rank": 61, "tmdb_id": 20532},   # Sansho the Bailiff (1954)
            {"rank": 62, "tmdb_id": 34148},   # Imitation of Life (1959)
            {"rank": 63, "tmdb_id": 5165},   # L'Avventura (1960)
            {"rank": 64, "tmdb_id": 2748},   # Journey to Italy (1954)
            {"rank": 65, "tmdb_id": 8392},   # My Neighbor Totoro (1988)
            {"rank": 66, "tmdb_id": 19542},   # The Red Shoes (1948)
            {"rank": 67, "tmdb_id": 19},   # Metropolis (1927)
            {"rank": 68, "tmdb_id": 895},   # Andrei Rublev (1966)
            {"rank": 69, "tmdb_id": 662},   # La Jetée (1962)
            {"rank": 70, "tmdb_id": 44379},   # The Gleaners and I (2000)
            {"rank": 71, "tmdb_id": 77771},   # Touki Bouki (1973)
            {"rank": 72, "tmdb_id": 1092},   # The Third Man (1949)
            {"rank": 73, "tmdb_id": 769},   # GoodFellas (1990)
            {"rank": 74, "tmdb_id": 289},   # Casablanca (1943)
            {"rank": 75, "tmdb_id": 68427},   # Daughters of the Dust (1991)
            {"rank": 76, "tmdb_id": 439},   # La Dolce Vita (1960)
            {"rank": 77, "tmdb_id": 376867},   # Moonlight (2016)
            {"rank": 78, "tmdb_id": 694},   # The Shining (1980)
            {"rank": 79, "tmdb_id": 11104},   # Chungking Express (1994)
            {"rank": 80, "tmdb_id": 793},   # Blue Velvet (1986)
            {"rank": 81, "tmdb_id": 4495},   # The Spirit of the Beehive (1973)
            {"rank": 82, "tmdb_id": 2786},   # Pierrot le Fou (1965)
            {"rank": 83, "tmdb_id": 116393},   # Histoire(s) du Cinéma 1a: All the (Hi)stories (1989)
            {"rank": 84, "tmdb_id": 28162},   # A Matter of Life and Death (1946)
            {"rank": 85, "tmdb_id": 3082},   # Modern Times (1936)
            {"rank": 86, "tmdb_id": 599},   # Sunset Boulevard (1950)
            {"rank": 87, "tmdb_id": 27019},   # Céline and Julie Go Boating (1974)
            {"rank": 88, "tmdb_id": 15804},   # A Brighter Summer Day (1991)
            {"rank": 89, "tmdb_id": 31414},   # Satantango (1994)
            {"rank": 90, "tmdb_id": 335},   # Once Upon a Time in the West (1968)
            {"rank": 91, "tmdb_id": 15244},   # A Man Escaped (1956)
            {"rank": 92, "tmdb_id": 961},   # The General (1926)
            {"rank": 93, "tmdb_id": 95597},   # Black Girl (1965)
            {"rank": 94, "tmdb_id": 11534},   # Tropical Malady (2004)
            {"rank": 95, "tmdb_id": 419430},   # Get Out (2017)
            {"rank": 96, "tmdb_id": 496243},   # Parasite (2019)
            {"rank": 97, "tmdb_id": 25538},   # Yi Yi (2000)
            {"rank": 98, "tmdb_id": 14696},   # Ugetsu (1953)
            {"rank": 99, "tmdb_id": 1040},   # The Leopard (1962)
            {"rank": 100, "tmdb_id": 27030},   # The Earrings of Madame de... (1953)
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
            {"rank": 1, "tmdb_id": 62},   # 2001: A Space Odyssey (1968)
            {"rank": 2, "tmdb_id": 429},   # The Good, the Bad and the Ugly (1966)
            {"rank": 3, "tmdb_id": 539},   # Psycho (1960)
            {"rank": 4, "tmdb_id": 872},   # Singin' in the Rain (1951)
            {"rank": 5, "tmdb_id": 931},   # Don't Look Now (1973)
            {"rank": 6, "tmdb_id": 103},   # Taxi Driver (1976)
            {"rank": 7, "tmdb_id": 27030},   # The Earrings of Madame de... (1953)
            {"rank": 8, "tmdb_id": 814},   # An American Werewolf in London (1981)
            {"rank": 9, "tmdb_id": 378},   # Raising Arizona (1987)
            {"rank": 10, "tmdb_id": 76341},   # Mad Max: Fury Road (2015)
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
            {"rank": 1, "musicbrainz_id": "5a5d9938-38a9-3f32-b03b-8f14f62b880a"},   # Frank Sinatra - In the Wee Small Hours
            # {"rank": 2, "musicbrainz_id": None},   # NO MATCH: Duke Ellington - Ellington at Newport '56 (1956)
            {"rank": 3, "musicbrainz_id": "0521aa7e-dabd-44dd-8846-0aae691bb48d"},   # Elvis Presley - Elvis Presley
            {"rank": 4, "musicbrainz_id": "d07b47f0-8170-4b56-a104-f597d98b9f19"},   # Frank Sinatra - Songs for Swingin’ Lovers
            {"rank": 5, "musicbrainz_id": "903d5fe8-ab43-33b2-9411-6738af50de19"},   # Miles Davis - Birth of the Cool
            {"rank": 6, "musicbrainz_id": "9dd87e9f-81d0-3d10-9a81-801083722273"},   # The Louvin Brothers - Tragic Songs of Life
            {"rank": 7, "musicbrainz_id": "1b464368-017c-3aba-8a2d-437bcf43b5d0"},   # Count Basie Orchestra - The Atomic Mr. Basie
            {"rank": 8, "musicbrainz_id": "a3d5e53b-9b31-3014-a9c7-b6bfacc7cad3"},   # Fats Domino - This Is Fats Domino!
            {"rank": 9, "musicbrainz_id": "a987042b-4fe0-35bb-9cca-7ff44b1ff5b4"},   # Little Richard - Here’s Little Richard
            {"rank": 10, "musicbrainz_id": "2f643039-2fbc-3ed6-a283-97f90ecdd401"},   # Louis Prima - The Wildest!
            {"rank": 11, "musicbrainz_id": "2b5535ee-adbe-33a5-8986-74eace9dd169"},   # Machito - Kenya
            {"rank": 12, "musicbrainz_id": "742751a6-c2f9-41fc-9604-21cd991a84c2"},   # Sabu Martinez - Palo Congo + Safari with Sabu + Sorcery!
            {"rank": 13, "musicbrainz_id": "d60a3486-7192-37ac-bbf0-d63c4c44377d"},   # The Crickets - The “Chirping” Crickets
            {"rank": 14, "musicbrainz_id": "764d0d9e-68b1-39fe-b1d1-eda104926777"},   # Thelonious Monk - Brilliant Corners
            {"rank": 15, "musicbrainz_id": "74fdc36c-ffa6-44a2-942a-cab1b47987e1"},   # Billie Holiday - Lady in Satin
            {"rank": 16, "musicbrainz_id": "962e0e61-0566-331c-9b9c-515256ae1a89"},   # Jack Elliott - Jack Takes the Floor
            {"rank": 17, "musicbrainz_id": "263137e2-45d4-338a-abeb-464624b79c68"},   # Ella Fitzgerald - Live at Mister Kelly’s
            {"rank": 18, "musicbrainz_id": "522f179f-7c31-3a7c-95ed-c22218eba84f"},   # Tito Puente - Dance Mania
            {"rank": 19, "musicbrainz_id": "035a7881-3e2c-39d2-b110-fe26a4de94e5"},   # The Dave Brubeck Quartet - Time Out
            {"rank": 20, "musicbrainz_id": "46f86dbe-4f1f-4a48-8821-6432feb6f293"},   # Ella Fitzgerald - Ella Fitzgerald Sings the George and Ira Gershwin Song Book
            {"rank": 21, "musicbrainz_id": "81e9ea0b-e334-35b3-9d10-f9a5f8bea5ae"},   # Marty Robbins - Gunfighter Ballads and Trail Songs
            {"rank": 22, "musicbrainz_id": "8e8a594f-2175-38c7-a871-abb68ec363e7"},   # Miles Davis - Kind of Blue
            {"rank": 23, "musicbrainz_id": "26ea6822-538d-3781-ac19-fd3575aa2688"},   # Ray Charles - The Genius of Ray Charles
            {"rank": 24, "musicbrainz_id": "21ef891b-bc3a-3e0f-9fc2-9ca294818dbd"},   # The Everly Brothers - A Date With The Everly Brothers
            {"rank": 25, "musicbrainz_id": "4524e346-681e-364d-b975-bad70d71f2d7"},   # Elvis Presley - Elvis Is Back!
            {"rank": 26, "musicbrainz_id": "4295b820-6c50-4fd7-8824-3afe1f9e109e"},   # Joan Baez - Joan Baez
            {"rank": 27, "musicbrainz_id": "64b75de0-e230-3421-8093-20338ccd6316"},   # Miriam Makeba - Miriam Makeba
            {"rank": 28, "musicbrainz_id": "2c1288fa-19c4-34d3-97a7-ff2fe9c96b57"},   # Muddy Waters - Muddy Waters at Newport 1960
            {"rank": 29, "musicbrainz_id": "79a8fca9-2678-3c9c-a18f-b6f715d2375d"},   # Bill Evans Trio - Sunday at the Village Vanguard
            {"rank": 30, "musicbrainz_id": "10bb15b0-2d55-369a-90c3-a5131406ac9e"},   # Jimmy Smith - Back at the Chicken Shack
            {"rank": 31, "musicbrainz_id": "bb95b270-0fc0-3d64-b264-eb9f15343d57"},   # Booker T. & the M.G.s - Green Onions
            {"rank": 32, "musicbrainz_id": "38671d62-32bd-399d-abbd-0f685c2fd4a3"},   # Ray Charles - Modern Sounds in Country and Western Music
            {"rank": 33, "musicbrainz_id": "193b6907-a428-46d2-bc7d-3ce70ac80783"},   # Sadao Watanabe - Jazz Samba
            {"rank": 34, "musicbrainz_id": "48070ee2-1865-3b11-ba36-360b1453a37a"},   # Charles Mingus - The Black Saint and the Sinner Lady
            {"rank": 35, "musicbrainz_id": "a2bad96f-a572-38f2-b362-5865dedc0d35"},   # James Brown - Live at the Apollo, 1962
            {"rank": 36, "musicbrainz_id": "5c0dcf13-d571-422a-a9c8-162b26eb970e"},   # Johnny Reid - A Christmas Gift to You
            {"rank": 37, "musicbrainz_id": "f1518424-9ed0-3418-b2c3-5a52050a76e5"},   # Ray Price - Night Life
            {"rank": 38, "musicbrainz_id": "1c17ea9a-97d1-33ed-930f-f4c28222d37f"},   # Sam Cooke - Live at the Harlem Square Club, 1963
            {"rank": 39, "musicbrainz_id": "a63dc65f-09f2-359b-a10e-648f00ecd96c"},   # The Beatles - With The Beatles
            {"rank": 40, "musicbrainz_id": "bf40678e-67a3-304e-9c80-1eae9dc1940a"},   # Bert Jansch - Bert Jansch
            {"rank": 41, "musicbrainz_id": "169b62aa-c3a5-3ed9-bed1-cc47c4bc51ad"},   # Bob Dylan - The Freewheelin’ Bob Dylan
            {"rank": 42, "musicbrainz_id": "813ecf80-7a92-3188-8eda-915dbbdbd43d"},   # Dusty Springfield - A Girl Called Dusty
            {"rank": 43, "musicbrainz_id": "d2668bde-5c6d-4d6f-b0a7-ec73041d1570"},   # Johnny Hallyday - Olympia 64
            {"rank": 44, "musicbrainz_id": "77cf47ba-58cd-3f3d-a5f9-79bf89860421"},   # John Coltrane - A Love Supreme
            {"rank": 45, "musicbrainz_id": "57e22d34-0274-38f4-8036-6f98cb5a32d4"},   # Solomon Burke - Rock ’n Soul
            {"rank": 46, "musicbrainz_id": "1ae98569-1603-3f38-8bc3-158d9430ff78"},   # Stan Getz - Getz/Gilberto #2
            {"rank": 47, "musicbrainz_id": "5dd5517d-7b23-4662-b10a-b633dbc133e6"},   # The Beatles - A Hard Day’s Night / A Hard Day’s Night
            {"rank": 48, "musicbrainz_id": "ddcf6ffe-5614-386f-a069-219fd32b8350"},   # The Rolling Stones - The Rolling Stones
            {"rank": 49, "musicbrainz_id": "a4d2a86c-bbd6-352b-b9fa-f9da86df842c"},   # B.B. King - Live at the Regal
            {"rank": 50, "musicbrainz_id": "6cadda7c-fbd0-3b19-9546-56915e3305d8"},   # Bob Dylan - Bringing It All Back Home
            {"rank": 51, "musicbrainz_id": "fb48b1dc-412f-36aa-8820-1023c08c46c6"},   # Bob Dylan - Highway 61 Revisited
            {"rank": 52, "musicbrainz_id": "6d86b87e-43e5-3631-bb46-84cb65b3f303"},   # Buck Owens - I’ve Got a Tiger by the Tail
            {"rank": 53, "musicbrainz_id": "58e8a7a7-060e-32e0-97da-f4ccf039b3e2"},   # Jerry Lee Lewis - “Live” at the Star‐Club, Hamburg
            # {"rank": 54, "musicbrainz_id": None},   # NO MATCH: Otis Redding - Otis Blue: Otis Redding Sings Soul (1965)
            {"rank": 55, "musicbrainz_id": "2b581513-39cc-3a81-9c50-79a8dbf5c031"},   # The Beach Boys - The Beach Boys Today!
            {"rank": 56, "musicbrainz_id": "dca03435-8adb-30a5-ba82-5a162267ff38"},   # The Beatles - Rubber Soul
            {"rank": 57, "musicbrainz_id": "dda9ce86-7b6a-335d-9296-61eb86718433"},   # The Byrds - Mr. Tambourine Man
            {"rank": 58, "musicbrainz_id": "d03da025-4f5b-35fc-9add-cbdb583ba516"},   # The Sonics - Here Are The Sonics!!!
            {"rank": 59, "musicbrainz_id": "b2e77472-77ba-4371-9374-df2ce87d9a90"},   # The Who - My Generation
            {"rank": 60, "musicbrainz_id": "329fb554-2a81-3d8a-8e22-ec2c66810019"},   # Bob Dylan - Blonde on Blonde
            {"rank": 61, "musicbrainz_id": "da5c8b77-c542-3a9e-b5f8-982bbbb31c84"},   # Donovan - Sunshine Superman
            {"rank": 62, "musicbrainz_id": "44895ae9-5c04-3e65-8ead-672d1b24ac84"},   # The Mothers of Invention - Freak Out!
            {"rank": 63, "musicbrainz_id": "43e95a39-7f85-3400-af58-03b800e63048"},   # Fred Neil - Fred Neil
            # {"rank": 64, "musicbrainz_id": None},   # NO MATCH: John Mayall's Bluesbreakers - Bluesbreakers with Eric Clapton (1966)
            {"rank": 65, "musicbrainz_id": "6399b0c8-a1a0-3674-92b5-585a574fdf20"},   # The Mama’s and the Papa’s - If You Can Believe Your Eyes and Ears
            {"rank": 66, "musicbrainz_id": "b4433a3e-d5ad-3d99-965c-96bfb6a0f071"},   # Nina Simone - Wild Is the Wind
            {"rank": 67, "musicbrainz_id": "dee8221e-7d95-3927-a800-a44fdf1755cf"},   # Paul Revere and the Raiders - Midnight Ride
            {"rank": 68, "musicbrainz_id": "aa8211e7-2a00-4fdd-998c-37872efc33d4"},   # Simon & Garfunkel - Parsley, Sage, Rosemary and Thyme / Bookends
            {"rank": 69, "musicbrainz_id": "6577ce2b-1be3-4ed0-92c6-f78175280bae"},   # 13th Floor Elevators - The Psychedelic Sounds of the 13th Floor Elevators
            {"rank": 70, "musicbrainz_id": "fdd96703-7b21-365e-bdea-38029fbeb84e"},   # The Beach Boys - Pet Sounds
            {"rank": 71, "musicbrainz_id": "72d15666-99a7-321e-b1f3-a3f8c09dff9f"},   # The Beatles - Revolver
            {"rank": 72, "musicbrainz_id": "8b98a364-6551-379f-89ea-c3fed4d5552f"},   # The Byrds - Fifth Dimension
            {"rank": 73, "musicbrainz_id": "9e3bff06-c552-345b-a10b-aeb6061e1a8a"},   # The Kinks - Face to Face
            {"rank": 74, "musicbrainz_id": "f0d042e6-6f09-4860-ae7c-d6c70cd613db"},   # The Monks - Black Monk Time
            {"rank": 75, "musicbrainz_id": "26987c39-5914-483b-a897-d43ce6aad9b1"},   # The Rolling Stones - Aftermath
            {"rank": 76, "musicbrainz_id": "051e7eb4-a90a-36fd-99aa-5db693ba3a07"},   # The Yardbirds - Yardbirds
            {"rank": 77, "musicbrainz_id": "7d8f07a7-4c64-3afb-8daf-8f1d4df89a78"},   # Aretha Franklin - I Never Loved a Man the Way I Love You
            {"rank": 78, "musicbrainz_id": "28768f4d-dd43-382d-a56f-79ddfa6597a9"},   # Buffalo Springfield - Buffalo Springfield Again
            {"rank": 79, "musicbrainz_id": "7e71ad8b-6cbd-3cc0-8087-3ab222e91c20"},   # Captain Beefheart & His Magic Band - Safe as Milk
            {"rank": 80, "musicbrainz_id": "11351784-a205-3a5c-a04c-712b645da99c"},   # Country Joe and the Fish - Electric Music For The Mind And Body
            {"rank": 81, "musicbrainz_id": "bbd66e31-ac27-3432-81a7-0d4b4b4c5de5"},   # Cream - Disraeli Gears
            {"rank": 82, "musicbrainz_id": "943461cc-377c-3f96-9d89-4d3ff5b03d25"},   # Francis Albert Sinatra - Francis Albert Sinatra & Antônio Carlos Jobim
            {"rank": 83, "musicbrainz_id": "e6440cd2-5e8e-367d-bc49-cc042b5ef524"},   # Jefferson Airplane - Surrealistic Pillow
            {"rank": 84, "musicbrainz_id": "4ba8b8c5-e417-3862-b718-0eae1cd4b212"},   # Loretta Lynn - Don’t Come Home a Drinkin’ (With Lovin’ on Your Mind)
            {"rank": 85, "musicbrainz_id": "4cc16c40-ef3a-36d9-9f96-89cbf1c61ec6"},   # Love - Da Capo
            {"rank": 86, "musicbrainz_id": "c7035bc6-6101-326f-992c-401d451c1716"},   # Love - Forever Changes
            {"rank": 87, "musicbrainz_id": "034570c1-b9e7-421a-a6a1-2857b01589b5"},   # Merle Haggard - I'm a Lonesome Fugitive
            {"rank": 88, "musicbrainz_id": "483f15b5-e784-3c78-ba40-1988f5f9c6a4"},   # Moby Grape - Moby Grape
            {"rank": 89, "musicbrainz_id": "ffa420fb-1bb3-3b67-8577-165429008835"},   # Nico - Chelsea Girl
            {"rank": 90, "musicbrainz_id": "6792b6d1-4e65-3c3c-9d20-d08aa1dcfc60"},   # Pink Floyd - The Piper at the Gates of Dawn
            {"rank": 91, "musicbrainz_id": "9f7a4c28-8fa2-3113-929c-c47a9f7982c3"},   # The Beatles - Sgt. Pepper’s Lonely Hearts Club Band
            {"rank": 92, "musicbrainz_id": "61b378ff-7f9b-3e89-9ee2-5069afc8c357"},   # The Beau Brummels - Triangle
            {"rank": 93, "musicbrainz_id": "4e4c1014-7c7b-397a-9c80-35b115a034fe"},   # The Byrds - Younger Than Yesterday
            {"rank": 94, "musicbrainz_id": "00a9c3d9-13c7-355b-b216-108c81ad3f78"},   # The Doors - The Doors
            {"rank": 95, "musicbrainz_id": "1a725575-a70d-4401-b66e-ecf66344c5d8"},   # Deviled Ham - I Had Too Much to Dream Last Night
            {"rank": 96, "musicbrainz_id": "791fdbb8-b19c-4d33-9ba4-d2d2f35abec6"},   # The Jimi Hendrix Experience - Are You Experienced
            {"rank": 97, "musicbrainz_id": "d0b1e21e-cef6-4575-8d92-1afea1894ca3"},   # The Jimi Hendrix Experience - Axis: Bold as Love
            {"rank": 98, "musicbrainz_id": "ab0ea2d3-a273-3d7f-855b-f9930a1395cf"},   # The Kinks - Something Else by The Kinks
            {"rank": 99, "musicbrainz_id": "60ea3167-8594-3d42-9904-e48efaea09b3"},   # The Monkees - Headquarters
            {"rank": 100, "musicbrainz_id": "6bf4d078-7bc6-32a1-8edf-0ef1bcb7a5df"},   # The Mothers of Invention - We’re Only in It for the Money
            {"rank": 101, "musicbrainz_id": "5cbd9d7b-597a-3c5e-bfd1-c2b364215560"},   # The Velvet Underground - The Velvet Underground & Nico
            {"rank": 102, "musicbrainz_id": "fc0885e0-0284-3f9d-81ee-17c5e7196346"},   # The Velvet Underground - White Light/White Heat
            {"rank": 103, "musicbrainz_id": "aa02a102-f7b5-3584-8d21-bd9c560effb6"},   # The Who - The Who Sell Out
            {"rank": 104, "musicbrainz_id": "56829851-672a-3921-827f-23252811f0e6"},   # The Young Rascals - Groovin’
            {"rank": 105, "musicbrainz_id": "2e569a55-d829-31c8-9016-0c9a56333288"},   # Tim Buckley - Goodbye and Hello
            {"rank": 106, "musicbrainz_id": "95eb3295-0606-3f79-87ff-204faac15c6a"},   # Alexander “Skip” Spence - Oar
            # {"rank": 107, "musicbrainz_id": None},   # NO MATCH: Aretha Franklin - Aretha: Lady Soul (1968)
            {"rank": 108, "musicbrainz_id": "1b08b70f-61a6-3f78-880c-d0bc4d204d83"},   # Astrud Gilberto - Beach Samba
            {"rank": 109, "musicbrainz_id": "02de8887-e93b-3ea6-8b6d-de072a159bba"},   # Big Brother & the Holding Company - Cheap Thrills
            {"rank": 110, "musicbrainz_id": "97fd4dc6-6a19-3ae1-b063-6fcdcc061e6b"},   # Blue Cheer - Vincebus Eruptum
            {"rank": 111, "musicbrainz_id": "d18dfcfe-af78-31c7-bcd5-f732b982d568"},   # Caetano Veloso - Caetano Veloso
            {"rank": 112, "musicbrainz_id": "a8b024d4-a8da-4aa9-9ea5-bb211db21259"},   # Iron Butterfly - In-A-Gadda-Da-Vida
            {"rank": 113, "musicbrainz_id": "9012914a-49e2-3f0a-bde9-25276c968b9f"},   # Robben Ford - Truth
            # {"rank": 114, "musicbrainz_id": None},   # NO MATCH: Johnny Cash - Johnny Cash at Folsom Prison (1968)
            {"rank": 115, "musicbrainz_id": "c5410670-fce4-3139-9fab-6806d79171c5"},   # Laura Nyro - Eli and the Thirteenth Confession
            {"rank": 116, "musicbrainz_id": "34291a49-8df9-304e-bd39-16b11d829d5f"},   # Leonard Cohen - Songs of Leonard Cohen
            {"rank": 117, "musicbrainz_id": "d603eca5-7b29-45e3-ac9f-91aef04a684e"},   # Os Mutantes - Os Mutantes
            {"rank": 118, "musicbrainz_id": "f1d60bab-675d-35e1-9804-a28b28cc96da"},   # Ravi Shankar - The Sounds of India
            {"rank": 119, "musicbrainz_id": "e14cb590-dbcb-34fe-9860-881e1a0a1bda"},   # Scott Walker - Scott 2
            {"rank": 120, "musicbrainz_id": "6329db5a-77c2-30b4-9fa0-aca1151f7e26"},   # Shivkumar Sharma - Call of the Valley
            {"rank": 121, "musicbrainz_id": "f4a26672-dcd8-342d-ad09-2b612d91c9fb"},   # Simon & Garfunkel - Bookends
            {"rank": 122, "musicbrainz_id": "466fddac-8006-3e71-bbe7-7aa0f587aa88"},   # The Band - Music From Big Pink
            {"rank": 123, "musicbrainz_id": "ea6f4e02-1ebd-4b64-8dfe-dbb8535f18b8"},   # The Beatles - The Beatles
            {"rank": 124, "musicbrainz_id": "5f8c3b00-bdfe-38ea-8a5d-61dc7e50882e"},   # The Byrds - The Notorious Byrd Brothers
            {"rank": 125, "musicbrainz_id": "2a02ea31-7a7f-3a46-8a46-aebfac434a81"},   # The Byrds - Sweetheart of the Rodeo
            {"rank": 126, "musicbrainz_id": "a057476f-ad3c-3b54-a763-30bad2497977"},   # The Incredible String Band - The Hangman’s Beautiful Daughter
            {"rank": 127, "musicbrainz_id": "47ba2d59-5544-34a4-b108-dc08c0956298"},   # The Jimi Hendrix Experience - Electric Ladyland
            {"rank": 128, "musicbrainz_id": "4516a30e-939c-3b2b-a8ea-f94ae418d3a6"},   # The Kinks - The Kinks Are the Village Green Preservation Society
            {"rank": 129, "musicbrainz_id": "93181a2a-e241-3856-be77-e3c6885884f6"},   # The Pretty Things - S.F. Sorrow
            {"rank": 130, "musicbrainz_id": "6e672bbd-7c7f-32f8-8335-c603be99d13b"},   # The Rolling Stones - Beggars Banquet
            # {"rank": 131, "musicbrainz_id": None},   # NO MATCH: Small Faces - Ogden's Nut Gone Flake (1968)
            {"rank": 132, "musicbrainz_id": "374ef16c-489b-3a3a-91f6-820827807469"},   # The United States of America - The United States of America
            {"rank": 133, "musicbrainz_id": "844c1dc4-2daf-4c08-982a-9f098e8dc3f2"},   # The Who - Tommy
            {"rank": 134, "musicbrainz_id": "9a4a9ebf-f4f7-3dba-9b80-0b274cbc80f9"},   # The Zombies - Odessey and Oracle
            {"rank": 135, "musicbrainz_id": "50701e2b-a074-380e-82aa-cfb21421dbb4"},   # Tim Buckley - Happy Sad
            {"rank": 136, "musicbrainz_id": "b53d5537-10e1-4df9-ab4e-7e376872dbb8"},   # Traffic - Traffic
            {"rank": 137, "musicbrainz_id": "f92e55ef-e35d-3254-a627-191f3b3c9677"},   # Blood, Sweat & Tears - Blood, Sweat & Tears
            {"rank": 138, "musicbrainz_id": "e6a580bd-5d29-3acd-a959-0bfab002ee6f"},   # Captain Beefheart & His Magic Band - Trout Mask Replica
            {"rank": 139, "musicbrainz_id": "fcbd5820-c7c6-40d3-b1c8-5c5f8d8ac1cc"},   # Chicago - Chicago Transit Authority: Texas Pop Festival 1969 (Live)
            {"rank": 140, "musicbrainz_id": "ef55850c-7b38-30fc-8f8d-d10f28784094"},   # Creedence Clearwater Revival - Bayou Country
            {"rank": 141, "musicbrainz_id": "6c08878c-d6a1-37b6-84c3-9566748545c1"},   # Creedence Clearwater Revival - Green River
            {"rank": 142, "musicbrainz_id": "f08da765-9592-42ae-b434-449d3a7e55c2"},   # Crosby, Stills & Nash - Crosby, Stills & Nash
            {"rank": 143, "musicbrainz_id": "9e463288-9694-4d3d-b6e2-287e81cebdba"},   # Dr. John - Gris-Gris Gumbo Ya Ya: Singles 1968-1974
            {"rank": 144, "musicbrainz_id": "aac8700b-8f62-30fc-ac2a-23b6cb37e3c3"},   # Dusty Springfield - Dusty in Memphis
            {"rank": 145, "musicbrainz_id": "2a753764-89d5-3b72-8dff-8c599f1ea925"},   # Elvis Presley - From Elvis in Memphis
            {"rank": 146, "musicbrainz_id": "3a6b89d1-ae82-3710-8e71-765405aa8a78"},   # Fairport Convention - Liege & Lief
            {"rank": 147, "musicbrainz_id": "a0a9d6a6-c3fe-367a-bc8c-449285c6c473"},   # Fairport Convention - Unhalfbricking
            {"rank": 148, "musicbrainz_id": "3f974fbd-9db8-3dff-9466-b9ae6fd9146c"},   # Frank Zappa - Hot Rats
            {"rank": 149, "musicbrainz_id": "e76d4f75-f09b-3f5b-aca9-44ac4489e58d"},   # Isaac Hayes - Hot Buttered Soul
            {"rank": 150, "musicbrainz_id": "50df1aa9-6c37-46da-90bd-140363ddf878"},   # Johnny Cash - Johnny Cash at San Quentin
            {"rank": 151, "musicbrainz_id": "a50636b5-5233-3329-a7f3-dba3d0e00ef7"},   # King Crimson - In the Court of the Crimson King
            {"rank": 152, "musicbrainz_id": "07e182ae-6567-4bc4-90f0-73619c942d73"},   # Led Zeppelin - Led Zeppelin x Led Zeppelin
            {"rank": 153, "musicbrainz_id": "33b4653d-006e-3cc1-8afb-386b15a6cd6e"},   # Led Zeppelin - Led Zeppelin II
            {"rank": 154, "musicbrainz_id": "0c0d5696-5d29-3809-8b79-4bf1320f0353"},   # Leonard Cohen - Songs From a Room
            {"rank": 155, "musicbrainz_id": "7d0a9612-7636-34fe-84d9-445c8df9c0f3"},   # Miles Davis - In a Silent Way
            {"rank": 156, "musicbrainz_id": "f61603ab-ef6b-386b-a5e0-aaefc00543f1"},   # Neil Young - Everybody Knows This Is Nowhere
            {"rank": 157, "musicbrainz_id": "b9c4fc17-0dc5-3aa5-b1b9-08e1446e5bea"},   # Nick Drake - Five Leaves Left
            {"rank": 158, "musicbrainz_id": "4180c3fa-faf6-3945-b7e4-7f887c7c681f"},   # The Pentangle - Basket of Light
            {"rank": 159, "musicbrainz_id": "688f6d4d-c035-3454-b840-62d191d305e9"},   # Quicksilver Messenger Service - Happy Trails
            {"rank": 160, "musicbrainz_id": "c33d96bd-94fa-30ba-a83a-8809f34e9f76"},   # Scott Walker - Scott 4
            {"rank": 161, "musicbrainz_id": "86871123-60e4-30a5-aae3-36e810e0964b"},   # Sly and the Family Stone - Stand!
            {"rank": 162, "musicbrainz_id": "0213dd3c-b0f7-4195-b12f-3f12d307897f"},   # The Band - The Band
            {"rank": 163, "musicbrainz_id": "9162580e-5df4-32de-80cc-f45a8d8a9b1d"},   # The Beatles - Abbey Road
            {"rank": 164, "musicbrainz_id": "8272c9c4-bc81-3409-8299-9c5b00b45bf5"},   # The Johnsons - Odessa
            {"rank": 165, "musicbrainz_id": "a7562b15-0ee5-35cf-b9ce-38d892475521"},   # The Flying Burrito Brothers - The Gilded Palace of Sin / Burrito Deluxe
            {"rank": 166, "musicbrainz_id": "cd27ba91-162e-3d8a-8042-9451b84aa78e"},   # The Kinks - Arthur (or The Decline and Fall of the British Empire)
            {"rank": 167, "musicbrainz_id": "44410403-45d3-30fa-ba48-d16664bf6fb3"},   # MC5 - Kick Out the Jams
            {"rank": 168, "musicbrainz_id": "784c0edd-0f37-33a2-9ca5-dff87b4f999c"},   # The Rolling Stones - Let It Bleed
            {"rank": 169, "musicbrainz_id": "18037a41-2695-3a8f-a732-f6653a7f125b"},   # The Stooges - The Stooges
            {"rank": 170, "musicbrainz_id": "e6c7e050-119b-3c99-92f6-039137c4a18d"},   # The Temptations - Cloud Nine
            {"rank": 171, "musicbrainz_id": "a616dcf5-7a1f-3afe-a53b-27281c2bf75e"},   # The Velvet Underground - The Velvet Underground
            {"rank": 172, "musicbrainz_id": "321fe6af-3eef-30b1-a5c2-7b36b0a4aae1"},   # The Youngbloods - Elephant Mountain
            {"rank": 173, "musicbrainz_id": "7d568f14-d86e-3584-97d0-c1824599de04"},   # Van Morrison - Astral Weeks
            {"rank": 174, "musicbrainz_id": "984be675-d4d4-3e1a-b6ee-3872fa353c5c"},   # Ananda Shankar - Ananda Shankar
            {"rank": 175, "musicbrainz_id": "d38fc9a6-62bd-40bd-8162-7a4146d3e519"},   # Black Sabbath - Black Sabbath
            {"rank": 176, "musicbrainz_id": "1df63269-fbc8-48ff-b7fa-b55ce8aab8a1"},   # Black Sabbath - Paranoid
            {"rank": 177, "musicbrainz_id": "418678e7-2807-3bed-a305-11b4181e533e"},   # Cat Stevens - Tea for the Tillerman
            {"rank": 178, "musicbrainz_id": "3412fd44-c6e6-3a3b-b91a-964a055192ec"},   # Crosby, Stills, Nash & Young - Déjà vu
            {"rank": 179, "musicbrainz_id": "ebdb53c3-fbae-34b1-81cb-f825c9a56822"},   # Deep Purple - Deep Purple in Rock
            {"rank": 180, "musicbrainz_id": "ba53dcbd-9328-3cf7-bc72-179b4512867e"},   # Derek and the Dominos - Layla and Other Assorted Love Songs
            {"rank": 181, "musicbrainz_id": "d4b0f3e2-e3eb-3531-b305-ed8105cb5be4"},   # George Harrison - All Things Must Pass
            {"rank": 182, "musicbrainz_id": "03e56c64-2ee7-4020-ab17-addcd7e251e6"},   # Reuben Wilson - Fun House
            {"rank": 183, "musicbrainz_id": "a3a2756d-93b4-37c6-8b82-513070ef58d6"},   # James Taylor - Sweet Baby James
            {"rank": 184, "musicbrainz_id": "8be83468-4917-390d-82b6-d890f058cd22"},   # John Lennon - John Lennon/Plastic Ono Band
            {"rank": 185, "musicbrainz_id": "53f80f76-f8af-3558-bfd5-e7221e055c75"},   # Led Zeppelin - Led Zeppelin III
            {"rank": 186, "musicbrainz_id": "d6a52dc7-f4fa-4d10-89d9-5a99d178dae9"},   # Paul McCartney - McCartney
            {"rank": 187, "musicbrainz_id": "a9e30282-5b37-3f92-b897-b9659a1a312b"},   # Miles Davis - Bitches Brew
            {"rank": 188, "musicbrainz_id": "70aa51b4-3b78-3e71-bc2d-67c354200c1c"},   # The Avalanches - After the Goldrush
            {"rank": 189, "musicbrainz_id": "d742fded-00e7-3746-a63d-aa2def3fdbcc"},   # Nick Drake - Bryter Layter
            {"rank": 190, "musicbrainz_id": "a19460f8-19fa-3bd6-987a-799b32d701e2"},   # Rod Stewart - Gasoline Alley
            {"rank": 191, "musicbrainz_id": "43424c73-fc58-36b0-b9cf-f8b057ac0603"},   # Santana - Abraxas
            {"rank": 192, "musicbrainz_id": "9d113e91-dc99-47d8-8a86-22d2bfc00518"},   # Simon & Garfunkel - Bridge Over Troubled Water / Sounds of Silence
            {"rank": 193, "musicbrainz_id": "9fabbd9f-c6a2-3773-91ce-6ef937d47daa"},   # Soft Machine - Third
            # {"rank": 194, "musicbrainz_id": None},   # NO MATCH: Spirit - Twelve Dreams of Doctor Sardonicus (1970)
            {"rank": 195, "musicbrainz_id": "9bb9b77e-0a1a-3de1-bbc4-c31e3a61445c"},   # Stephen Stills - Stephen Stills
            {"rank": 196, "musicbrainz_id": "f8d4bee5-0b74-3bb4-9010-2a454adbfbe7"},   # Syd Barrett - The Madcap Laughs
            {"rank": 197, "musicbrainz_id": "e994261c-6e55-37b3-8f78-dde48667e185"},   # Rigmor Gustafsson - Close to You
            {"rank": 198, "musicbrainz_id": "deee6f92-2662-3095-8aea-6892b10b8265"},   # The Doors - Morrison Hotel
            {"rank": 199, "musicbrainz_id": "994c2c59-d32f-304e-8f53-bda17a254f52"},   # Grateful Dead - American Beauty
            {"rank": 200, "musicbrainz_id": "4c442102-c2d2-33ca-8c11-80db9e569420"},   # The Grateful Dead - Live/Dead
            {"rank": 201, "musicbrainz_id": "0ba3b960-9b4b-3191-bcc5-1e51169e5955"},   # The Who - Live at Leeds
            {"rank": 202, "musicbrainz_id": "3770d5ce-e0e1-3389-9acf-cd38f0722baf"},   # Traffic - John Barleycorn Must Die
            {"rank": 203, "musicbrainz_id": "16506432-d133-3b2f-a504-dc88966dad2a"},   # Van Morrison - Moondance
            {"rank": 204, "musicbrainz_id": "13d08c0e-14e2-30b2-9ad7-5f501761a8ea"},   # Can - Tago Mago
            {"rank": 205, "musicbrainz_id": "6e4f39e6-3403-39d7-81c6-8e61a990d509"},   # Carole King - Tapestry
            {"rank": 206, "musicbrainz_id": "3a31800f-1916-3f4c-a7ae-26b783d00670"},   # Creedence Clearwater Revival - Cosmo’s Factory
            {"rank": 207, "musicbrainz_id": "c1d70ab6-f857-3aa2-b6f5-a8cb080b7844"},   # David Crosby - If I Could Only Remember My Name
            {"rank": 208, "musicbrainz_id": "2c98f21a-e2af-3412-a253-de9a1e06d7f7"},   # Dolly Parton - Coat of Many Colors
            {"rank": 209, "musicbrainz_id": "1189a8bc-f356-3c0a-a689-d8e0d1b5e4b8"},   # Don McLean - American Pie
            {"rank": 210, "musicbrainz_id": "9c371adb-37de-308c-88ea-8e52248ab1a1"},   # Elton John - Madman Across the Water
            {"rank": 211, "musicbrainz_id": "e940f4e4-1b0a-3d83-9ccd-6ed712a55b3c"},   # Emerson, Lake & Palmer - Tarkus
            {"rank": 212, "musicbrainz_id": "b1fff2ac-34eb-358b-9bf5-196b2a5fc288"},   # Emerson, Lake & Palmer - Pictures at an Exhibition
            {"rank": 213, "musicbrainz_id": "90d7d3e2-d544-3c66-ab84-84a986476460"},   # Fela Ransome‐Kuti - Live!
            {"rank": 214, "musicbrainz_id": "a334e612-e736-3b4f-82b4-c4dfb774983c"},   # Funkadelic - Maggot Brain
            {"rank": 215, "musicbrainz_id": "19a185f4-f683-3d00-9571-7378ea276068"},   # Nilsson - Nilsson Schmilsson
            {"rank": 216, "musicbrainz_id": "edb44be8-a63e-3ebf-bff0-959fd37c3bc5"},   # Isaac Hayes - Shaft: Music From the Soundtrack
            {"rank": 217, "musicbrainz_id": "99878359-e736-3cdc-a225-548ad17d1c76"},   # Janis Joplin - Pearl
            {"rank": 218, "musicbrainz_id": "204cc47e-2e1a-3877-8e1e-d14bfffd19aa"},   # Jethro Tull - Aqualung
            {"rank": 219, "musicbrainz_id": "20fab8a7-0b29-4cc6-a7bf-850d723b2b5c"},   # John Lennon - Imagine
            {"rank": 220, "musicbrainz_id": "42d725fb-a8b7-388c-8866-3b02789af326"},   # Joni Mitchell - Blue
            {"rank": 221, "musicbrainz_id": "2e61da88-39e9-3473-81d2-c964cb394952"},   # Led Zeppelin - [Led Zeppelin IV]
            {"rank": 222, "musicbrainz_id": "964ccc52-2873-3bce-a806-73d71532c539"},   # Leonard Cohen - Songs of Love and Hate
            {"rank": 223, "musicbrainz_id": "da336311-12f8-4ca3-8268-806dc536936f"},   # Johnny “Hammond” Smith - What's Goin' On
            {"rank": 224, "musicbrainz_id": "d4e7be0c-6db3-372e-aee6-e048dbb9ac51"},   # Rod Stewart - Every Picture Tells a Story
            {"rank": 225, "musicbrainz_id": "431ae137-315a-3faa-8005-c959fc0d57e9"},   # Serge Gainsbourg - Histoire de Melody Nelson
            {"rank": 226, "musicbrainz_id": "d8b8448a-2634-3e92-ac86-cf55e018f825"},   # Sly & the Family Stone - There’s a Riot Goin’ On
            {"rank": 227, "musicbrainz_id": "e53310bf-8ccc-3d7f-a0b7-5ca4dbababcb"},   # T. Rex - Electric Warrior
            {"rank": 228, "musicbrainz_id": "d757b87e-4a3b-38ec-9246-548baeff5ceb"},   # The Allman Brothers Band - At Fillmore East
            {"rank": 229, "musicbrainz_id": "a42b6a80-b542-344c-921d-15a07fdb580e"},   # The Beach Boys - Surf's Up
            {"rank": 230, "musicbrainz_id": "fe30770e-d417-3629-97ee-77d229c2d32f"},   # Bee Gees - Trafalgar
            {"rank": 231, "musicbrainz_id": "7be633bd-d1f6-3d89-8939-803ae0ed0de8"},   # The Doors - L.A. Woman
            # {"rank": 232, "musicbrainz_id": None},   # NO MATCH: Faces - A Nod's as Good as a Wink... to a Blind Horse (1971)
            {"rank": 233, "musicbrainz_id": "9ec6b178-14c4-35e9-b9bd-896aff95c17e"},   # Flamin’ Groovies - Teenage Head
            {"rank": 234, "musicbrainz_id": "4a4213d0-f224-3d51-bcca-476f61162681"},   # The Rolling Stones - Sticky Fingers
            {"rank": 235, "musicbrainz_id": "9584e28b-66a7-3846-8d52-b3008a283539"},   # The Who - Who’s Next
            {"rank": 236, "musicbrainz_id": "0fa03925-736c-3537-b0c6-201091543177"},   # Yes - The Yes Album
            {"rank": 237, "musicbrainz_id": "b1176e7b-fa2e-3b28-959a-d8f55b5b6ccf"},   # Yes - Fragile
            {"rank": 238, "musicbrainz_id": "eed9ffe2-5731-3b9a-9906-01728a083d1d"},   # Al Green - Let’s Stay Together
            {"rank": 239, "musicbrainz_id": "9e038b79-8be1-3cf1-bdd6-62f4842ab665"},   # Alice Cooper - School’s Out
            {"rank": 240, "musicbrainz_id": "18ec10a7-864f-3f1b-8d68-5cb622165b20"},   # Big Star - #1 Record
            {"rank": 241, "musicbrainz_id": "4e9db6ce-9019-33b5-8ab4-b203cba390a3"},   # Banda Calypso - Volume 4
            {"rank": 242, "musicbrainz_id": "2b649670-7d2d-3287-9b40-5b88fb4e1f35"},   # Burning Spear - Marcus Garvey
            {"rank": 243, "musicbrainz_id": "3f68cf91-b4f0-39ef-8318-93dc064a53ba"},   # Curtis Mayfield - Superfly
            {"rank": 244, "musicbrainz_id": "6f78435e-5d1b-3cc8-83ce-10f0a2f11ee5"},   # David Ackles - American Gothic
            {"rank": 245, "musicbrainz_id": "6c9ae3dd-32ad-472c-96be-69d0a3536261"},   # David Bowie - The Rise and Fall of Ziggy Stardust and the Spiders From Mars
            {"rank": 246, "musicbrainz_id": "743b0b2e-a23a-3182-950e-232f8cb0dfb7"},   # David Bowie - Hunky Dory
            {"rank": 247, "musicbrainz_id": "3a3a3181-3b32-404b-8356-5d8eec2a40cd"},   # Deep Purple - Machine Head
            {"rank": 248, "musicbrainz_id": "3fce812e-d2a3-4352-8a4b-6b19c1282337"},   # Gene Clark - Here Tonight: The White Light Demos
            {"rank": 249, "musicbrainz_id": "59f4a254-b66c-438d-adaa-d72feafaa6d6"},   # Hugh Masekela - Home Is Where the Music Is / The African Connection
            {"rank": 250, "musicbrainz_id": "a13154a4-14a1-3344-ae14-3bea728ebe58"},   # John Prine - John Prine
            {"rank": 251, "musicbrainz_id": "6c8345df-f822-33af-b64a-eff2e46941b9"},   # Lou Reed - Transformer
            {"rank": 252, "musicbrainz_id": "be161b2c-ec5c-3102-8e0b-374a29cc5113"},   # Milton Nascimento - Clube da Esquina 2
            {"rank": 253, "musicbrainz_id": "b25419cf-71bf-3a54-8cd4-2161c61056a0"},   # Neil Young - Harvest
            {"rank": 254, "musicbrainz_id": "740ec10a-e887-38a6-a04d-fe2069c9e2a7"},   # Nick Drake - Pink Moon
            {"rank": 255, "musicbrainz_id": "0ec57ce0-987b-3ea4-b3de-ba1db6488b4b"},   # The Nitty Gritty Dirt Band - Will the Circle Be Unbroken
            {"rank": 256, "musicbrainz_id": "a1cc3fbd-609b-323c-95e2-435dfceb51e9"},   # Paul Simon - Paul Simon
            {"rank": 257, "musicbrainz_id": "d1c0b3db-6b93-3b9d-9479-0d60486120cb"},   # Randy Newman - Sail Away
            {"rank": 258, "musicbrainz_id": "3ff6284f-88b0-3285-895a-61c733e6d4ca"},   # Roxy Music - Roxy Music
            {"rank": 259, "musicbrainz_id": "8455be77-292b-3699-81c4-c11dd6b9049f"},   # Slade - Slayed?
            {"rank": 260, "musicbrainz_id": "9d73a864-2976-3286-b6c1-8aabc7407737"},   # Steely Dan - Can’t Buy a Thrill
            {"rank": 261, "musicbrainz_id": "58c6d809-bfa7-3b25-acf3-a99d53402b08"},   # Stevie Wonder - Talking Book
            {"rank": 262, "musicbrainz_id": "bf12c581-95c6-3cde-8ac2-713e803fc9e9"},   # T. Rex - The Slider
            {"rank": 263, "musicbrainz_id": "7eceb3e2-8ff4-3574-b66f-bc660139f36e"},   # Eagles - The Eagles / Desperado
            {"rank": 264, "musicbrainz_id": "2beb05b7-e789-427c-98ce-99b9a62f9499"},   # The Rolling Stones - Sticky Fingers / Exile on Main Street
            {"rank": 265, "musicbrainz_id": "1b715418-65d4-35d1-9fc1-b3b3a3087bcf"},   # The Temptations - All Directions
            {"rank": 266, "musicbrainz_id": "edbaf38a-ba3c-3d21-981c-879fe4ac6c76"},   # Todd Rundgren - Something/Anything?
            {"rank": 267, "musicbrainz_id": "ae18844a-d94e-380f-a558-78252d57dc9a"},   # War - The World Is a Ghetto
            {"rank": 268, "musicbrainz_id": "5a59b948-1961-32ff-80d9-e970c7d4ebe9"},   # Yes - Close to the Edge
            {"rank": 269, "musicbrainz_id": "0bfa0a07-16c5-3c8e-ab53-927d1e021791"},   # Alice Cooper - Billion Dollar Babies
            {"rank": 270, "musicbrainz_id": "03170256-02c9-44c7-abad-e0ea3dd47c22"},   # Bob Marley & The Wailers - Catch a Fire
            {"rank": 271, "musicbrainz_id": "aa41b178-9f16-3dc4-84b6-e9ad8b5be4b8"},   # Can - Future Days
            {"rank": 272, "musicbrainz_id": "50f8710f-3ae6-319b-85a7-afe783f13449"},   # David Bowie - Aladdin Sane
            {"rank": 273, "musicbrainz_id": "afab893b-4284-37c3-bf74-0139773c8c6d"},   # Deep Purple - Made in Japan
            {"rank": 274, "musicbrainz_id": "80df0f1b-4ce7-348a-aa1b-0d31ebff111a"},   # Elton John - Goodbye Yellow Brick Road
            {"rank": 275, "musicbrainz_id": "75ec1e72-cc7d-37b6-bebd-a1131b578e7b"},   # Faust - Faust IV
            {"rank": 276, "musicbrainz_id": "1fadec3d-7451-32e8-9194-ad7e5312cb9b"},   # Genesis - Selling England by the Pound
            {"rank": 277, "musicbrainz_id": "eeb6a226-8323-327e-9116-1dc51e2fcb23"},   # Gram Parsons - Grievous Angel
            {"rank": 278, "musicbrainz_id": "42fb29f2-728b-3dbb-85cf-70468d7b8a24"},   # Hawkwind - Space Ritual
            {"rank": 279, "musicbrainz_id": "0f2ba08b-77e2-3322-9f14-0eab3e3efd07"},   # Iggy Pop & The Stooges - Raw Power
            {"rank": 280, "musicbrainz_id": "56da088f-9d69-3af4-aeac-55649e19bffe"},   # John Cale - Paris 1919
            {"rank": 281, "musicbrainz_id": "e1670336-f7b9-31b6-bd3c-77d8e8169cd9"},   # John Martyn - Solid Air
            {"rank": 282, "musicbrainz_id": "6d655093-4a0b-32ca-8d0e-b497d6ac781d"},   # King Crimson - Larks’ Tongues in Aspic
            {"rank": 283, "musicbrainz_id": "c6190069-644f-3b41-92aa-1e771e451036"},   # Lou Reed - Berlin
            {"rank": 284, "musicbrainz_id": "33446893-8c9f-30b6-aa73-d719df371430"},   # Lynyrd Skynyrd - (pronounced ’lĕh-’nérd ’skin-’nérd)
            {"rank": 285, "musicbrainz_id": "5ee3fdb7-4ae4-3cd0-9a81-e42a60db76dd"},   # Manassas - Manassas
            {"rank": 286, "musicbrainz_id": "e834440b-ffe0-41bf-83de-336b53dc1470"},   # Marvin Gaye - Let’s Get It On
            {"rank": 287, "musicbrainz_id": "beeb6b52-d7f1-3cf4-9da4-eec7e1d59c02"},   # Incredible Bongo Band - Bongo Rock
            {"rank": 288, "musicbrainz_id": "1082b88c-a2c4-36a3-834f-126405c20dc3"},   # Mike Oldfield - Tubular Bells
            {"rank": 289, "musicbrainz_id": "4f213af5-f4f9-3129-ad7e-d34f1fd8abd1"},   # Mott the Hoople - Mott
            {"rank": 290, "musicbrainz_id": "2b678170-1c4e-3e61-b18c-f889fc1537b3"},   # Paul McCartney & Wings - Band on the Run
            {"rank": 291, "musicbrainz_id": "5dbefdbd-8bdc-4611-91e5-f0c0a2695612"},   # Pink Floyd - Dark Side of the Moon [RESTORED]
            {"rank": 292, "musicbrainz_id": "72fd9993-17b8-3402-9f8d-c39cb3d2c27e"},   # Roxy Music - For Your Pleasure
            {"rank": 293, "musicbrainz_id": "33726877-dd41-301b-9f1e-498ebbadc7d8"},   # Steely Dan - Countdown to Ecstasy
            {"rank": 294, "musicbrainz_id": "e626b377-74c5-3b97-8f16-8cef5e1c04ea"},   # Stevie Wonder - Innervisions
            {"rank": 295, "musicbrainz_id": "dba6cc6f-2406-4655-bd1d-dda71b914797"},   # NPVR - 33 33
            {"rank": 296, "musicbrainz_id": "4cdd4c59-e38f-382b-b01c-e69829faa69c"},   # New York Dolls - New York Dolls
            {"rank": 297, "musicbrainz_id": "9821e041-4973-381a-a627-a02fd018f7e9"},   # The Sensational Alex Harvey Band - Next…
            {"rank": 298, "musicbrainz_id": "d6263c37-09b4-35f3-80db-3ffff1cf4252"},   # Todd Rundgren - A Wizard, a True Star
            {"rank": 299, "musicbrainz_id": "d86fc913-939f-4d03-a82c-218b85cae3c5"},   # Waylon Jennings - Honky Tonk Heroes
            {"rank": 300, "musicbrainz_id": "3aee7fe4-813e-3f04-8280-8d25f066f143"},   # ZZ Top - Tres hombres
            {"rank": 301, "musicbrainz_id": "909e7c30-838a-32ac-bf8b-c65a7e101fec"},   # 10cc - Sheet Music
            {"rank": 302, "musicbrainz_id": "1f67788b-223d-3f28-b972-7f07c9418ed0"},   # Bad Company - Bad Company
            {"rank": 303, "musicbrainz_id": "9c1b8072-eb1d-33d2-af8c-984d46e40902"},   # Bob Dylan - Blood on the Tracks
            {"rank": 304, "musicbrainz_id": "90d9be4c-30be-3e28-949a-66ee22c3a63a"},   # Brian Eno - Here Come the Warm Jets
            {"rank": 305, "musicbrainz_id": "9aa1dc17-d89c-3969-8453-defec8fe0361"},   # Dennis Wilson - Pacific Ocean Blue
            {"rank": 306, "musicbrainz_id": "ced848a4-b94b-3f34-b08b-6dc8bf8aed8f"},   # Eric Clapton - 461 Ocean Boulevard
            {"rank": 307, "musicbrainz_id": "1a8984d7-503a-3a06-b02c-dad5e01b0d10"},   # Gene Clark - No Other
            {"rank": 308, "musicbrainz_id": "f2e5d462-6ec1-3cf8-8ea8-06eab8fe51f5"},   # Genesis - The Lamb Lies Down on Broadway
            {"rank": 309, "musicbrainz_id": "e709a485-297f-37a4-a2ae-c405956dd5c1"},   # George Jones - The Grand Tour
            {"rank": 310, "musicbrainz_id": "ba564694-316b-43bd-8a84-31fa97641465"},   # Rene Froger - Winter in America
            {"rank": 311, "musicbrainz_id": "178428cf-bb92-4c49-9cd3-2d8406aa8460"},   # Herbie Hancock - Headhunters (Live)
            {"rank": 312, "musicbrainz_id": "3bd19e28-698e-3b7e-a8ec-f872bf001651"},   # Joni Mitchell - Court and Spark
            {"rank": 313, "musicbrainz_id": "f73729e8-4501-3088-aa20-44945296036e"},   # Kraftwerk - Autobahn
            {"rank": 314, "musicbrainz_id": "f4174531-b783-3786-b75f-4fe61a8f6333"},   # Neil Young - On the Beach
            {"rank": 315, "musicbrainz_id": "002ed683-3327-3df0-88c8-318746089925"},   # Queen - Sheer Heart Attack
            {"rank": 316, "musicbrainz_id": "93d91bd6-1b55-3751-bca7-8b9d33beb7ef"},   # Queen - Queen II
            {"rank": 317, "musicbrainz_id": "bb1a6e55-7d0a-3d48-b447-49b86cdcca7a"},   # Randy Newman - Good Old Boys
            {"rank": 318, "musicbrainz_id": "b35625b1-200d-3692-b02a-08bd4f693ef8"},   # Richard & Linda Thompson - I Want to See the Bright Lights Tonight
            {"rank": 319, "musicbrainz_id": "94a36264-ab82-34b7-ae9d-2320803c4516"},   # Robert Wyatt - Rock Bottom
            {"rank": 320, "musicbrainz_id": "b2d10ce6-bf86-3091-8c71-3e8330f4b748"},   # Roxy Music - Country Life
            {"rank": 321, "musicbrainz_id": "0539b843-2228-36f5-965d-f370d05f66c3"},   # Sparks - Kimono My House
            {"rank": 322, "musicbrainz_id": "5c938587-b4cd-3d6c-9f9e-a87492a2c9de"},   # Steely Dan - Pretzel Logic
            {"rank": 323, "musicbrainz_id": "95e58ee5-5421-38b0-a937-803b004c7ae8"},   # Stevie Wonder - Fulfillingness’ First Finale
            {"rank": 324, "musicbrainz_id": "c3749af5-0d0c-3ed1-b1c0-8b4a8f6c3436"},   # Supertramp - Crime of the Century
            {"rank": 325, "musicbrainz_id": "866c88fa-a18b-3739-9814-2ad215e5e11a"},   # Tangerine Dream - Phaedra
            {"rank": 326, "musicbrainz_id": "37ed1703-f12d-399d-9c36-58c72479fa58"},   # Van Morrison - It’s Too Late to Stop Now
            {"rank": 327, "musicbrainz_id": "d03bb6b1-d7b4-38ea-974e-847cbb31dca4"},   # Aerosmith - Toys in the Attic
            {"rank": 328, "musicbrainz_id": "e776533c-4132-3b63-bfaa-94fe901951b5"},   # Bob Marley & The Wailers - Natty Dread
            {"rank": 329, "musicbrainz_id": "7d5a684e-73a3-325c-a59c-34c9a941d8d6"},   # Eno - Another Green World
            {"rank": 330, "musicbrainz_id": "39b22944-7503-3937-8bba-09b17281cc6a"},   # Bruce Springsteen - Born to Run
            {"rank": 331, "musicbrainz_id": "9b93bf1c-a61d-341e-8900-b305f3812c2c"},   # Curtis Mayfield - There’s No Place Like America Today
            {"rank": 332, "musicbrainz_id": "8c2a0eae-1359-3577-9127-e3d862acc2a2"},   # David Bowie - Young Americans
            {"rank": 333, "musicbrainz_id": "47256750-eca8-3d6c-91c4-33866caf4ea9"},   # Dion - Born to Be With You
            {"rank": 334, "musicbrainz_id": "e9845207-8ae3-36db-b0e1-2efcdb46687d"},   # Earth, Wind & Fire - That’s the Way of the World
            {"rank": 335, "musicbrainz_id": "f735c43b-aa59-3855-8f4b-fa2cd6af7bbd"},   # Emmylou Harris - Pieces of the Sky
            {"rank": 336, "musicbrainz_id": "169a1a7e-f91e-3b10-a136-d94eba6eee2e"},   # Joni Mitchell - The Hissing of Summer Lawns
            {"rank": 337, "musicbrainz_id": "516d4629-7bf3-3ac3-907a-ed9a022db840"},   # Keith Jarrett - The Köln Concert
            {"rank": 338, "musicbrainz_id": "116c9490-6af4-3827-8261-2d5b1f508fe7"},   # Led Zeppelin - Physical Graffiti
            {"rank": 339, "musicbrainz_id": "e0207e33-af06-3862-baba-f42ca722de0d"},   # Neil Young - Tonight’s the Night
            {"rank": 340, "musicbrainz_id": "34ec11b1-07d4-3a25-a5bf-d43097a91f35"},   # Neu! - Neu! ’75
            {"rank": 341, "musicbrainz_id": "ff8f533c-3cb3-3877-9209-11f433edaad2"},   # Patti Smith - Horses
            {"rank": 342, "musicbrainz_id": "cbf9819e-4a0b-35f1-9b1c-ab34764cf10c"},   # Peter Frampton - Frampton Comes Alive!
            {"rank": 343, "musicbrainz_id": "aec8c2eb-0639-436f-99db-9974781f241c"},   # Pink Floyd - Wish You Were Here
            {"rank": 344, "musicbrainz_id": "6b47c9a0-b9e1-3df9-a5e8-50a6ce0dbdbd"},   # Queen - A Night at the Opera
            # {"rank": 345, "musicbrainz_id": None},   # NO MATCH: R.D. Burman / Bappi Lahiri - Shalimar / College Girl (1975)
            {"rank": 346, "musicbrainz_id": "2bb3b259-5ea7-3773-96be-20d9a592358a"},   # Shuggie Otis - Inspiration Information
            {"rank": 347, "musicbrainz_id": "0fbf007d-981a-3455-85ec-e53a67cbfa4f"},   # The Dictators - Go Girl Crazy
            {"rank": 348, "musicbrainz_id": "864cb6a1-ede7-378d-9f1e-7d4fb3ceed71"},   # Tim Buckley - Greetings From L.A.
            {"rank": 349, "musicbrainz_id": "ae446997-5355-3b5d-9dce-8a48ee1044ac"},   # Tom Waits - Nighthawks at the Diner
            {"rank": 350, "musicbrainz_id": "b51ba291-2490-3132-a85d-2094de795b63"},   # Willie Nelson - Red Headed Stranger
            {"rank": 351, "musicbrainz_id": "e464e167-83ab-3b59-88bd-262cf552056e"},   # ABBA - Arrival
            {"rank": 352, "musicbrainz_id": "775d9a2d-effc-35c8-b80a-f9a4e4206d27"},   # Aerosmith - Rocks
            {"rank": 353, "musicbrainz_id": "f0371fc4-3e22-3d8d-8ce3-4af873ea6f1c"},   # Boston - Boston
            {"rank": 354, "musicbrainz_id": "686cdbd1-b400-32d8-8cb8-9317a2e41a58"},   # David Bowie - Station to Station
            {"rank": 355, "musicbrainz_id": "0ac6d075-35ed-3ec4-8751-06533b8511ee"},   # Joan Armatrading - Joan Armatrading
            {"rank": 356, "musicbrainz_id": "039f2ae4-36dd-3608-9103-67ce7f6c9288"},   # Joni Mitchell - Hejira
            {"rank": 357, "musicbrainz_id": "a5e2f270-c00e-3309-84d1-2c4285565ee3"},   # Jorge Ben - África Brasil
            {"rank": 358, "musicbrainz_id": "541eb339-d0c6-3740-b665-8ad6c09da331"},   # KISS - Destroyer
            {"rank": 359, "musicbrainz_id": "cb69bfc6-a15c-34cd-b1af-76b6481bf09a"},   # Parliament - Mothership Connection
            {"rank": 360, "musicbrainz_id": "3f4929bc-c88d-3f41-910b-5c1c308da8f2"},   # Peter Tosh - Legalize It
            {"rank": 361, "musicbrainz_id": "9243ac59-9390-37e1-abee-fcf31fb8035f"},   # Rush - 2112
            {"rank": 362, "musicbrainz_id": "ea88b09b-fd34-33cf-a3e5-25a3a2fb4c6f"},   # Stevie Wonder - Songs in the Key of Life
            {"rank": 363, "musicbrainz_id": "91bf707c-6c33-4efd-83ca-e4c88f14bcaa"},   # Eagles - Hotel California
            {"rank": 364, "musicbrainz_id": "7de1e321-4a53-3feb-b83e-f1dab88bf952"},   # Ramones - Ramones
            {"rank": 365, "musicbrainz_id": "735bcee6-6be6-3957-af15-d21ba2bd355b"},   # Billy Joel - The Stranger
            {"rank": 366, "musicbrainz_id": "87164686-938c-30d5-accc-c50957735686"},   # Bob Marley & The Wailers - Exodus
            {"rank": 367, "musicbrainz_id": "6f9e2641-f79b-32f2-a752-f7212e9040e4"},   # Brian Eno - Before and After Science
            {"rank": 368, "musicbrainz_id": "db46b19c-0e97-30de-ba53-7e823104d14a"},   # Chic - C’est Chic
            {"rank": 369, "musicbrainz_id": "f6a51281-56c4-3538-b915-65a9d4eb29b5"},   # David Bowie - Low
            {"rank": 370, "musicbrainz_id": "1f5ef8d3-10ca-30eb-b41e-85b16987d412"},   # David Bowie - “Heroes”
            {"rank": 371, "musicbrainz_id": "a720436f-9c8e-439a-a147-18e83441edab"},   # Electric Light Orchestra - Out of the Blue
            {"rank": 372, "musicbrainz_id": "c7a4740f-2729-3895-8498-08c521886a95"},   # Elvis Costello - My Aim Is True
            {"rank": 373, "musicbrainz_id": "d3de5856-816a-4759-bf9c-d5ff0e5cd740"},   # Fela Kuti - Na Poi / Zombie
            {"rank": 374, "musicbrainz_id": "416bb5e5-c7d1-3977-8fd7-7c9daf6c2be6"},   # Fleetwood Mac - Rumours
            {"rank": 375, "musicbrainz_id": "62c71c2a-ecd1-37be-9584-31cd4c746caa"},   # Ian Dury - New Boots and Panties!!
            {"rank": 376, "musicbrainz_id": "15dc9ccf-e33b-3f4d-8c81-8346388d0b29"},   # Iggy Pop - Lust for Life
            {"rank": 377, "musicbrainz_id": "09c88c6d-090e-378d-b104-7966eb5d33d2"},   # Iggy Pop - The Idiot
            {"rank": 378, "musicbrainz_id": "3055cd07-9b9d-34ed-b227-942ba6977174"},   # Jean Michel Jarre - Oxygène
            {"rank": 379, "musicbrainz_id": "a30af693-6896-3620-a603-2be0d0945584"},   # John Martyn - One World
            {"rank": 380, "musicbrainz_id": "91e1f88a-f081-3639-9972-0d46b3d3b616"},   # The Modern Lovers - The Modern Lovers
            # {"rank": 381, "musicbrainz_id": None},   # NO MATCH: Kraftwerk - Trans-Europe Express (1977)
            {"rank": 382, "musicbrainz_id": "565f5d6b-f487-39ef-a29e-23638b523c6f"},   # Pere Ubu - The Modern Dance
            # {"rank": 383, "musicbrainz_id": None},   # NO MATCH: Peter Gabriel - Peter Gabriel (Car) (1977)
            {"rank": 384, "musicbrainz_id": "8588c5a5-b491-37a4-8d51-2227346a072e"},   # Steely Dan - Aja
            {"rank": 385, "musicbrainz_id": "702d4a53-9f00-3f57-a723-e5e267518454"},   # Suicide - Suicide
            {"rank": 386, "musicbrainz_id": "d99084ee-de04-3ba1-8203-5f1a7e5355ee"},   # Talking Heads - Talking Heads: 77
            {"rank": 387, "musicbrainz_id": "ca91cb5a-7ecc-3c46-84a0-0d4951889374"},   # The Clash - The Clash
            # {"rank": 388, "musicbrainz_id": None},   # NO MATCH: Penguin Cafe Orchestra - Music From the Penguin Cafe Orchestra (1977)
            {"rank": 389, "musicbrainz_id": "e959a4b3-6306-3c45-9df6-e7241dae9ea3"},   # Sex Pistols - Never Mind the Bollocks Here’s the Sex Pistols
            {"rank": 390, "musicbrainz_id": "69cc7d7d-4405-3f65-b4e7-e35f216f6191"},   # The Stranglers - Rattus Norvegicus
            {"rank": 391, "musicbrainz_id": "59cb1d59-e0c8-37f0-a2af-9bc8df64f6cd"},   # Tom Petty and the Heartbreakers - Tom Petty and the Heartbreakers
            {"rank": 392, "musicbrainz_id": "f1753c0a-50be-3591-8cbb-6848142e055f"},   # Weather Report - Heavy Weather
            {"rank": 393, "musicbrainz_id": "9facb8b5-4b02-3f28-9f4a-61cb9b8fd7aa"},   # Wire - Pink Flag
            # {"rank": 394, "musicbrainz_id": None},   # NO MATCH: Big Star - Third/Sister Lovers (1978)
            {"rank": 395, "musicbrainz_id": "0c1a4d70-5926-3ae8-aa25-466fe65639fe"},   # Blondie - Parallel Lines
            {"rank": 396, "musicbrainz_id": "5fdd6ba8-83c1-3a87-b378-d5f61dec5ddd"},   # Brian Eno - Ambient 1: Music for Airports
            {"rank": 397, "musicbrainz_id": "b613123b-a234-3f48-9c45-e05bf4e6b9e7"},   # Bruce Springsteen - Darkness on the Edge of Town
            {"rank": 398, "musicbrainz_id": "7a82f652-2300-3ce6-a6ae-dd0efa8e4b15"},   # Buzzcocks - Another Music in a Different Kitchen
            {"rank": 399, "musicbrainz_id": "2c3682e2-cc7b-32e0-ab48-d4dbbd458479"},   # Cheap Trick - Cheap Trick at Budokan
            {"rank": 400, "musicbrainz_id": "60a754f9-50e1-346a-97db-925a1e2ad7e0"},   # DEVO - Q: Are We Not Men? A: We Are Devo!
            {"rank": 401, "musicbrainz_id": "4914e4cf-4ad4-466d-a016-3d57bcb682ed"},   # Dire Straits - Dire Straits
            {"rank": 402, "musicbrainz_id": "c641d104-0c97-450b-8f6e-b5661afde07c"},   # Nara Leão - Vento de Maio
            {"rank": 403, "musicbrainz_id": "5e8117f4-a87f-3732-be5f-313c7e5b308d"},   # Elvis Costello - This Year’s Model
            {"rank": 404, "musicbrainz_id": "9d084107-b712-3599-ab62-ac76fe3756b5"},   # Funkadelic - One Nation Under a Groove
            {"rank": 405, "musicbrainz_id": "e94db330-743f-3cb2-81dd-eae73ebe7a47"},   # Joe Ely - Honky Tonk Masquerade
            {"rank": 406, "musicbrainz_id": "396d81a6-bec0-30ac-9bfc-940e31893daa"},   # Kraftwerk - The Man-Machine Recreated
            {"rank": 407, "musicbrainz_id": "5ef7ef5c-f9aa-3800-9f55-ec58130846ba"},   # Magazine - Real Life
            {"rank": 408, "musicbrainz_id": "225a6648-d4d2-3b89-986b-6e515e7a94f0"},   # Marvin Gaye - Here, My Dear
            {"rank": 409, "musicbrainz_id": "47616c4c-5d4b-30f6-83bc-60e1c696b099"},   # Meat Loaf - Bat Out of Hell
            {"rank": 410, "musicbrainz_id": "a77c72ce-c6d9-3ebd-a4c1-ced5d4ec0b4b"},   # Muddy Waters - Hard Again
            {"rank": 411, "musicbrainz_id": "e6cf6f53-43a8-3d00-9913-991cd8ae8f53"},   # Pere Ubu - Dub Housing
            {"rank": 412, "musicbrainz_id": "1a3d0d0c-38bd-3662-9e27-e507fc949aa6"},   # Public Image Ltd. - First Issue
            {"rank": 413, "musicbrainz_id": "0efd12a2-2d31-3fa8-a76c-5f8af6613fca"},   # Willie Colón - Siembra
            {"rank": 414, "musicbrainz_id": "67f24412-60c9-36f3-a1dc-e48e56098802"},   # Siouxsie and the Banshees - The Scream
            {"rank": 415, "musicbrainz_id": "2cecb2c0-cac3-3c55-8083-577308746230"},   # Talking Heads - More Songs About Buildings and Food
            {"rank": 416, "musicbrainz_id": "2b9f99d8-becf-3fc3-86a6-2bdd4cef93fe"},   # Television - Marquee Moon
            {"rank": 417, "musicbrainz_id": "7f32f3a7-2b4d-357d-a722-6943880ace45"},   # The Adverts - Crossing the Red Sea with The Adverts
            {"rank": 418, "musicbrainz_id": "36172f3d-9b55-37f1-9fd4-0cbd2f3af0ce"},   # The Cars - The Cars
            {"rank": 419, "musicbrainz_id": "68a97464-1449-331a-b32c-89e0b4658aa9"},   # The Jam - All Mod Cons
            {"rank": 420, "musicbrainz_id": "393c7679-ee77-304f-a293-7d5167426333"},   # The Only Ones - The Only Ones
            # {"rank": 421, "musicbrainz_id": None},   # NO MATCH: The Residents - Duck Stab/Buster & Glen (1978)
            {"rank": 422, "musicbrainz_id": "c0069416-d369-3453-b3b7-00774b9e698b"},   # The Saints - Eternally Yours
            {"rank": 423, "musicbrainz_id": "e9ae496e-c750-3433-a35c-adfc50f83858"},   # Thin Lizzy - Live and Dangerous
            {"rank": 424, "musicbrainz_id": "a1b3bae2-0081-3266-a349-1297f50a3c78"},   # Throbbing Gristle - D.o.A. The Third and Final Report
            # {"rank": 425, "musicbrainz_id": None},   # NO MATCH: Van Halen - Van Halen 1 (1978)
            {"rank": 426, "musicbrainz_id": "196bb5cd-d3bf-3da8-9a6c-25c6212bda05"},   # Willie Nelson - Stardust
            # {"rank": 427, "musicbrainz_id": None},   # NO MATCH: X-Ray Spex - Germ-Free Adolescents (1978)
            {"rank": 428, "musicbrainz_id": "f85647ec-a69b-3b0a-ad04-bb6076c4dcf1"},   # AC/DC - Highway to Hell
            {"rank": 429, "musicbrainz_id": "baa74317-3f23-3f0b-a996-c68f52c61f13"},   # Chic - Risqué
            {"rank": 430, "musicbrainz_id": "2b0dc0fa-b299-4fd5-81e9-2397fd41b8d1"},   # Elvis Costello - Selections From: Armed Forces – Imperial Bedroom – Mighty Like a Rose
            {"rank": 431, "musicbrainz_id": "22deeac8-6009-31ad-a069-26e85d246412"},   # Fleetwood Mac - Tusk
            {"rank": 432, "musicbrainz_id": "d0493944-992b-3534-9174-8320c1879837"},   # Gang of Four - Entertainment!
            {"rank": 433, "musicbrainz_id": "2ba66802-18a7-3bf4-958c-db871a6e7f34"},   # Gary Numan - The Pleasure Principle
            {"rank": 434, "musicbrainz_id": "1f66bd0f-4bbe-3eeb-8271-3a43972473ff"},   # Germs - (GI)
            {"rank": 435, "musicbrainz_id": "b8daa1d3-3db4-3f71-93c2-762a58964264"},   # Holger Czukay - Movies
            {"rank": 436, "musicbrainz_id": "c1a568c7-055c-374a-9d92-9ea077f2bf1f"},   # Japan - Quiet Life
            {"rank": 437, "musicbrainz_id": "42352def-1aab-3000-b548-895ebd869cb6"},   # Joy Division - Unknown Pleasures
            {"rank": 438, "musicbrainz_id": "96e40648-a0e2-320b-9592-fff4a49d9395"},   # Marianne Faithfull - Broken English
            {"rank": 439, "musicbrainz_id": "ee749c63-5699-38e0-b565-7e84414648d9"},   # Michael Jackson - Off the Wall
            {"rank": 440, "musicbrainz_id": "a710c7c7-46e6-36ca-9c3c-87c8e79f8daf"},   # Neil Young - Rust Never Sleeps
            {"rank": 441, "musicbrainz_id": "f2026101-945b-3d05-9ef4-aa718fc3feef"},   # Pink Floyd - The Wall
            {"rank": 442, "musicbrainz_id": "448c8d23-3118-397f-9b81-a560c799f27a"},   # Pretenders - Pretenders
            {"rank": 443, "musicbrainz_id": "57209d3f-f3ef-34db-82a7-ad633497b784"},   # Public Image Ltd. - Metal Box
            {"rank": 444, "musicbrainz_id": "acb1aa80-3ede-3a65-a862-5b0730c92607"},   # Sister Sledge - We Are Family
            {"rank": 445, "musicbrainz_id": "f378dcb1-841b-3be1-9d96-779036562de1"},   # Talking Heads - Fear of Music
            {"rank": 446, "musicbrainz_id": "ac37276d-7621-4389-82b4-e06f7b3d314c"},   # The B‐52’s - The B‐52’s / Wild Planet
            {"rank": 447, "musicbrainz_id": "8d73e45e-7ca1-3cb4-ae28-6da76196c17c"},   # The Clash - London Calling
            {"rank": 448, "musicbrainz_id": "a45dc179-ed49-3881-a322-6ed211bbd686"},   # The Crusaders - Street Life
            {"rank": 449, "musicbrainz_id": "2e30aefe-004b-3680-8ad4-4b2398d8e0ed"},   # The Damned - Machine Gun Etiquette
            {"rank": 450, "musicbrainz_id": "26046710-088b-3188-996b-d9f654dfe0ef"},   # The Fall - Live at the Witch Trials
            {"rank": 451, "musicbrainz_id": "2b98e6d7-a521-332f-961e-d281ba33ba3d"},   # The Police - Reggatta de Blanc
            {"rank": 452, "musicbrainz_id": "116b94a2-4361-3ec2-af92-270d97dc10f9"},   # The Slits - Cut
            {"rank": 453, "musicbrainz_id": "9c02ca99-df9a-3e48-8b7a-fabb599d19a3"},   # The Specials - Specials
            {"rank": 454, "musicbrainz_id": "d462b990-66d5-3c6b-bc67-4f3d152cdc45"},   # The Undertones - The Undertones
            {"rank": 455, "musicbrainz_id": "d3bc1a64-7561-3787-b680-0003aa50f8f1"},   # AC/DC - Back in Black
            {"rank": 456, "musicbrainz_id": "8698397e-887c-3f78-9d95-6c6499a1daa8"},   # Adam and the Ants - Kings of the Wild Frontier
            {"rank": 457, "musicbrainz_id": "8f5c4731-688f-3612-b5fe-318842359579"},   # Circle Jerks - Group Sex
            {"rank": 458, "musicbrainz_id": "3495fca0-ce60-3342-93f2-23fd525d8069"},   # Dead Kennedys - Fresh Fruit for Rotting Vegetables
            {"rank": 459, "musicbrainz_id": "eba92674-43f2-31f9-9a6c-ba7d3604da95"},   # Dexys Midnight Runners - Searching for the Young Soul Rebels
            {"rank": 460, "musicbrainz_id": "94b22dcb-4761-3655-975a-1a226e00a9c8"},   # Echo and the Bunnymen - Crocodiles
            {"rank": 461, "musicbrainz_id": "e92a6dba-cd7f-4121-b32d-364c29fb9f1b"},   # Iron Maiden - Iron Maiden
            {"rank": 462, "musicbrainz_id": "852f9715-24b3-37d5-b8a5-456f5e19b41e"},   # Joy Division - Closer
            {"rank": 463, "musicbrainz_id": "0c819099-2669-488a-a1a3-33e2bb6aab25"},   # Judas Priest - British Steel
            {"rank": 464, "musicbrainz_id": "282c764a-5925-3bef-8d6d-20613c602768"},   # Killing Joke - Killing Joke
            {"rank": 465, "musicbrainz_id": "5a72e9b3-5075-3671-9750-8f3fa6e0d2f8"},   # Motörhead - Ace of Spades
            # {"rank": 466, "musicbrainz_id": None},   # NO MATCH: Peter Gabriel - Peter Gabriel (Melt) (1980)
            {"rank": 467, "musicbrainz_id": "1e0b3c8b-9e48-30a1-a49d-5f8c433c960b"},   # Steve Winwood - Arc of a Diver
            {"rank": 468, "musicbrainz_id": "f6b1b900-6108-32f0-abbd-2855af9151eb"},   # Talking Heads - Remain in Light
            {"rank": 469, "musicbrainz_id": "8bad0855-1673-393c-a247-1e88d856815d"},   # The Teardrop Explodes - Kilimanjaro
            {"rank": 470, "musicbrainz_id": "4b60e6ef-b29a-3a26-9146-07f35c7e285d"},   # The Cramps - Songs the Lord Taught Us
            {"rank": 471, "musicbrainz_id": "7cd31244-186e-36bb-966f-fd6a90c0832c"},   # The Cure - Seventeen Seconds
            {"rank": 472, "musicbrainz_id": "720d64da-e200-3bea-ae34-9cc0ea83c66e"},   # The Jam - Sound Affects
            {"rank": 473, "musicbrainz_id": "d9046296-1811-3504-8199-4a557cf97872"},   # The Soft Boys - Underwater Moonlight
            {"rank": 474, "musicbrainz_id": "da095ec5-ca70-30ab-bd36-45ef961dced7"},   # The Specials - More Specials
            {"rank": 475, "musicbrainz_id": "3b92033a-4d04-3e5d-9b8e-fb7e0da79a30"},   # The Undertones - Hypnotised
            {"rank": 476, "musicbrainz_id": "6a9906e1-1ab2-37e1-980b-5e4889661089"},   # Tom Waits - Heartattack and Vine
            {"rank": 477, "musicbrainz_id": "73459ae1-a126-3f8b-ac59-a8a41fbda78f"},   # UB40 - Signing Off
            {"rank": 478, "musicbrainz_id": "76bb9f69-b5c1-31be-9bbf-b4b3d98988b0"},   # ABBA - The Visitors
            {"rank": 479, "musicbrainz_id": "b9478bd5-7b9a-326e-8bdf-ad8cf8978f54"},   # Bauhaus - Mask
            {"rank": 480, "musicbrainz_id": "2cf40300-0f67-3136-9b84-57104f1f7a50"},   # Black Flag - Damaged
            {"rank": 481, "musicbrainz_id": "3921b79d-b1f3-3651-9a3b-6795940b168d"},   # Bobby Womack - The Poet
            # {"rank": 482, "musicbrainz_id": None},   # NO MATCH: Brian Eno - David Byrne - My Life In The Bush Of Ghosts (1981)
            {"rank": 483, "musicbrainz_id": "5fc08a84-d9f5-3795-bf98-0abb5a8428bd"},   # Einstürzende Neubauten - Kollaps
            {"rank": 484, "musicbrainz_id": "8b64edc9-1a59-3840-8b12-85a4e19cf48a"},   # Go‐Go’s - Beauty and the Beat
            {"rank": 485, "musicbrainz_id": "1353ea6d-1ec7-3171-9fe0-8a4199d74165"},   # Heaven 17 - Penthouse and Pavement
            {"rank": 486, "musicbrainz_id": "e8e7999e-0b87-3298-947d-2ad22717fc27"},   # The Human League - Dare
            {"rank": 487, "musicbrainz_id": "98a70d58-bbc1-328d-89ca-31850e74d678"},   # Motörhead - No Sleep ’Til Hammersmith
            {"rank": 488, "musicbrainz_id": "dd28f081-4d8c-34aa-afe3-a19b833954b5"},   # The Psychedelic Furs - Talk Talk Talk
            {"rank": 489, "musicbrainz_id": "40e30dc1-55ac-33e1-85d3-1f1508140bfc"},   # Rush - Moving Pictures
            {"rank": 490, "musicbrainz_id": "844bfb05-2b51-35e2-8063-1c8e6746c781"},   # Siouxsie and the Banshees - Juju
            {"rank": 491, "musicbrainz_id": "e5bc1607-7947-3044-8558-6b4eae334c51"},   # Soft Cell - Non‐Stop Erotic Cabaret
            {"rank": 492, "musicbrainz_id": "95b4ac0b-3286-3208-8821-b292ab88dfac"},   # The Gun Club - Fire of Love
            # {"rank": 493, "musicbrainz_id": None},   # NO MATCH: The Tom Tom Club - The Tom Tom Club (1981)
            {"rank": 494, "musicbrainz_id": "8aca1b90-9412-3a00-965c-fd1873f6b986"},   # X - Wild Gift
            {"rank": 495, "musicbrainz_id": "5bc5e6a3-4c24-33c3-9022-4b815d0c48d5"},   # ABC - The Lexicon of Love
            {"rank": 496, "musicbrainz_id": "324aee0c-36ec-35c1-9c93-b67a1d428037"},   # Bruce Springsteen - Nebraska
            {"rank": 497, "musicbrainz_id": "b3865201-9889-3be7-bf42-146bd298cc6f"},   # Kevin Rowland - Too-Rye-Ay
            {"rank": 498, "musicbrainz_id": "a0f2615e-aebd-3300-99e3-626c4ea7bcae"},   # Donald Fagen - The Nightfly
            {"rank": 499, "musicbrainz_id": "2b0dc0fa-b299-4fd5-81e9-2397fd41b8d1"},   # Elvis Costello - Selections From: Armed Forces – Imperial Bedroom – Mighty Like a Rose
            {"rank": 500, "musicbrainz_id": "2348a270-ad78-30e1-b50f-82b2445c15f0"},   # Grandmaster Flash & The Furious Five - The Message
            {"rank": 501, "musicbrainz_id": "a88e179b-7d6e-325d-b683-55158b439973"},   # Haircut One Hundred - Pelican West
            {"rank": 502, "musicbrainz_id": "d65d9d2c-b31d-4cb9-9d41-cd10d6528914"},   # Iron Maiden - The Number of the Beast
            {"rank": 503, "musicbrainz_id": "d28777fc-f135-3394-a033-eafb9ebcffb4"},   # Kate Bush - The Dreaming
            {"rank": 504, "musicbrainz_id": "7b3c2ec0-7390-39eb-a23c-f33d760f274a"},   # Madness - The Rise & Fall
            {"rank": 505, "musicbrainz_id": "f32fab67-77dd-3937-addc-9062e28e4c37"},   # Michael Jackson - Thriller
            {"rank": 506, "musicbrainz_id": "b29ee43a-2073-3b7d-add8-ad893be0ecc9"},   # Orange Juice - Rip It Up
            {"rank": 507, "musicbrainz_id": "561be5b7-a39c-3866-859d-d86f30816ae7"},   # Prince - 1999
            {"rank": 508, "musicbrainz_id": "c7126542-56ab-3d15-8a86-9caf5b3d4de1"},   # Simple Minds - New Gold Dream (81‐82‐83‐84)
            {"rank": 509, "musicbrainz_id": "3bad3ada-83d1-402f-a56a-7023de6d5584"},   # The Associates - Sulk / Fourth Drawer Down
            {"rank": 510, "musicbrainz_id": "d2a8fe20-1bc1-309c-b6f0-77bbf6c3d089"},   # The Birthday Party - Junkyard
            {"rank": 511, "musicbrainz_id": "5d4f8f19-23cf-34cf-b225-8cd0339c37de"},   # The Cure - Pornography
            {"rank": 512, "musicbrainz_id": "84df033e-49e6-30aa-8331-11e4c0e161b6"},   # Venom - Black Metal
            {"rank": 513, "musicbrainz_id": "616a1d80-83d0-3234-bf71-fe3de8109f99"},   # Violent Femmes - Violent Femmes
            {"rank": 514, "musicbrainz_id": "00490137-fa0b-3252-90f7-42b8eea8ae14"},   # Culture Club - Colour by Numbers
            {"rank": 515, "musicbrainz_id": "d77df681-b779-3d6d-b66a-3bfd15985e3e"},   # Def Leppard - Pyromania
            {"rank": 516, "musicbrainz_id": "3c638420-8208-3c01-b723-f061b10e3f3a"},   # Duran Duran - Rio
            {"rank": 517, "musicbrainz_id": "931e971f-eb34-369f-b6a4-f5ef7c6a1c9e"},   # Echo & the Bunnymen - Porcupine
            {"rank": 518, "musicbrainz_id": "b969f851-b5cf-3a3f-9bfe-1280eb271406"},   # Eurythmics - Sweet Dreams (Are Made of This)
            {"rank": 519, "musicbrainz_id": "2f251736-952c-3d8d-b028-322a73ab826d"},   # Hanoi Rocks - Back to Mystery City
            {"rank": 520, "musicbrainz_id": "54242604-882a-391c-b91b-d9af5a63db42"},   # Malcolm McLaren - Duck Rock
            {"rank": 521, "musicbrainz_id": "d33dbcf6-ab44-3c91-872b-9563f724dc0f"},   # Meat Puppets - Meat Puppets II
            {"rank": 522, "musicbrainz_id": "db4d417f-8295-3843-829d-2b8c0b649517"},   # Minor Threat - Out of Step
            {"rank": 523, "musicbrainz_id": "c31b767b-97f0-3cb1-8b09-233a64683997"},   # Orchestral Manœuvres in the Dark - Architecture & Morality
            {"rank": 524, "musicbrainz_id": "1f99b3d9-8739-3a62-afa5-2abb8ff11ee0"},   # Paul Simon - Hearts and Bones
            {"rank": 525, "musicbrainz_id": "de790d3d-a35c-364c-a8fb-adfb73084a45"},   # R.E.M. - Murmur
            {"rank": 526, "musicbrainz_id": "f6df6292-fd40-37c3-bd61-22c53abfe773"},   # The Police - Synchronicity
            {"rank": 527, "musicbrainz_id": "923e256a-7bf0-31e0-bddc-ec76db526c32"},   # The The - Soul Mining
            {"rank": 528, "musicbrainz_id": "c791b365-0400-3926-be67-d1d9c71fc37e"},   # Tom Waits - Swordfishtrombones
            {"rank": 529, "musicbrainz_id": "c6b36664-7e60-3b3e-a24d-d096c67a11e9"},   # U2 - War
            {"rank": 530, "musicbrainz_id": "c58b50f0-d7a4-322c-b281-d86ebe3b8acf"},   # ZZ Top - Eliminator
            {"rank": 531, "musicbrainz_id": "e476a451-bfb1-4756-98e8-08bd671021cf"},   # Bruce Springsteen - Born in the U.S.A.
            {"rank": 532, "musicbrainz_id": "46d415e9-39b7-3978-9e3d-d9d8a32c6751"},   # Cyndi Lauper - She’s So Unusual
            {"rank": 533, "musicbrainz_id": "e0023081-c755-377d-9bbf-fd7551d5d14c"},   # Cocteau Twins - Treasure
            {"rank": 534, "musicbrainz_id": "ecbe6d07-c2e4-37fe-9a99-8484dd7f9a20"},   # Echo & the Bunnymen - Ocean Rain
            {"rank": 535, "musicbrainz_id": "c734406b-3c8a-3214-98cc-dd553f82f813"},   # Frankie Goes to Hollywood - Welcome to the Pleasuredome
            {"rank": 536, "musicbrainz_id": "11dfe59e-068b-3390-8148-c0c08bfb0675"},   # Lloyd Cole and the Commotions - Rattlesnakes
            {"rank": 537, "musicbrainz_id": "0bcb9f3e-e341-3ed5-ac5b-8ed5e17f9a7e"},   # Minutemen - Double Nickels on the Dime
            {"rank": 538, "musicbrainz_id": "b93a7c47-a6d4-33f2-9034-53fdd991f4ba"},   # Prince - Purple Rain
            {"rank": 539, "musicbrainz_id": "0eea6349-52b5-3bf2-abb5-91e68df3902f"},   # Run‐D.M.C. - Ultimate Run DMC
            {"rank": 540, "musicbrainz_id": "af2a0c41-e612-3232-949d-bdca340c407c"},   # Sade - Diamond Life
            {"rank": 541, "musicbrainz_id": "49081a6f-8f76-3159-aba2-8527126d9384"},   # The Style Council - Café Bleu
            {"rank": 542, "musicbrainz_id": "f5bb7c5e-4153-3bcf-9a3b-14d59de5e875"},   # The Blue Nile - A Walk Across the Rooftops
            {"rank": 543, "musicbrainz_id": "2c644807-3b5d-39d4-8c65-dec603bf3f3a"},   # The Replacements - Let It Be
            {"rank": 544, "musicbrainz_id": "cffc5347-3b75-37cc-9120-0ae98b2748dc"},   # Tina Turner - Private Dancer
            {"rank": 545, "musicbrainz_id": "5846f0c9-fec3-3b9e-a77c-fbe9a7bdf0e7"},   # Van Halen - 1984
            {"rank": 546, "musicbrainz_id": "73cd8eec-b315-45c1-beb4-ca71207d3c0a"},   # Youssou N'Dour & Le Super Étoile de Dakar - Immigrés / Bitim Rew
            {"rank": 547, "musicbrainz_id": "53926047-68bc-36a6-95f8-9209f285c95d"},   # Abdullah Ibrahim - Water From an Ancient Well
            {"rank": 548, "musicbrainz_id": "af7347df-ef5a-3c41-826d-d884f8916c17"},   # a‐ha - Hunting High and Low
            {"rank": 549, "musicbrainz_id": "7fe24a11-378e-3c2a-ac4e-dd7e7fb0291e"},   # Dexys Midnight Runners - Don’t Stand Me Down
            {"rank": 550, "musicbrainz_id": "b02f651e-32a1-30ae-bc23-070b59170278"},   # Dire Straits - Brothers in Arms
            {"rank": 551, "musicbrainz_id": "017f2a37-a78f-3578-9611-fa40408e5d90"},   # Kate Bush - Hounds of Love
            {"rank": 552, "musicbrainz_id": "69be20bc-189f-3e40-8486-6fba8459f6a0"},   # New Order - Low‐Life
            {"rank": 553, "musicbrainz_id": "41dcc351-8b81-44f4-a5c5-3e942a21c5de"},   # Prefab Sprout - Steve McQueen
            {"rank": 554, "musicbrainz_id": "e60795c6-96fb-3f5f-84db-9837a9dad179"},   # Scritti Politti - Cupid & Psyche 85
            {"rank": 555, "musicbrainz_id": "7a80d7c7-94f0-302b-90d9-d5ae4cbe3dae"},   # Simply Red - Picture Book
            {"rank": 556, "musicbrainz_id": "ec8b40df-f243-30a6-a076-3691d7f851f2"},   # Suzanne Vega - Suzanne Vega
            {"rank": 557, "musicbrainz_id": "475946e9-4b00-3f7c-9bd7-c11f55740262"},   # Tears for Fears - Songs From the Big Chair
            {"rank": 558, "musicbrainz_id": "e163ed54-842b-3114-9e98-a2d376029abd"},   # The Fall - This Nation’s Saving Grace
            {"rank": 559, "musicbrainz_id": "7534461f-d5ed-3ab0-b5a8-48d7f9b49c70"},   # The Jesus and Mary Chain - Psychocandy
            {"rank": 560, "musicbrainz_id": "e929100a-27b7-3d08-97a5-0fdd97f5a476"},   # Mekons - Fear and Whiskey
            {"rank": 561, "musicbrainz_id": "ba1f6641-9085-36a0-8962-65ad6e48afd1"},   # The Pogues - Rum Sodomy & the Lash
            {"rank": 562, "musicbrainz_id": "0d56a04c-045a-37db-bcc3-6c7099e94f16"},   # The Smiths - Meat Is Murder
            {"rank": 563, "musicbrainz_id": "fb25a883-2270-3ec4-8c62-85c7ed857e6f"},   # Tom Waits - Rain Dogs
            {"rank": 564, "musicbrainz_id": "2dab7547-b12d-3124-8a92-0286986006e8"},   # Afrika Bambaataa & Soulsonic Force - Planet Rock: The Album
            {"rank": 565, "musicbrainz_id": "b544c1b2-9190-34ac-8d03-348c86a77cb2"},   # Anita Baker - Rapture
            {"rank": 566, "musicbrainz_id": "5772996a-d791-3d21-a62e-3efd2a24979c"},   # Bad Brains - I Against I
            {"rank": 567, "musicbrainz_id": "57f5e7c8-2a6e-34a0-b4cd-0e77695bc36f"},   # Beastie Boys - Licensed to Ill
            {"rank": 568, "musicbrainz_id": "94e3e968-4a8d-3d2f-9538-b96c0bfa2a06"},   # Big Black - Atomizer
            {"rank": 569, "musicbrainz_id": "da57eed5-8b1c-36be-a644-bdb4b45660d0"},   # Billy Bragg - Talking With the Taxman About Poetry
            {"rank": 570, "musicbrainz_id": "f07346e6-c889-33b8-83c8-ad987d7b14f6"},   # Bon Jovi - Slippery When Wet
            {"rank": 571, "musicbrainz_id": "cbcc8fdf-180f-36b9-8c0a-e653d78fea2e"},   # Elvis Costello & The Attractions - Blood & Chocolate
            {"rank": 572, "musicbrainz_id": "4eea6bcc-3226-3c0d-a71d-af682a0a1dd8"},   # Megadeth - Peace Sells… but Who’s Buying?
            {"rank": 573, "musicbrainz_id": "3d00fb45-f8ab-3436-a8e1-b4bfc4d66913"},   # Metallica - Master of Puppets
            {"rank": 574, "musicbrainz_id": "8c71b258-5d45-4eb4-b56e-4c3aa0894fe1"},   # Nanci Griffith - The Last of the True Believers
            {"rank": 575, "musicbrainz_id": "19847822-1430-3380-9cf1-bc45545b34ac"},   # Paul Simon - Graceland
            {"rank": 576, "musicbrainz_id": "be3cc3e7-bdb0-3c13-a60b-a985b30eb603"},   # Peter Gabriel - So
            {"rank": 577, "musicbrainz_id": "a209c0a5-e9b2-37ff-a76d-df5bc405a0e8"},   # Run‐D.M.C. - Raising Hell
            {"rank": 578, "musicbrainz_id": "dbf1b3c0-1efb-4e5f-9fe1-4c42b144aa24"},   # Slayer - Reign in Blood
            {"rank": 579, "musicbrainz_id": "77641c44-b2d6-3cfb-a82c-37bbec30abfd"},   # Sonic Youth - EVOL
            {"rank": 580, "musicbrainz_id": "884d5172-4689-33b2-bc8b-592d9556d6c4"},   # Steve Earle - Guitar Town
            {"rank": 581, "musicbrainz_id": "d8dde278-482c-3cc8-a530-fea70476f3a5"},   # The Smiths - The Queen Is Dead
            {"rank": 582, "musicbrainz_id": "1eb45345-2fee-3be5-8b0a-5b91238de4f4"},   # The The - Infected
            {"rank": 583, "musicbrainz_id": "7519fa49-4bcc-38b3-aad3-8517b5389f2e"},   # Throwing Muses - Throwing Muses
            {"rank": 584, "musicbrainz_id": "507d4ab2-03f0-3b8a-a076-cb37d0f970c7"},   # XTC - Skylarking
            {"rank": 585, "musicbrainz_id": "413bc69f-9391-3fe3-802b-5bf4922f6066"},   # Anthrax - Among the Living
            {"rank": 586, "musicbrainz_id": "505efa10-c8c9-3741-814f-9d9fe44e49cf"},   # Butthole Surfers - Locust Abortion Technician
            {"rank": 587, "musicbrainz_id": "12fa3845-7c62-36e5-a8da-8be137155a72"},   # Def Leppard - Hysteria
            {"rank": 588, "musicbrainz_id": "e59021bd-1710-3c13-9449-b78560039592"},   # Depeche Mode - Music for the Masses
            {"rank": 589, "musicbrainz_id": "40f8a16c-568b-3b94-9682-863c4dc7ab66"},   # Dinosaur - You’re Living All Over Me
            {"rank": 590, "musicbrainz_id": "a7ec1997-bffa-40b5-826b-a9e5e12f81f0"},   # TrioTrio - Trio Trio
            {"rank": 591, "musicbrainz_id": "4e61585f-f341-3174-85cf-afad8df46fbe"},   # George Michael - Faith
            {"rank": 592, "musicbrainz_id": "a0b94d0a-210b-4b15-bd1d-93be2196c14a"},   # Guns N’ Roses - Appetite for Destruction
            {"rank": 593, "musicbrainz_id": "c3375e84-7473-3623-8545-889f32cc6f2c"},   # Hüsker Dü - Warehouse: Songs and Stories
            {"rank": 594, "musicbrainz_id": "77691ed4-949d-3487-9cec-00bd8d79fa26"},   # John Zorn - Spy vs. Spy: The Music of Ornette Coleman
            {"rank": 595, "musicbrainz_id": "a7db6b13-54c1-4628-9182-60d97d4e101c"},   # Ladysmith Black Mambazo - Shaka Zulu
            {"rank": 596, "musicbrainz_id": "6c5d92c6-d16b-31ad-a424-2d18b058734e"},   # Laibach - Opus Dei
            {"rank": 597, "musicbrainz_id": "a5711a77-42d1-3f4c-830c-e27a96f0800f"},   # Michael Jackson - Bad
            {"rank": 598, "musicbrainz_id": "28fde873-9dcd-35f7-9521-8d446ee2753b"},   # Napalm Death - Scum
            {"rank": 599, "musicbrainz_id": "6de9a233-13dd-30b5-ad30-61c5814774c5"},   # Pet Shop Boys - Actually
            {"rank": 600, "musicbrainz_id": "a47f26f1-6166-46bd-9612-cb4c327ffe5f"},   # Prince - Sign o’ the Times Live!
            {"rank": 601, "musicbrainz_id": "137385b2-b4cc-385e-9d59-781e7674f5bc"},   # R.E.M. - Document
            {"rank": 602, "musicbrainz_id": "d1ae968e-ed20-35a2-9741-17f82e20bd28"},   # The Sisters of Mercy - Floodland
            {"rank": 603, "musicbrainz_id": "e4256ddc-fa26-3e7f-933b-4de77b05f519"},   # Sonic Youth - Sister
            {"rank": 604, "musicbrainz_id": "072ec17c-aa60-3070-99ab-fce9e9009d97"},   # Talk Talk - The Colour of Spring
            {"rank": 605, "musicbrainz_id": "8958b20d-ce4a-3fa3-95e3-cff2273211aa"},   # Terence Trent D’Arby - Introducing the Hardline According to Terence Trent D’Arby
            {"rank": 606, "musicbrainz_id": "e9e740ec-a09f-3f29-802f-43af41b7e440"},   # The Cult - Electric
            {"rank": 607, "musicbrainz_id": "cda63ecb-5777-37e2-8aa6-32f5c93e0f9f"},   # The Jesus and Mary Chain - Darklands
            {"rank": 608, "musicbrainz_id": "18a15c66-9681-3b6f-9915-7bbfa175bdca"},   # Astor Piazzolla - The New Tango
            {"rank": 609, "musicbrainz_id": "53bcf9cf-db1e-3887-80f5-9f23c87a0f64"},   # The Smiths - Strangeways, Here We Come
            {"rank": 610, "musicbrainz_id": "ca5c8da9-4a92-3e50-aa16-4805c31b7acd"},   # The Triffids - Calenture
            {"rank": 611, "musicbrainz_id": "6f3e9fa6-be7a-3de8-a2b2-2072ece8a54d"},   # U2 - The Joshua Tree
            {"rank": 612, "musicbrainz_id": "84042e46-4063-356e-85b5-0a576170351b"},   # American Music Club - California
            # {"rank": 613, "musicbrainz_id": None},   # NO MATCH: Cowboy Junkies - The Trinity Sessions (1988)
            {"rank": 614, "musicbrainz_id": "0ff9acaf-2710-316d-ba3c-37ded4372c0f"},   # Dagmar Krause - Tank Battles: The Songs of Hanns Eisler / Panzerschlacht: Die Lieder von Hanns Eisler
            {"rank": 615, "musicbrainz_id": "b45028e5-c9d9-34cf-9d2f-0e90ce500c9a"},   # Dinosaur Jr. - Bug
            # {"rank": 616, "musicbrainz_id": None},   # NO MATCH: Dwight Yoakam - Buenos Noches from a Lonely Room (1988)
            {"rank": 617, "musicbrainz_id": "8f9ef1de-e694-33ee-854a-ba5d0bb38dcc"},   # Everything but the Girl - Idlewild
            {"rank": 618, "musicbrainz_id": "98b3437a-6c67-34cb-bc5a-f808bb2b467c"},   # Fishbone - Truth and Soul
            # {"rank": 619, "musicbrainz_id": None},   # NO MATCH: Go-Betweens - 16 Lover's Lane (1988)
            {"rank": 620, "musicbrainz_id": "f13bfae5-5081-364b-97ca-acf0019e5940"},   # Happy Mondays - Bummed
            {"rank": 621, "musicbrainz_id": "97b7e291-8714-3e54-ac24-480be535ee8d"},   # Jane’s Addiction - Nothing’s Shocking
            {"rank": 622, "musicbrainz_id": "054a2fdf-1357-3dbf-89c3-af8f11735dda"},   # k.d. lang - Shadowland
            {"rank": 623, "musicbrainz_id": "7f073c9c-f64f-3a79-bbd8-5aa7668e5cd8"},   # Leonard Cohen - I’m Your Man
            {"rank": 624, "musicbrainz_id": "8ce498ba-26f5-3ea9-b499-9007212ae269"},   # Living Colour - Vivid
            {"rank": 625, "musicbrainz_id": "67553e23-8dad-3792-b6f2-8fedd5650ff3"},   # Metallica - …And Justice for All
            {"rank": 626, "musicbrainz_id": "005909de-978b-3450-a820-c89b7dae787a"},   # Morrissey - Viva Hate
            # {"rank": 627, "musicbrainz_id": None},   # NO MATCH: Mudhoney - Superfuzz Bigmuff (1988)
            {"rank": 628, "musicbrainz_id": "55a73423-bf7d-3969-b1b2-c34c43140e1a"},   # My Bloody Valentine - Isn’t Anything
            {"rank": 629, "musicbrainz_id": "fed1608d-80b7-38d2-aeb8-c6357f0d4c23"},   # N.W.A - Straight Outta Compton
            {"rank": 630, "musicbrainz_id": "01921d99-9d15-3fce-8734-46e58327cfb7"},   # Public Enemy - It Takes a Nation of Millions to Hold Us Back
            {"rank": 631, "musicbrainz_id": "24769a99-8189-3d8c-947e-dbc8574dad5c"},   # Sonic Youth - Daydream Nation
            {"rank": 632, "musicbrainz_id": "74e36cbc-a747-3ebf-a60e-51e656c87741"},   # Pixies - Surfer Rosa
            {"rank": 633, "musicbrainz_id": "46451c52-7d69-3d8a-91f5-9d4b65488f59"},   # The Pogues - If I Should Fall From Grace With God
            {"rank": 634, "musicbrainz_id": "972b3962-49dc-3bbc-ab11-c6b8f7f0838b"},   # The Sugarcubes - Life’s Too Good
            {"rank": 635, "musicbrainz_id": "6730eae2-cc75-3510-97fc-80df1e443aac"},   # The Waterboys - Fisherman’s Blues
            {"rank": 636, "musicbrainz_id": "a738bdf1-f610-30aa-9ae7-9a4f90d6f2d7"},   # Tracy Chapman - Tracy Chapman
            {"rank": 637, "musicbrainz_id": "e600e8fe-df72-33ee-9bcc-131175187453"},   # 808 State - Ninety
            {"rank": 638, "musicbrainz_id": "8f174877-ffc4-39b9-b247-a39fff4097a1"},   # Aerosmith - Pump
            # {"rank": 639, "musicbrainz_id": None},   # NO MATCH: Baaba Maal & Mansour Seck - Djam Leeli (1989)
            {"rank": 640, "musicbrainz_id": "f01b6754-e1bc-3064-a8ef-e6b359f9233d"},   # Barry Adamson - Moss Side Story
            {"rank": 641, "musicbrainz_id": "b534aa01-d621-31ba-9278-38a500e3cdca"},   # Beastie Boys - Paul’s Boutique
            {"rank": 642, "musicbrainz_id": "182a8072-0513-3aa2-b812-9f7a9692731a"},   # Bonnie Raitt - Nick of Time
            {"rank": 643, "musicbrainz_id": "b576dcd9-b1db-3104-a730-f732a86ed60d"},   # Coldcut - What’s That Noise?
            # {"rank": 644, "musicbrainz_id": None},   # NO MATCH: De La Soul - Three Feet High and Rising (1989)
            {"rank": 645, "musicbrainz_id": "1ba7c980-4882-31fb-9918-12791f59d303"},   # Faith No More - The Real Thing
            {"rank": 646, "musicbrainz_id": "6118acdb-7f49-389b-80ec-50a9b12a1690"},   # fIREHOSE - fROMOHIO
            {"rank": 647, "musicbrainz_id": "20aaac17-e4e8-373c-99cc-211321b82832"},   # Janet Jackson - Rhythm Nation 1814
            {"rank": 648, "musicbrainz_id": "2de52330-f003-310c-bc99-94438bf5a904"},   # John Lee Hooker - The Healer
            {"rank": 649, "musicbrainz_id": "2cfffb56-98df-3718-8c8f-631904ca2554"},   # Jungle Brothers - Done by the Forces of Nature
            {"rank": 650, "musicbrainz_id": "ad555095-b0a6-42c8-87aa-8ba035d20e12"},   # Kate Bush - The Sensual World
            {"rank": 651, "musicbrainz_id": "afd82f3b-cab1-3fab-84dc-6c5c80919bd3"},   # Lenny Kravitz - Let Love Rule
            {"rank": 652, "musicbrainz_id": "1f75a8df-176c-3d23-8f1f-b0c8935682ec"},   # Madonna - Like a Prayer
            {"rank": 653, "musicbrainz_id": "daf52bf4-9abf-353e-b226-ef69e1f3e95d"},   # Neneh Cherry - Raw Like Sushi
            {"rank": 654, "musicbrainz_id": "a0902fc4-e3d9-3b2b-bc94-cd4d0e59db29"},   # New Order - Technique
            {"rank": 655, "musicbrainz_id": "7416a063-8697-37a5-af06-af4da329c398"},   # Queen Latifah - All Hail the Queen
            {"rank": 656, "musicbrainz_id": "16a9cef3-b470-3ae1-bf10-cc04232d3e21"},   # R.E.M. - Green
            {"rank": 657, "musicbrainz_id": "cdc4e3e5-8366-3985-aa28-b23b836d2bcc"},   # Soul II Soul - Club Classics Vol. One
            {"rank": 658, "musicbrainz_id": "23e72d60-6199-3f19-b29d-21e460b997ac"},   # Spacemen 3 - Playing With Fire
            {"rank": 659, "musicbrainz_id": "1aa41b19-5a72-341b-bd91-4cf61d1dab6b"},   # Pixies - Doolittle
            {"rank": 660, "musicbrainz_id": "88b86fe0-26f5-3949-817a-8082145e704d"},   # The Stone Roses - The Stone Roses
            {"rank": 661, "musicbrainz_id": "f0b690ac-01cf-321c-a639-3898e464d1af"},   # The Young Gods - L’eau rouge
            {"rank": 662, "musicbrainz_id": "02adb8a7-496c-3a9a-a324-662df73fdba5"},   # A Tribe Called Quest - People’s Instinctive Travels and the Paths of Rhythm
            {"rank": 663, "musicbrainz_id": "12fab6b9-4eaf-33b0-963e-cae03ac332fe"},   # Cocteau Twins - Heaven or Las Vegas
            {"rank": 664, "musicbrainz_id": "4f625d26-3d84-3d3b-8230-2c98e5d45100"},   # Deee‐Lite - World Clique
            {"rank": 665, "musicbrainz_id": "71f1482e-e63f-3b2c-811b-939f62708f2a"},   # Depeche Mode - Violator
            {"rank": 666, "musicbrainz_id": "84abec74-3b40-3a83-9449-46d7e420d4d7"},   # Digital Underground - Sex Packets
            {"rank": 667, "musicbrainz_id": "c7c2de8e-3c98-3923-a4d9-54c4295d20b4"},   # Fugazi - Repeater
            # {"rank": 668, "musicbrainz_id": None},   # NO MATCH: George Michael - Listen Without Prejudice Vol. 1 (1990)
            {"rank": 669, "musicbrainz_id": "f63a7c53-571f-3d4a-a942-053f56590605"},   # Happy Mondays - Pills ’n’ Thrills and Bellyaches
            {"rank": 670, "musicbrainz_id": "baeba3f5-a5aa-3e6e-944f-cca5374192e4"},   # Jane’s Addiction - Ritual de lo habitual
            {"rank": 671, "musicbrainz_id": "30e20b6b-778b-3d6a-aa72-3f821a8dd538"},   # The KLF - The White Room
            {"rank": 672, "musicbrainz_id": "a1440823-4a3f-38c3-8649-a346a86fe1ec"},   # L.L. Cool J - Mama Said Knock You Out
            {"rank": 673, "musicbrainz_id": "19e7c9f3-7c4c-3a56-ba50-4156b39f76ca"},   # Megadeth - Rust in Peace
            {"rank": 674, "musicbrainz_id": "91fdfd77-a868-3678-b9f2-11ad92118955"},   # Neil Young - Ragged Glory
            {"rank": 675, "musicbrainz_id": "751d3b2b-9b6d-3182-8ab5-9b231ab9a7fc"},   # Pet Shop Boys - Behaviour
            {"rank": 676, "musicbrainz_id": "13cf2244-c850-304d-bc46-b30e3f10e0cc"},   # Public Enemy - Fear of a Black Planet
            {"rank": 677, "musicbrainz_id": "4ff18a50-33fa-37aa-a355-ea2a70e35ae3"},   # Ride - Nowhere
            {"rank": 678, "musicbrainz_id": "9747bcfe-7c42-35ac-8c3e-7ecac9f1227b"},   # Sinéad O’Connor - I Do Not Want What I Haven’t Got
            {"rank": 679, "musicbrainz_id": "8114542a-d659-3b5f-a11f-cf86ed7fa84d"},   # Sonic Youth - Goo
            {"rank": 680, "musicbrainz_id": "456a8f06-5f7f-3c30-9be9-111355526469"},   # The Black Crowes - Shake Your Money Maker
            {"rank": 681, "musicbrainz_id": "494bf606-d2f7-36d0-8340-eadad8601d2b"},   # The Cure - Disintegration
            {"rank": 682, "musicbrainz_id": "f57d03ff-b0a5-3b73-a14c-a5ed5f8cd956"},   # The La’s - The La’s
            {"rank": 683, "musicbrainz_id": "e062f23a-ed81-3baf-8f24-8979fef060cc"},   # Pixies - Bossanova
            {"rank": 684, "musicbrainz_id": "0c06a420-01db-36ec-84e4-5371ee6390cc"},   # The Shamen - En-Tact
            {"rank": 685, "musicbrainz_id": "f7e8792d-4aaf-389c-b0e5-a4bbae2bacdf"},   # Ice Cube - AmeriKKKa’s Most Wanted
            {"rank": 686, "musicbrainz_id": "c3733436-fcba-3c08-b082-d548df5c5139"},   # A Tribe Called Quest - The Low End Theory
            {"rank": 687, "musicbrainz_id": "e2d01440-4e91-3dac-8230-72b63992771e"},   # Crowded House - Woodface
            {"rank": 688, "musicbrainz_id": "6845afb3-c21c-47ef-9fae-6244fd8b74d2"},   # Cypress Hill - Cypress Hill
            {"rank": 689, "musicbrainz_id": "b66d223b-f057-3bba-9fee-92ee3db86257"},   # Gang Starr - Step in the Arena
            {"rank": 690, "musicbrainz_id": "5efcd612-f7d0-3eaa-bd04-b712b80f25af"},   # Ice‐T - O.G. Original Gangster
            {"rank": 691, "musicbrainz_id": "0b2902de-d625-3090-a79c-92179202e9e2"},   # Jah Wobble’s Invaders of the Heart - Rising Above Bedlam
            {"rank": 692, "musicbrainz_id": "aa40c6e4-466b-3f32-af95-1f10e6a24edc"},   # Julian Cope - Peggy Suicide
            {"rank": 693, "musicbrainz_id": "c616d884-221b-34db-aa62-7603af3b2394"},   # Koffi Olomidé - Haut De Gamme – Koweit, Rive Gauche
            {"rank": 694, "musicbrainz_id": "8b6f133a-2fdf-3cc2-b84d-1c889adc0939"},   # Massive Attack - Blue Lines
            {"rank": 695, "musicbrainz_id": "997ffa2b-9f07-4995-8095-928ff669eab7"},   # Metallica - Metallica
            {"rank": 696, "musicbrainz_id": "a06ea2e4-c2ff-3169-8af5-5625f0a6ed9a"},   # Mudhoney - Every Good Boy Deserves Fudge
            {"rank": 697, "musicbrainz_id": "cb76227e-3ac0-3002-9a10-615a5b73cc59"},   # My Bloody Valentine - Loveless
            {"rank": 698, "musicbrainz_id": "1b022e01-4da6-387b-8658-8678046e4cef"},   # Nirvana - Nevermind
            {"rank": 699, "musicbrainz_id": "48a1839c-f4e0-3223-831f-fc36ca6ff7cf"},   # Primal Scream - Screamadelica
            {"rank": 700, "musicbrainz_id": "b21f49a6-cd5f-3783-9302-6a727121e787"},   # Public Enemy - Apocalypse 91… The Enemy Strikes Black
            {"rank": 701, "musicbrainz_id": "68bee70d-b425-3813-aca7-dd7b912c3d11"},   # Red Hot Chili Peppers - Blood Sugar Sex Magik
            {"rank": 702, "musicbrainz_id": "726170fb-e4ce-378a-bec4-c74e742920ab"},   # Saint Etienne - Foxbase Alpha
            {"rank": 703, "musicbrainz_id": "6d9ffabb-233a-3cc1-9ac3-d2a8e4c99cdd"},   # Sepultura - Arise
            {"rank": 704, "musicbrainz_id": "e9f4b96a-94df-36be-9659-c9a811caead6"},   # Slint - Spiderland
            {"rank": 705, "musicbrainz_id": "4119fd8b-9858-33c9-8256-fcc1570bc07f"},   # Teenage Fanclub - Bandwagonesque
            {"rank": 706, "musicbrainz_id": "744c7a1b-ac79-35c4-bd92-7e2c6a24c8d8"},   # U2 - Achtung Baby
            {"rank": 707, "musicbrainz_id": "92d8f0c4-8c64-3bee-bee1-812a70e77efa"},   # Alice in Chains - Dirt
            {"rank": 708, "musicbrainz_id": "6842c81d-ea77-3dfd-abf7-4323add3f4d4"},   # Aphex Twin - Selected Ambient Works 85–92
            {"rank": 709, "musicbrainz_id": "ede793b4-4976-3b7a-ba3b-fde6801de64c"},   # Arrested Development - 3 Years, 5 Months and 2 Days in the Life Of…
            {"rank": 710, "musicbrainz_id": "7823bf97-2c4f-35a0-be77-977ae04fa0fb"},   # Baaba Maal - Lam Toro
            {"rank": 711, "musicbrainz_id": "4b9127b6-60bb-373a-9460-f90327947ec4"},   # The Disposable Heroes of Hiphoprisy - Hypocrisy Is the Greatest Luxury
            {"rank": 712, "musicbrainz_id": "fdad4a4d-8cfd-3a6c-a397-0f08861dc967"},   # k.d. lang - Ingénue
            {"rank": 713, "musicbrainz_id": "15cfaf82-5a4b-3ee1-bcce-75561055d27a"},   # Ministry - ΚΕΦΑΛΗΞΘ
            {"rank": 714, "musicbrainz_id": "24ffe899-66f2-3e52-97ea-527531bf4680"},   # Morrissey - Your Arsenal
            {"rank": 715, "musicbrainz_id": "697785ad-05f6-3067-9618-796e811e4ec3"},   # Nick Cave & the Bad Seeds - Henry’s Dream
            {"rank": 716, "musicbrainz_id": "dbfaec14-d410-3775-b538-2d5fbff4358f"},   # Nusrat Fateh Ali Khan & Party - Devotional Songs
            {"rank": 717, "musicbrainz_id": "78e2be48-6a07-31bf-b85f-3a1093177263"},   # PJ Harvey - Dry
            {"rank": 718, "musicbrainz_id": "814e0b20-6884-31c5-9d99-d215f048cfd6"},   # Pantera - Vulgar Display of Power
            {"rank": 719, "musicbrainz_id": "cea5d18a-1924-3cda-bebc-38933834b25d"},   # Pearl Jam - Ten
            {"rank": 720, "musicbrainz_id": "c86c6af9-d10e-3079-b34b-30b682a797eb"},   # R.E.M. - Automatic for the People
            {"rank": 721, "musicbrainz_id": "30fef5ef-b1d4-36b5-8f75-f45b8e76c545"},   # Sonic Youth - Dirty
            {"rank": 722, "musicbrainz_id": "e12a1258-c0cf-326d-80c4-782763ff3c46"},   # Spiritualized - Lazer Guided Melodies
            {"rank": 723, "musicbrainz_id": "069b2e51-c7a9-32f4-a5f1-704ad00f13da"},   # Stereo MC’s - Connected
            {"rank": 724, "musicbrainz_id": "997a4855-3bd3-3e5c-81d0-656209b3aa74"},   # Sugar - Copper Blue
            {"rank": 725, "musicbrainz_id": "d8cf6f02-a68b-4b73-be3e-746fb5a5adf6"},   # Lemonheads - It’s a Shame About Ray
            {"rank": 726, "musicbrainz_id": "c799ef0c-f038-364b-972b-51f52d794781"},   # The Pharcyde - Bizarre Ride II the Pharcyde
            {"rank": 727, "musicbrainz_id": "b65ca7b8-4069-3782-9c4c-b2353cc4bc04"},   # Tom Waits - Bone Machine
            {"rank": 728, "musicbrainz_id": "cb10018e-e795-3b62-b9d6-f143d188e496"},   # Tori Amos - Little Earthquakes
            {"rank": 729, "musicbrainz_id": "02e4e84f-5d06-3288-bcfd-32522ba23bd9"},   # The Auteurs - New Wave
            {"rank": 730, "musicbrainz_id": "6891a28c-5865-36e2-9e5f-c9fac1d3595f"},   # Björk - Debut
            {"rank": 731, "musicbrainz_id": "e7affd78-d157-4772-a468-675fa4309c61"},   # Blur - Modern Life Is Rubbish
            {"rank": 732, "musicbrainz_id": "ad444843-7160-33d7-b0c9-fc99f2c14a99"},   # Dr. Dre - The Chronic
            # {"rank": 733, "musicbrainz_id": None},   # NO MATCH: Girls Against Boys - Venus Luxure No1 Baby (1993)
            {"rank": 734, "musicbrainz_id": "290cd1a5-22cc-3db4-817e-bf264be59fd0"},   # Grant Lee Buffalo - Fuzzy
            {"rank": 735, "musicbrainz_id": "2e904c43-e060-3a4c-aa6d-7e4cd8f7cde8"},   # Ice Cube - The Predator
            {"rank": 736, "musicbrainz_id": "07d5dcac-a3a5-3691-9a88-44bff141aecb"},   # Jamiroquai - Emergency on Planet Earth
            {"rank": 737, "musicbrainz_id": "424d0675-f87c-3937-bc38-6b29810d1152"},   # MC Solaar - Qui sème le vent récolte le tempo
            {"rank": 738, "musicbrainz_id": "2a0981fb-9593-3019-864b-ce934d97a16e"},   # Nirvana - In Utero
            # {"rank": 739, "musicbrainz_id": None},   # NO MATCH: Orbital - Orbital (brown album) (1993)
            {"rank": 740, "musicbrainz_id": "c1bb54cc-751d-300c-ba29-d7502d571c2d"},   # PJ Harvey - Rid of Me
            {"rank": 741, "musicbrainz_id": "2fb89402-6ed9-3f5b-b267-d77ac921b2d2"},   # Paul Weller - Wild Wood
            {"rank": 742, "musicbrainz_id": "869f9eac-2a40-3a41-80a3-6bf2297a7cbc"},   # Pavement - Slanted and Enchanted
            {"rank": 743, "musicbrainz_id": "c56fbb2a-f0f2-370a-94aa-e3e2864f5847"},   # Pet Shop Boys - Very
            {"rank": 744, "musicbrainz_id": "55399028-fe94-48c7-867a-3ad4fae84569"},   # Rage Against the Machine - Rage Against the Machine
            {"rank": 745, "musicbrainz_id": "41c08aa5-8de6-351b-aaca-f79d594e7793"},   # Sebadoh - Bubble and Scrape
            {"rank": 746, "musicbrainz_id": "0f0ecd4f-1d20-34b9-9f67-5aaa785c7f11"},   # Sheryl Crow - Tuesday Night Music Club
            {"rank": 747, "musicbrainz_id": "a159e102-18bb-42ca-a59e-5f96a7eff241"},   # Smashing Pumpkins - Siamese Dream
            {"rank": 748, "musicbrainz_id": "f5519a60-cada-496a-8315-9a2b6339ee41"},   # Master Tempo - Doggy Style
            {"rank": 749, "musicbrainz_id": "f880fa4d-1694-49b8-a000-10cc52fe9812"},   # Suede - Suede
            {"rank": 750, "musicbrainz_id": "3b27e8ac-c904-3b1e-a4a9-920c79664dfa"},   # The Afghan Whigs - Gentlemen
            {"rank": 751, "musicbrainz_id": "dbcc977c-ddcf-3dc6-921a-e31ec1e7ab90"},   # The Boo Radleys - Giant Steps
            {"rank": 752, "musicbrainz_id": "ef245bd8-7937-313b-a787-f290653e0957"},   # The Fall - The Infotainment Scan
            {"rank": 753, "musicbrainz_id": "a045be5a-5bc2-35f1-9860-6dc999ae64b9"},   # Aimee Mann - Whatever
            {"rank": 754, "musicbrainz_id": "47629863-75ca-3a1e-a987-716736942e25"},   # William Orbit - Strange Cargo III
            {"rank": 755, "musicbrainz_id": "610fb60f-900a-3c42-ac7d-f6b6aa8035f9"},   # Wu‐Tang Clan - Enter the Wu‐Tang (36 Chambers)
            {"rank": 756, "musicbrainz_id": "a5a7a716-a039-3815-aee3-88ac135721c5"},   # Ali Farka Touré - Talking Timbuktu
            {"rank": 757, "musicbrainz_id": "1134696c-1078-3c38-bcaa-4ee7c320670a"},   # Beastie Boys - Ill Communication
            {"rank": 758, "musicbrainz_id": "67461c8e-d864-3910-9bf4-39e44357aac9"},   # Blur - Parklife
            {"rank": 759, "musicbrainz_id": "532210d8-5101-3893-a2bb-f9cd8df6e303"},   # Drive Like Jehu - Yank Crime
            {"rank": 760, "musicbrainz_id": "361a52d4-9656-307f-b7e4-480e3103a73c"},   # Elvis Costello - Brutal Youth
            {"rank": 761, "musicbrainz_id": "0977c169-d4dc-37d3-89fa-2f2f60e4e43d"},   # Frank Black - Teenager of the Year
            {"rank": 762, "musicbrainz_id": "d54dc508-1b22-3922-8839-6ddcfff10b7d"},   # G. Love & Special Sauce - G. Love & Special Sauce
            {"rank": 763, "musicbrainz_id": "314cffd4-daa5-3337-85e5-e54165a96113"},   # Green Day - Dookie
            {"rank": 764, "musicbrainz_id": "fe676d05-f97c-303a-890b-da53c69e5d42"},   # Hole - Live Through This
            {"rank": 765, "musicbrainz_id": "4c1feb97-bc6c-32f9-8adb-bd85105fdaa0"},   # Jeru the Damaja - The Sun Rises in the East
            {"rank": 766, "musicbrainz_id": "c186db82-9988-367e-8486-2e38e9b6c8db"},   # Liz Phair - Exile in Guyville
            {"rank": 767, "musicbrainz_id": "ded46e46-788d-3c1f-b21b-9f5e9c37b1bc"},   # Massive Attack - Protection
            {"rank": 768, "musicbrainz_id": "85af95fb-f93d-30e9-b60e-9ee6eb00d42b"},   # Method Man - Tical
            {"rank": 769, "musicbrainz_id": "627c18bf-ce65-3f4d-8695-cc0431933e3f"},   # Morrissey - Vauxhall and I
            {"rank": 770, "musicbrainz_id": "28298e2c-4d70-3eed-a0f5-a3280c662b3d"},   # Nas - Illmatic
            {"rank": 771, "musicbrainz_id": "7c4cab8d-dead-3870-b501-93c90fd0a580"},   # Nine Inch Nails - The Downward Spiral
            {"rank": 772, "musicbrainz_id": "fb3770f6-83fb-32b7-85c4-1f522a92287e"},   # Nirvana - MTV Unplugged in New York
            {"rank": 773, "musicbrainz_id": "5afcfeac-118a-35e6-af0d-35ec9003354d"},   # The Notorious B.I.G. - Ready to Die
            {"rank": 774, "musicbrainz_id": "451dca98-c118-32e1-9244-c47ca9c3c0f9"},   # Oasis - Definitely Maybe
            {"rank": 775, "musicbrainz_id": "a55a5a03-0c0e-311b-85df-ec52f841715c"},   # Offspring - Smash
            {"rank": 776, "musicbrainz_id": "9f3f29eb-109b-3080-8705-a0be659e21cf"},   # Orbital - Snivilisation
            {"rank": 777, "musicbrainz_id": "4f348977-6f44-39f9-b243-071927ecc6a4"},   # Pavement - Crooked Rain, Crooked Rain
            {"rank": 778, "musicbrainz_id": "48140466-cff6-3222-bd55-63c27e43190d"},   # Portishead - Dummy
            {"rank": 779, "musicbrainz_id": "f9fa083f-db00-3048-99e7-5b186672bb09"},   # The Prodigy - Music for the Jilted Generation
            {"rank": 780, "musicbrainz_id": "61ec3e33-4f43-39bf-ae36-7869126d8285"},   # The Sabres of Paradise - Haunted Dancehall
            {"rank": 781, "musicbrainz_id": "8300fe9c-0022-3c55-8a3e-8dc61f282e8c"},   # Soundgarden - Superunknown
            {"rank": 782, "musicbrainz_id": "da15737e-3eb3-31e4-97f0-fe46299f75fb"},   # Suede - Dog Man Star
            {"rank": 783, "musicbrainz_id": "7882cea8-bd15-3ff7-a62a-f22f49c6a0c1"},   # Manic Street Preachers - The Holy Bible
            {"rank": 784, "musicbrainz_id": "cfc98a2a-6aaa-3dda-a01d-e034e56c4fec"},   # 2Pac - Me Against the World
            {"rank": 785, "musicbrainz_id": "ee3d18ed-d6a8-37c7-a964-41bbdb6d59f1"},   # Alanis Morissette - Jagged Little Pill
            {"rank": 786, "musicbrainz_id": "a4591f67-48d9-36ae-bc68-2deb954d0a15"},   # D’Angelo - Brown Sugar
            {"rank": 787, "musicbrainz_id": "f1cbf448-c205-3642-a4c5-6042989d8ed4"},   # Elastica - Elastica
            {"rank": 788, "musicbrainz_id": "4bf6210c-ecb3-3ad8-805f-a1ac55ebbe60"},   # Femi Kuti - Femi Kuti
            {"rank": 789, "musicbrainz_id": "440c9ce8-8ce4-3103-a745-0b385ae70a34"},   # Foo Fighters - Foo Fighters
            {"rank": 790, "musicbrainz_id": "dcad245f-9d95-3751-9e69-d50ca399b46a"},   # Garbage - Garbage
            {"rank": 791, "musicbrainz_id": "6075a004-e983-3a00-8a13-50af32f0e200"},   # Genius/GZA - Liquid Swords
            {"rank": 792, "musicbrainz_id": "7a752bd0-8ef8-3811-96c9-5cf53535152e"},   # Goldie - Timeless
            {"rank": 793, "musicbrainz_id": "5cb308cd-3d5c-3682-b568-2fc374dc2ed7"},   # Guided by Voices - Alien Lanes
            {"rank": 794, "musicbrainz_id": "ea29c347-696f-3165-986d-7bad1394b178"},   # Jeff Buckley - Grace
            {"rank": 795, "musicbrainz_id": "9345480c-e2d2-3cb9-9205-88c8a70e911d"},   # Leftfield - Leftism
            {"rank": 796, "musicbrainz_id": "c4482347-92da-3a29-8ed6-78655ed02f66"},   # Nightmares on Wax - Smokers Delight
            {"rank": 797, "musicbrainz_id": "cc7e6348-cc55-31fa-aeb2-748a46a81cb3"},   # Oasis - (What’s the Story) Morning Glory?
            {"rank": 798, "musicbrainz_id": "88f69eab-8f07-343b-847c-b944ad33dfcf"},   # Pulp - Different Class
            {"rank": 799, "musicbrainz_id": "b8048f24-c026-3398-b23a-b5e50716cbc7"},   # Radiohead - The Bends
            {"rank": 800, "musicbrainz_id": "ab981b48-9a7b-34c4-b46a-f6266317ce7c"},   # Raekwon - Only Built 4 Cuban Linx…
            {"rank": 801, "musicbrainz_id": "ef9bedc1-12c2-3f31-9712-059a4263e55f"},   # Rocket From the Crypt - Scream, Dracula, Scream!
            {"rank": 802, "musicbrainz_id": "1af599c9-0b44-3a5a-a06b-39e8db6b2b4e"},   # The Smashing Pumpkins - Mellon Collie and the Infinite Sadness
            {"rank": 803, "musicbrainz_id": "6e796029-272d-3fe2-8ad0-d8a10ef80a66"},   # Supergrass - I Should Coco
            {"rank": 804, "musicbrainz_id": "8fffd616-de95-3597-b1f2-211666cfc2dd"},   # The Chemical Brothers - Exit Planet Dust
            {"rank": 805, "musicbrainz_id": "2e65b39d-405f-3b59-84ec-5f3e8e660b95"},   # The Verve - A Northern Soul
            {"rank": 806, "musicbrainz_id": "3d886c06-a4c7-3431-be87-2b2940f07acd"},   # TLC - CrazySexyCool
            {"rank": 807, "musicbrainz_id": "9fd2415f-182f-39c1-aa02-5acb36f99bef"},   # Tricky - Maxinquaye
            {"rank": 808, "musicbrainz_id": "2b87d240-123b-350c-a9e1-a4f6be883a99"},   # Ash - 1977
            {"rank": 809, "musicbrainz_id": "bd3f1efd-d700-34e5-86f4-f528dcf25264"},   # Barry Adamson - Oedipus Schmoedipus
            {"rank": 810, "musicbrainz_id": "df0bfd42-78a9-40c3-a45f-a12e10d446f8"},   # Beck - Odelay
            {"rank": 811, "musicbrainz_id": "66be5deb-75d5-3737-9037-1c745891d3ec"},   # Belle and Sebastian - If You’re Feeling Sinister
            {"rank": 812, "musicbrainz_id": "a36f3183-e862-3829-a4eb-b924264c76b6"},   # Belle and Sebastian - Tigermilk
            {"rank": 813, "musicbrainz_id": "4b2186f5-ff00-3227-ae11-783ba93e1089"},   # DJ Shadow - Endtroducing.....
            {"rank": 814, "musicbrainz_id": "b38e21f6-8f76-3f87-a021-e91afad9e7e5"},   # Dr. Octagon - Dr. Octagonecologyst
            {"rank": 815, "musicbrainz_id": "d49f838a-5a6e-3f28-8984-269fc40a8a3c"},   # Everything but the Girl - Walking Wounded
            {"rank": 816, "musicbrainz_id": "0af908c7-0ec7-3183-b677-1240f6e47b9c"},   # Fatboy Slim - Better Living Through Chemistry
            {"rank": 817, "musicbrainz_id": "82ba556e-99bf-380d-b9b5-5a97737f1cd1"},   # Fiona Apple - Tidal
            {"rank": 818, "musicbrainz_id": "4c3b1b47-f80e-37da-a5a8-1fb1c0cb7cdd"},   # The Jon Spencer Blues Explosion - Now I Got Worry
            {"rank": 819, "musicbrainz_id": "3ae18f4d-8a99-3dd1-b9d0-7275adc3bd92"},   # LTJ Bukem - Logical Progression
            {"rank": 820, "musicbrainz_id": "6cb17389-101a-3f0a-8864-bea548465406"},   # Marilyn Manson - Antichrist Superstar
            {"rank": 821, "musicbrainz_id": "e8d49b88-b411-35f9-9e34-4370a9708ef2"},   # Maxwell - Maxwell’s Urban Hang Suite
            {"rank": 822, "musicbrainz_id": "4030ac23-b953-33ee-9f31-35e9f3febf86"},   # Nick Cave and the Bad Seeds - Murder Ballads
            {"rank": 823, "musicbrainz_id": "078d0c59-9b9b-3551-b2fa-dfa57a9fe9ae"},   # Screaming Trees - Dust
            {"rank": 824, "musicbrainz_id": "f625cd30-9427-360b-b63d-e294d23b1980"},   # Sepultura - Roots
            {"rank": 825, "musicbrainz_id": "1c51069d-4c59-4ddf-bd12-dacefada37c3"},   # Stereolab - Emperor Tomato Ketchup
            {"rank": 826, "musicbrainz_id": "69cadaa8-c952-3122-92d8-c4f41da065ac"},   # Super Furry Animals - Fuzzy Logic
            {"rank": 827, "musicbrainz_id": "33a35fc0-1126-30c2-a046-b2803116f882"},   # The Cardigans - First Band on the Moon
            {"rank": 828, "musicbrainz_id": "a9f71672-e2d5-304b-a6d9-348d9fdad11c"},   # The Charlatans - Tellin’ Stories
            {"rank": 829, "musicbrainz_id": "4e972fc5-f217-378e-a0ff-ea8fa32d1d5e"},   # The Divine Comedy - Casanova
            {"rank": 830, "musicbrainz_id": "119a9488-9980-3645-be68-f50210a35a26"},   # eels - Beautiful Freak
            {"rank": 831, "musicbrainz_id": "2c095917-0839-31c0-9a43-725813c59068"},   # The Tender Box - The Score
            {"rank": 832, "musicbrainz_id": "3f7d2215-c754-3401-a9c6-4d3f8ec3dc03"},   # Fun Lovin’ Criminals - Come Find Yourself
            {"rank": 833, "musicbrainz_id": "c26969b8-13ce-3bb5-996a-eed9e21e1149"},   # Manic Street Preachers - Everything Must Go
            {"rank": 834, "musicbrainz_id": "7bb7debb-bdcf-3991-aa19-2937a1ad4fa9"},   # Tortoise - Millions Now Living Will Never Die
            {"rank": 835, "musicbrainz_id": "c0b6864a-9de7-3a2e-897b-e07919cab0e4"},   # Underworld - Second Toughest in the Infants
            {"rank": 836, "musicbrainz_id": "5aed5f2c-4b8a-35a7-9655-906e3ea72fa1"},   # Wilco - Being There
            {"rank": 837, "musicbrainz_id": "fdd6c833-3c96-33cb-9917-72e15bcd34bc"},   # Blur - Blur
            {"rank": 838, "musicbrainz_id": "dad1dada-1fda-3186-beb7-3bc80e90f9e0"},   # Bob Dylan - Time Out of Mind
            {"rank": 839, "musicbrainz_id": "32bbab8e-02c0-30d2-9e23-a19739864b84"},   # Buena Vista Social Club - Buena Vista Social Club
            {"rank": 840, "musicbrainz_id": "070fb0a3-76ff-34fb-a892-19f6c7d303f6"},   # Cornershop - When I Was Born for the 7th Time
            {"rank": 841, "musicbrainz_id": "00054665-89fa-33d5-a8f0-1728ea8c32c3"},   # Daft Punk - Homework
            {"rank": 842, "musicbrainz_id": "65ee6fe4-2f93-3ec4-afca-801bc8fe6a3f"},   # David Holmes - Let’s Get Killed
            {"rank": 843, "musicbrainz_id": "dfb85157-313b-3f5f-8739-a5162bcb6345"},   # Elliott Smith - Either/Or
            {"rank": 844, "musicbrainz_id": "3944908c-c3a3-30a3-9ec8-35262721184c"},   # Finley Quaye - Maverick a Strike
            {"rank": 845, "musicbrainz_id": "1ea6ffaa-df4f-31cc-955f-0fc57a9cf864"},   # Mariah Carey - Butterfly
            {"rank": 846, "musicbrainz_id": "45a68d94-6923-38c1-a6dd-4cfc1cdc193a"},   # Missy Misdemeanor Elliott - Supa Dupa Fly
            {"rank": 847, "musicbrainz_id": "af11e225-96a0-3b42-8645-54d9e8906054"},   # Nick Cave & the Bad Seeds - The Boatman’s Call
            {"rank": 848, "musicbrainz_id": "ed585ebf-919f-3a78-a985-c261f67b0aa4"},   # Primal Scream - Vanishing Point
            {"rank": 849, "musicbrainz_id": "ac9138ce-6331-3f8d-86d7-69f13e4ab4f4"},   # Prodigy - The Fat of the Land
            {"rank": 850, "musicbrainz_id": "b1392450-e666-3926-a536-22c65f834433"},   # Radiohead - OK Computer
            {"rank": 851, "musicbrainz_id": "1cd3a513-be39-373c-b56d-54a3fed5b928"},   # Robbie Williams - Life Thru a Lens
            {"rank": 852, "musicbrainz_id": "aa501697-af7b-34c2-9276-03118977f9fe"},   # Robert Wyatt - Shleep
            {"rank": 853, "musicbrainz_id": "89de0232-18d8-3816-b936-5456658cdec9"},   # Roni Size / Reprazent - New Forms²
            {"rank": 854, "musicbrainz_id": "209b45b7-8b2f-3e07-b194-efff9cde80dd"},   # Sleater‐Kinney - Dig Me Out
            {"rank": 855, "musicbrainz_id": "c88c77da-b9f9-34b9-abdf-ad3cec875aca"},   # Spiritualized - Ladies and Gentlemen We Are Floating in Space
            {"rank": 856, "musicbrainz_id": "67c36698-2a14-3f95-b9ea-75804a7f5a8e"},   # Supergrass - In It for the Money
            {"rank": 857, "musicbrainz_id": "69f4aa7f-d760-3890-bd2a-902fb9abe40b"},   # The Chemical Brothers - Dig Your Own Hole
            {"rank": 858, "musicbrainz_id": "53cd5789-ae30-3bee-9aeb-377265aaecad"},   # The Dandy Warhols - …The Dandy Warhols Come Down
            {"rank": 859, "musicbrainz_id": "381bcdcb-ec75-37b0-8201-f7bb16fa6583"},   # The Divine Comedy - A Short Album About Love
            {"rank": 860, "musicbrainz_id": "3dd0c8e4-af53-3605-9c20-f27c7635fb60"},   # The Verve - Urban Hymns
            {"rank": 861, "musicbrainz_id": "b0bf2b77-b8cf-32f6-8893-9741d757b400"},   # Air - Moon Safari
            {"rank": 862, "musicbrainz_id": "9ae4e54c-ec74-3f15-823a-8302fc9a832d"},   # Billy Bragg - Mermaid Avenue
            {"rank": 863, "musicbrainz_id": "17d74d52-c92b-3b8d-9f87-218ab2d1c4a0"},   # Boards of Canada - Music Has the Right to Children
            {"rank": 864, "musicbrainz_id": "49da924d-13fd-32be-8e22-7093f5ef400e"},   # Bob Dylan - The Bootleg Series, Vol. 4: Live 1966: The “Royal Albert Hall” Concert
            {"rank": 865, "musicbrainz_id": "ed247591-9a60-3d95-906c-2d1eae52639b"},   # Bonnie 'Prince' Billy - I See a Darkness
            {"rank": 866, "musicbrainz_id": "faeb8741-2ca0-3ca6-8a1a-70bab1e67c82"},   # Britney Spears - …Baby One More Time
            {"rank": 867, "musicbrainz_id": "67c151dc-4702-3fdc-9bea-9b6256758e11"},   # David Gray - White Ladder
            {"rank": 868, "musicbrainz_id": "435fe38e-404c-3887-8300-cc94420a121c"},   # Fatboy Slim - You’ve Come a Long Way, Baby
            {"rank": 869, "musicbrainz_id": "bdf37fad-7332-3efb-8e7e-073d1c756c7e"},   # Hole - Celebrity Skin
            {"rank": 870, "musicbrainz_id": "6d098cc2-5165-367e-9200-7afa2d019485"},   # Khaled - Kenza
            {"rank": 871, "musicbrainz_id": "4a8ff174-fcd8-38d4-8ed3-a46334759251"},   # Kid Rock - Devil Without a Cause
            {"rank": 872, "musicbrainz_id": "e47ad139-89f6-39e8-aa84-fe84c45aeb7d"},   # Korn - Follow the Leader
            {"rank": 873, "musicbrainz_id": "8691d12c-abd8-385c-b1eb-d841190124f7"},   # Lauryn Hill - The Miseducation of Lauryn Hill
            {"rank": 874, "musicbrainz_id": "493de006-33bf-3404-9bb7-1f3b0c22ce05"},   # Lucinda Williams - Car Wheels on a Gravel Road
            {"rank": 875, "musicbrainz_id": "cb93e87f-5d21-3447-a6e8-22d44f9b0d7a"},   # Madonna - Ray of Light
            {"rank": 876, "musicbrainz_id": "24a451c9-a8f3-33f9-a4fc-5e2d00cb7816"},   # Manu Chao - Clandestino
            {"rank": 877, "musicbrainz_id": "09c61550-5780-3fb4-b5ec-8b873fe4e8a9"},   # Mercury Rev - Deserter’s Songs
            {"rank": 878, "musicbrainz_id": "1ab343e8-490d-32a6-a6c8-1e56cf33c888"},   # Pulp - This Is Hardcore
            {"rank": 879, "musicbrainz_id": "17ee0d7f-4a9d-317f-a0b0-8ca528a34b19"},   # Queens of the Stone Age - Queens of the Stone Age
            {"rank": 880, "musicbrainz_id": "97f37409-b91a-3495-8e70-56fd9f7658c2"},   # System of a Down - System of a Down
            {"rank": 881, "musicbrainz_id": "1a203a3e-4663-3a09-a9d1-b3673f8949e5"},   # Talvin Singh - OK
            {"rank": 882, "musicbrainz_id": "fd350da8-c2a9-3f67-8ed8-91d0c40060c7"},   # Turboneger - Apocalypse Dudes
            {"rank": 883, "musicbrainz_id": "3ce95abe-66f2-4e21-a365-0a4766e33e30"},   # Basement Jaxx - Remedy
            {"rank": 884, "musicbrainz_id": "e11d0dc5-1fff-3eec-bcea-803bee9578d9"},   # Beth Orton - Central Reservation
            {"rank": 885, "musicbrainz_id": "3b74156f-e774-37bb-b4b9-a820a145d865"},   # Death in Vegas - The Contino Sessions
            {"rank": 886, "musicbrainz_id": "be725de4-4633-3c8a-9a03-f2c4392b6e0d"},   # Eminem - The Slim Shady LP
            {"rank": 887, "musicbrainz_id": "1a021034-95d1-3a2d-bdca-73b25e455e49"},   # The Flaming Lips - The Soft Bulletin
            {"rank": 888, "musicbrainz_id": "387aca0c-d34a-3d0c-b7e4-c1b0f73e2dae"},   # Incubus - Make Yourself
            {"rank": 889, "musicbrainz_id": "116d142c-e7fd-3902-8ca5-0d4999abd00e"},   # Le Tigre - Le Tigre
            {"rank": 890, "musicbrainz_id": "6d267ba8-89c3-3eef-84bd-a225e6f59000"},   # Les Rythmes Digitales - Darkdancer
            {"rank": 891, "musicbrainz_id": "49371adc-871d-38f6-bb60-fd9e5af6795f"},   # Metallica - S&M
            {"rank": 892, "musicbrainz_id": "7f6a4e72-9fee-39db-8817-63425f97a0f5"},   # Moby - Play
            {"rank": 893, "musicbrainz_id": "4a65b47b-8ef9-3295-ad4e-a7c93294259b"},   # Nitin Sawhney - Beyond Skin
            {"rank": 894, "musicbrainz_id": "ca5dfcc3-83fb-3eee-9061-c27296b77b2c"},   # Red Hot Chili Peppers - Californication
            {"rank": 895, "musicbrainz_id": "9fc9bf6f-4bb9-3b73-98b5-66f89bff6c82"},   # Suba - São Paulo Confessions
            {"rank": 896, "musicbrainz_id": "cf351133-87b1-3f74-9ee4-97bd3fb6956a"},   # Shack - H.M.S. Fable
            {"rank": 897, "musicbrainz_id": "62b427b8-1c52-34e7-b250-da2aa3e44860"},   # Sigur Rós - Ágætis byrjun
            {"rank": 898, "musicbrainz_id": "fd11c3c2-6f11-3a79-b6b4-f4256b899fa6"},   # Skunk Anansie - Post Orgasmic Chill
            {"rank": 899, "musicbrainz_id": "5140eef4-5b5d-309c-a3aa-5c5da107b1da"},   # Slipknot - Slipknot
            {"rank": 900, "musicbrainz_id": "5dfac852-1aed-35b2-93b6-e8f9c93fe521"},   # The Magnetic Fields - 69 Love Songs
            {"rank": 901, "musicbrainz_id": "d96bd9ec-329a-3740-9eb5-e65257445afa"},   # Travis - The Man Who
            # {"rank": 902, "musicbrainz_id": None},   # NO MATCH: XTC - Apple Venus Vol. 1 (1999)
            {"rank": 903, "musicbrainz_id": "80aa8257-7bc5-39c0-87e1-95941e4c746c"},   # Air - The Virgin Suicides
            {"rank": 904, "musicbrainz_id": "b53623c2-266f-393f-9bc5-71eaac3b5a31"},   # Badly Drawn Boy - The Hour of Bewilderbeast
            {"rank": 905, "musicbrainz_id": "84afe68c-10a8-38cd-9157-3a327257449d"},   # Bebel Gilberto - Tanto tempo
            {"rank": 906, "musicbrainz_id": "1dc4c347-a1db-32aa-b14f-bc9cc507b843"},   # Coldplay - Parachutes
            {"rank": 907, "musicbrainz_id": "fabc3ec9-2656-3a98-8fdd-4bc40a9ca8ba"},   # Common - Like Water for Chocolate
            {"rank": 908, "musicbrainz_id": "2fd75c21-7a92-3bcc-b045-d5bab5c36d11"},   # Elliott Smith - Figure 8
            {"rank": 909, "musicbrainz_id": "b0fa91c8-0996-38f1-ab84-797f58d7c4eb"},   # Eminem - The Marshall Mathers LP
            {"rank": 910, "musicbrainz_id": "c09bf526-416d-3f9c-8291-8794cef83d87"},   # Emmylou Harris - Red Dirt Girl
            {"rank": 911, "musicbrainz_id": "25bdfd28-72ca-3d1f-88fc-dcf67df91720"},   # Erykah Badu - Mama’s Gun
            {"rank": 912, "musicbrainz_id": "2b10653e-655d-34fe-9db4-77242d817a17"},   # Giant Sand - Chore of Enchantment
            {"rank": 913, "musicbrainz_id": "4999b316-bacf-3bf9-9cf9-07c4ebae470a"},   # Goldfrapp - Felt Mountain
            {"rank": 914, "musicbrainz_id": "4ae785f1-e986-3909-ab99-30e32024f94a"},   # Lambchop - Nixon
            {"rank": 915, "musicbrainz_id": "55203b2f-314b-39c2-9e48-56a95e41a337"},   # Limp Bizkit - Chocolate Starfish and the Hot Dog Flavored Water
            {"rank": 916, "musicbrainz_id": "43091de5-04b6-46e6-b181-b457694f4ce0"},   # Linkin Park - Hybrid Theory
            {"rank": 917, "musicbrainz_id": "0a0808d5-8f78-382f-87af-f9d6fedf3f68"},   # Madonna - Music
            {"rank": 918, "musicbrainz_id": "c0ea5f23-70ad-373e-9ca5-5eaeaf00c0ce"},   # Mike Ladd - Welcome to the Afterfuture
            {"rank": 919, "musicbrainz_id": "b2bcd09d-d66b-36c8-afcb-0d448b1127d9"},   # MJ Cole - Sincere
            {"rank": 920, "musicbrainz_id": "00d2cd53-21c9-3738-b683-56847b7b0040"},   # OutKast - Stankonia
            {"rank": 921, "musicbrainz_id": "71641af7-d122-326a-b0bb-f76a8d09810c"},   # PJ Harvey - Stories From the City, Stories From the Sea
            {"rank": 922, "musicbrainz_id": "e75c0549-ad55-39e3-8025-c72c5d4a3c5d"},   # Radiohead - Kid A
            # {"rank": 923, "musicbrainz_id": None},   # NO MATCH: Red Snapper - Our Aim is to Satisfy Red Snapper (2000)
            {"rank": 924, "musicbrainz_id": "66571bda-46b6-3384-8ebb-7d09a1b1f169"},   # Ryan Adams - Heartbreaker
            {"rank": 925, "musicbrainz_id": "28438e4f-3710-459f-a332-a1eba9dd1f26"},   # The Avalanches - Since I Left You
            {"rank": 926, "musicbrainz_id": "ae6595fb-a53c-340f-97a1-cff821300fec"},   # Doves - Lost Souls
            {"rank": 927, "musicbrainz_id": "88c59b55-200d-3ac1-beff-8eb99830807e"},   # U2 - All That You Can’t Leave Behind
            {"rank": 928, "musicbrainz_id": "c1117d6c-1d65-3321-a3de-530834adf338"},   # Ute Lemper - Punishing Kiss
            {"rank": 929, "musicbrainz_id": "271faeb3-fdd1-3ebb-80aa-97b3116e9341"},   # Björk - Vespertine
            {"rank": 930, "musicbrainz_id": "9def6672-e304-36f1-9d32-59ab846d1da8"},   # Destiny’s Child - Survivor
            {"rank": 931, "musicbrainz_id": "1974b728-bad0-3406-9863-5da1094ed243"},   # Drive‐By Truckers - Southern Rock Opera
            {"rank": 932, "musicbrainz_id": "4f9a9d35-b16d-3b7b-80d0-32b29683633f"},   # Gillian Welch - Time (The Revelator)
            {"rank": 933, "musicbrainz_id": "b0405d2a-5720-340a-bb56-4e135d031cc2"},   # Gorillaz - Gorillaz
            {"rank": 934, "musicbrainz_id": "1866c2af-03f2-3bb1-a61b-41f68951ee25"},   # Gotan Project - La revancha del tango
            {"rank": 935, "musicbrainz_id": "11ae8c9c-27c1-3308-9761-edb87c8f54ea"},   # Jay‐Z - The Blueprint
            {"rank": 936, "musicbrainz_id": "bca9280e-28b4-327f-8fe0-fd918579e486"},   # Radiohead - Amnesiac
            {"rank": 937, "musicbrainz_id": "95d72e72-55b2-3408-8d76-cce7abad3836"},   # Röyksopp - Melody A.M.
            {"rank": 938, "musicbrainz_id": "4c7d8cfb-0678-38a4-ac3b-8ff98705a6b5"},   # Ryan Adams - Gold
            {"rank": 939, "musicbrainz_id": "3a7abbe0-2134-34f3-ae51-811b783e0f26"},   # Silver Jews - Bright Flight
            {"rank": 940, "musicbrainz_id": "53463422-40a6-36d1-a637-43c1f233bbcf"},   # Super Furry Animals - Rings Around the World
            {"rank": 941, "musicbrainz_id": "34c62e23-de6c-36ba-afa0-8d91086d22c2"},   # The Beta Band - Hot Shots II
            {"rank": 942, "musicbrainz_id": "efea26d1-a016-30f6-b8e2-bc8c02336b0a"},   # The Strokes - Is This It
            {"rank": 943, "musicbrainz_id": "c5a0411f-374e-360d-9364-3ddec3007162"},   # The White Stripes - White Blood Cells
            {"rank": 944, "musicbrainz_id": "5f84e8b9-b8e5-3fbf-b514-0192a62d88b6"},   # Beck - Sea Change
            {"rank": 945, "musicbrainz_id": "d19453c0-cd72-3468-b110-0f898c111e5e"},   # Bruce Springsteen - The Rising
            {"rank": 946, "musicbrainz_id": "120c786d-a3b2-3c19-b4ff-2b7b3b4435bf"},   # Coldplay - A Rush of Blood to the Head
            {"rank": 947, "musicbrainz_id": "aca4ccc8-5d1b-361e-ab21-396b2c6d42d3"},   # Johnny Cash - American IV: The Man Comes Around
            {"rank": 948, "musicbrainz_id": "3ec846cc-e07a-3734-836c-822d10ab10d0"},   # Jurassic 5 - Power in Numbers
            {"rank": 949, "musicbrainz_id": "596090bc-cdfa-347e-96a5-d253848d3b37"},   # Missy Elliott - Under Construction
            {"rank": 950, "musicbrainz_id": "40716dae-d035-3e99-aded-581a1c811945"},   # Ms. Dynamite - A Little Deeper
            {"rank": 951, "musicbrainz_id": "6ccac9d2-22ed-33de-bd5d-f2aadcacf7f8"},   # Norah Jones - Come Away With Me
            {"rank": 952, "musicbrainz_id": "56d42e63-7052-325d-a46d-adf95ca55747"},   # The Bees - Sunshine Hit Me
            {"rank": 953, "musicbrainz_id": "1bc78730-eb94-311e-ab40-969c29619ef1"},   # The Coral - The Coral
            {"rank": 954, "musicbrainz_id": "91b37425-6d27-3cbc-b8a4-589e44cd968f"},   # Doves - The Last Broadcast
            {"rank": 955, "musicbrainz_id": "54b1ad4e-7e86-308d-b053-a0843f6abbdb"},   # The Flaming Lips - Yoshimi Battles the Pink Robots
            {"rank": 956, "musicbrainz_id": "98277141-0f63-3796-894a-11409d1377c4"},   # The Roots - Phrenology
            {"rank": 957, "musicbrainz_id": "95f2ba4b-2dd9-38d1-8158-a416a391489c"},   # Wilco - Yankee Hotel Foxtrot
            {"rank": 958, "musicbrainz_id": "01ac6115-0ea4-346d-b022-5bcde31c6264"},   # Dizzee Rascal - Boy in da Corner
            {"rank": 959, "musicbrainz_id": "8eecdf24-c5a4-3d74-8a81-80b59cd8e7aa"},   # Lightning Bolt - Wonderful Rainbow
            # {"rank": 960, "musicbrainz_id": None},   # NO MATCH: Outkast - Speakerboxxx/The Love Below (2003)
            {"rank": 961, "musicbrainz_id": "b226aaa9-f69a-3fd9-b31b-c3ada1ea2870"},   # Rufus Wainwright - Want One
            {"rank": 962, "musicbrainz_id": "605124dd-0f2a-382b-a8ba-720658c1fe45"},   # The Mars Volta - De‐Loused in the Comatorium
            {"rank": 963, "musicbrainz_id": "d85b9684-4277-3565-b89b-115c8b4b7fd3"},   # The White Stripes - Elephant
            {"rank": 964, "musicbrainz_id": "e8e2d824-dd32-3b24-9c7c-24619fbe86a9"},   # Yeah Yeah Yeahs - Fever to Tell
            {"rank": 965, "musicbrainz_id": "05affa96-5959-32da-8d75-1c9eb985ca59"},   # Arcade Fire - Funeral
            {"rank": 966, "musicbrainz_id": "4b2ee53c-6527-30e5-940c-c426a7a6f618"},   # Björk - Medúlla
            {"rank": 967, "musicbrainz_id": "9a839f47-ad2b-32bd-b794-b339d0b3b587"},   # Cee‐Lo Green - Cee‐Lo Green… Is the Soul Machine
            {"rank": 968, "musicbrainz_id": "964fe50c-8bb3-3086-98ac-88f92cbec56a"},   # Devendra Banhart - Rejoicing in the Hands
            {"rank": 969, "musicbrainz_id": "eac2b1f1-9ae8-43d6-94e5-ec8c20dcabd1"},   # Franz Ferdinand - Franz Ferdinand
            {"rank": 970, "musicbrainz_id": "de9bf827-a9b0-348b-a7c9-556c03c3fb07"},   # Green Day - American Idiot
            {"rank": 971, "musicbrainz_id": "8a01217e-6947-3927-a39b-6691104694f1"},   # Kanye West - The College Dropout
            {"rank": 972, "musicbrainz_id": "315cb93b-deab-3b3a-b3df-763060807feb"},   # Liars - They Were Wrong, So We Drowned
            {"rank": 973, "musicbrainz_id": "a7b797f2-7ada-30be-9d94-7b4687a3e450"},   # Morrissey - You Are the Quarry
            {"rank": 974, "musicbrainz_id": "78b95d1b-47b5-3247-a10f-c46318354e05"},   # Mylo - Destroy Rock & Roll
            # {"rank": 975, "musicbrainz_id": None},   # NO MATCH: Nick Cave & the Bad Seeds - Abattoir Blues/The Lyre Of Orpheus (2004)
            {"rank": 976, "musicbrainz_id": "75e20106-9ce2-3145-ad87-e4f17bea575c"},   # Ozomatli - Street Signs
            {"rank": 977, "musicbrainz_id": "8ce746e3-85f3-32b9-a8f9-b15942504549"},   # Rufus Wainwright - Want Two
            {"rank": 978, "musicbrainz_id": "9235cafc-3083-33c7-bfee-ed9f0828b6de"},   # Scissor Sisters - Scissor Sisters
            {"rank": 979, "musicbrainz_id": "cd30b700-b873-347d-a666-36e2790195fd"},   # The Icarus Line - Penance Soirée
            {"rank": 980, "musicbrainz_id": "e8c09b4e-33ae-368b-8f70-24b4e14fb9ad"},   # The Killers - Hot Fuss
            {"rank": 981, "musicbrainz_id": "606032a2-ec19-32ca-a7c9-17a32dea72ae"},   # The Streets - A Grand Don’t Come for Free
            # {"rank": 982, "musicbrainz_id": None},   # NO MATCH: TV on the Radio - Desperate Youths, Blood Thirsty Babes (2004)
            {"rank": 983, "musicbrainz_id": "63373d83-a96e-355c-aa44-837db92c2193"},   # Antony and the Johnsons - I Am a Bird Now
            {"rank": 984, "musicbrainz_id": "93b891c9-4fc4-3085-960e-5da4c7fe8113"},   # Common - Be
            {"rank": 985, "musicbrainz_id": "c16b9d8e-60e5-3947-a13f-cb9233138510"},   # Richard Hawley - Coles Corner
            {"rank": 986, "musicbrainz_id": "1fb75447-c513-38c4-ad8f-1bfc441aa74c"},   # Sufjan Stevens - Illinois
            {"rank": 987, "musicbrainz_id": "4d484e44-90eb-364a-8175-b9afe668a716"},   # Ali Farka Touré - Savane
            {"rank": 988, "musicbrainz_id": "6eac2e57-ee50-36f8-b0c4-c4c847a2c098"},   # Amy Winehouse - Back to Black
            {"rank": 989, "musicbrainz_id": "6c9c4985-3628-3070-b956-b538f30c9bea"},   # Arctic Monkeys - Whatever People Say I Am, That’s What I’m Not
            {"rank": 990, "musicbrainz_id": "909875a2-dced-346f-a341-b0c3bbd4b8b7"},   # Christina Aguilera - Back to Basics
            {"rank": 991, "musicbrainz_id": "67de538c-a1e0-39d0-91dd-c9d29e72e06c"},   # Ghostface Killah - Fishscale
            {"rank": 992, "musicbrainz_id": "34315f68-08a5-3637-8da7-deaad8f45514"},   # Joanna Newsom - Ys
            # {"rank": 993, "musicbrainz_id": None},   # NO MATCH: Lupe Fiasco - Lupe Fiasco's Food & Liqour (2006)
            {"rank": 994, "musicbrainz_id": "af2e8e23-e9c3-4e67-8ad8-66387c5898fd"},   # Muse - Black Holes and Revelations
            {"rank": 995, "musicbrainz_id": "c091b282-aa91-3bc0-9c95-938db1f1f930"},   # Arcade Fire - Neon Bible
            {"rank": 996, "musicbrainz_id": "2fedcb2d-c224-3a34-b9bc-d8f8e9bea4c4"},   # Justice - A Cross the Universe
            {"rank": 997, "musicbrainz_id": "5cbcdd9f-4b7d-3b3c-b9f2-6b0e75971157"},   # LCD Soundsystem - Sound of Silver
            {"rank": 998, "musicbrainz_id": "44261ea6-06cf-3fd3-a05c-42dee49c295a"},   # M.I.A. - Kala
            {"rank": 999, "musicbrainz_id": "6e335887-60ba-38f0-95af-fae7774336bf"},   # Radiohead - In Rainbows
            {"rank": 1000, "musicbrainz_id": "a2c5066c-eed0-374d-b259-59420f2cfa23"},   # The Good, the Bad & the Queen - The Good, the Bad & the Queen
            {"rank": 1001, "musicbrainz_id": "e46c2970-bc74-3f6e-add9-fcf8e87a5c4f"},   # Klaxons - Myths of the Near Future
        ],
    },
        # ------------------------------------------------------------------ #
    #  Arthur C. Clarke — Novels (publication order)                       #
    #  Populate hardcover_id from hardcover.app (numeric book ID in URL).  #
    # ------------------------------------------------------------------ #
    {
        "slug": "arthur_c_clarke_novels",
        "name": "Arthur C. Clarke — Novels",
        "icon": "🛰️",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            {"rank": 1, "hardcover_id": 140091},   # Arthur C. Clarke - Prelude to Space
            {"rank": 2, "hardcover_id": 132834},   # Arthur C. Clarke - The Sands of Mars
            {"rank": 3, "hardcover_id": 208343},   # Arthur C. Clarke - Islands in the Sky
            {"rank": 4, "hardcover_id": 595362},   # Arthur C. Clarke - Against the Fall of Night
            {"rank": 5, "hardcover_id": 184949},   # Arthur C. Clarke - Childhood's End
            {"rank": 6, "hardcover_id": 468156},   # Arthur C. Clarke - Earthlight
            {"rank": 7, "hardcover_id": 427323},   # Arthur C. Clarke - The City and the Stars
            {"rank": 8, "hardcover_id": 38240},   # Arthur C. Clarke - The Deep Range
            {"rank": 9, "hardcover_id": 457124},   # Arthur C. Clarke - A Fall of Moondust
            {"rank": 10, "hardcover_id": 359731},   # Arthur C. Clarke - Dolphin Island
            {"rank": 11, "hardcover_id": 919836},   # Arthur C. Clarke - Glide Path
            {"rank": 12, "hardcover_id": 374134},   # Arthur C. Clarke - 2001: A Space Odyssey
            {"rank": 13, "hardcover_id": 4720},   # Arthur C. Clarke - Rendezvous with Rama
            {"rank": 14, "hardcover_id": 384512},   # Arthur C. Clarke - Imperial Earth
            {"rank": 15, "hardcover_id": 14254},   # Arthur C. Clarke - The Fountains of Paradise
            {"rank": 16, "hardcover_id": 445066},   # Arthur C. Clarke - 2010: Odyssey Two
            {"rank": 17, "hardcover_id": 437937},   # Arthur C. Clarke - The Songs of Distant Earth
            {"rank": 18, "hardcover_id": 17728},   # Arthur C. Clarke - 2061: Odyssey Three
            {"rank": 19, "hardcover_id": 215563},   # Arthur C. Clarke - Cradle
            {"rank": 20, "hardcover_id": 445036},   # Arthur C. Clarke - Rama II
            {"rank": 21, "hardcover_id": 919790},   # Arthur C. Clarke - The Ghost from the Grand Banks
            {"rank": 22, "hardcover_id": 13293},   # Arthur C. Clarke - The Garden of Rama
            {"rank": 23, "hardcover_id": 330303},   # Arthur C. Clarke - The Hammer of God
            {"rank": 24, "hardcover_id": 324325},   # Arthur C. Clarke - Rama Revealed
            {"rank": 25, "hardcover_id": 919788},   # Arthur C. Clarke - Richter 10
            {"rank": 26, "hardcover_id": 39696},   # Arthur C. Clarke - 3001: The Final Odyssey
            {"rank": 27, "hardcover_id": 356520},   # Arthur C. Clarke - The Trigger
            {"rank": 28, "hardcover_id": 432794},   # Arthur C. Clarke - The Light of Other Days
            {"rank": 29, "hardcover_id": 446216},   # Arthur C. Clarke - Time's Eye
            {"rank": 30, "hardcover_id": 446085},   # Arthur C. Clarke - Sunstorm
            {"rank": 31, "hardcover_id": 385359},   # Arthur C. Clarke - Firstborn
            {"rank": 32, "hardcover_id": 270360},   # Arthur C. Clarke - The Last Theorem
        ],
    },

    # ------------------------------------------------------------------ #
    #  SF Masterworks (Gollancz/Millennium) — series order not preserved;  #
    #  "year" here is left None since this is a reprint series, not an     #
    #  award — sort/display by title or original pub year once resolved.  #
    #  NOTE: verified complete only through the Jan-2016 sfgateway.com     #
    #  checkpoint (138 titles below). Series continued to ~199 titles      #
    #  through 2025 — see "later additions, unverified" block at bottom    #
    #  for known but unconfirmed entries to check manually.               #
    #  Populate hardcover_id from hardcover.app (numeric book ID in URL).  #
    # ------------------------------------------------------------------ #
    {
        "slug": "sf_masterworks",
        "name": "SF Masterworks",
        "icon": "📖",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            {"rank": 1, "hardcover_id": 441091},   # George R. Stewart - Earth Abides
            {"rank": 2, "hardcover_id": 32296},   # Alfred Bester - The Demolished Man
            {"rank": 3, "hardcover_id": 267204},   # Ursula K. Le Guin - The Dispossessed
            {"rank": 4, "hardcover_id": 433144},   # Kurt Vonnegut - The Sirens of Titan
            {"rank": 5, "hardcover_id": 458016},   # Michael Moorcock - Behold the Man
            {"rank": 6, "hardcover_id": 457683},   # Frederik Pohl - Man Plus
            {"rank": 7, "hardcover_id": 84476},   # Brian W. Aldiss - Non-Stop
            {"rank": 8, "hardcover_id": 458284},   # Ward Moore - Bring the Jubilee
            {"rank": 9, "hardcover_id": 270051},   # Ursula K. Le Guin - The Lathe of Heaven
            {"rank": 10, "hardcover_id": 547019},   # John Sladek - The Complete Roderick
            {"rank": 11, "hardcover_id": 1343693},   # Michael Moorcock - The Dancers at the End of Time
            {"rank": 12, "hardcover_id": 373933},   # Frederik Pohl - The Space Merchants
            {"rank": 13, "hardcover_id": 427450},   # Larry Niven - Ringworld
            {"rank": 14, "hardcover_id": 484180},   # Geoff Ryman - The Child Garden
            {"rank": 15, "hardcover_id": 468386},   # Walter Tevis - Mockingbird
            {"rank": 16, "hardcover_id": 312460},   # Frank Herbert - Dune
            {"rank": 17, "hardcover_id": 1989646},   # Robert A. Heinlein - The Moon is a Harsh Mistress
            {"rank": 18, "hardcover_id": 427359},   # Alfred Bester - The Stars My Destination
            {"rank": 19, "hardcover_id": 482086},   # Cordwainer Smith - The Rediscovery of Man
            {"rank": 20, "hardcover_id": 97435},   # Frederik Pohl - Gateway
            {"rank": 21, "hardcover_id": 458243},   # Gene Wolfe - The Fifth Head of Cerberus
            {"rank": 22, "hardcover_id": 113324},   # James Blish - Cities in Flight
            {"rank": 23, "hardcover_id": 427389},   # Joe Haldeman - The Forever War
            {"rank": 24, "hardcover_id": 268150},   # Philip K. Dick - Do Androids Dream of Electric Sheep?
            {"rank": 25, "hardcover_id": 255573},   # Richard Matheson - I Am Legend
            {"rank": 26, "hardcover_id": 109204},   # Roger Zelazny - Lord of Light
            {"rank": 27, "hardcover_id": 430657},   # Samuel R. Delany - Babel-17
            {"rank": 28, "hardcover_id": 253601},   # Philip K. Dick - Ubik
            {"rank": 29, "hardcover_id": 3680},   # Philip K. Dick - The Three Stigmata of Palmer Eldritch
            {"rank": 30, "hardcover_id": 435385},   # Christopher Priest - Inverted World
            {"rank": 31, "hardcover_id": 341002},   # Philip K. Dick - Time Out Of Joint
            {"rank": 32, "hardcover_id": 150638},   # Philip K. Dick - The Simulacra
            {"rank": 33, "hardcover_id": 107110},   # Philip K. Dick - Flow My Tears, the Policeman Said
            {"rank": 34, "hardcover_id": 457364},   # Philip K. Dick - Valis
            {"rank": 35, "hardcover_id": 427315},   # Kurt Vonnegut - Cat's Cradle
            {"rank": 36, "hardcover_id": 184949},   # Arthur C. Clarke - Childhood's End
            {"rank": 37, "hardcover_id": 1152022},   # H. G. Wells - H. G. Wells : The Island of Doctor Moreau
            {"rank": 38, "hardcover_id": 69589},   # H. G. Wells - The Time Machine
            {"rank": 39, "hardcover_id": 428029},   # Samuel R. Delany - Dhalgren
            {"rank": 40, "hardcover_id": 771358},   # Brian W. Aldiss - Helliconia Spring
            {"rank": 41, "hardcover_id": 1192615},   # H. G. Wells - H.G. Wells Seven Novels, Complete & Unabridged The Time Machine, Island of Dr. Moreau, Invisible Man, First Men In The Moon, Food of the Gods, In the Days of the Comet and War of the Worlds
            {"rank": 42, "hardcover_id": 1070095},   # Jack Finney - The Body Snatchers
            {"rank": 43, "hardcover_id": 243617},   # Joanna Russ - The Female Man
            {"rank": 44, "hardcover_id": 68049},   # M.J. Engh - Arslan
            {"rank": 45, "hardcover_id": 461566},   # M. John Harrison - The Centauri Device
            {"rank": 46, "hardcover_id": 194655},   # Poul Anderson - Tau Zero
            {"rank": 47, "hardcover_id": 341721},   # William Gibson - The Difference Engine
            {"rank": 48, "hardcover_id": 427346},   # Christopher Priest - The Prestige
            {"rank": 49, "hardcover_id": 481950},   # Brian W. Aldiss - Greybeard
            {"rank": 50, "hardcover_id": 137617},   # Philip K. Dick - Martian Time-Slip
            {"rank": 51, "hardcover_id": 474644},   # Olaf Stapledon - Sirius
            {"rank": 52, "hardcover_id": 427460},   # Dan Simmons - Hyperion
            {"rank": 53, "hardcover_id": 427323},   # Arthur C. Clarke - The City and the Stars
            {"rank": 54, "hardcover_id": 373370},   # Clifford D. Simak - City
            {"rank": 55, "hardcover_id": 474595},   # Frank Herbert - Hellstrom's Hive
            {"rank": 56, "hardcover_id": 151204},   # William Tenn - Ofmen and monsters
            {"rank": 57, "hardcover_id": 458195},   # Gregory Benford - Timescape
            {"rank": 58, "hardcover_id": 458013},   # Keith Roberts - Pavane
            {"rank": 59, "hardcover_id": 458317},   # Robert Silverberg - Dying Inside
            {"rank": 60, "hardcover_id": 116508},   # Sheri S. Tepper - Grass
            {"rank": 61, "hardcover_id": 428012},   # Theodore Sturgeon - More Than Human
            {"rank": 62, "hardcover_id": 456904},   # Christopher Priest - The Affirmation
            {"rank": 63, "hardcover_id": 1400317},   # Karel Čapek - R.U.R. & War with the Newts
            {"rank": 64, "hardcover_id": 461477},   # Jack Vance - Emphyrio
            {"rank": 65, "hardcover_id": 439930},   # Olaf Stapledon - Star Maker
            {"rank": 66, "hardcover_id": 483040},   # Robert Silverberg - The Book of Skulls
            {"rank": 67, "hardcover_id": 300455},   # Cecelia Holland - Floating worlds
            {"rank": 68, "hardcover_id": 214074},   # Greg Bear - Blood Music
            {"rank": 69, "hardcover_id": 439979},   # Algis Budrys - Rogue Moon
            {"rank": 70, "hardcover_id": 435683},   # Harlan Ellison - Dangerous Visions
            {"rank": 71, "hardcover_id": 4720},   # Arthur C. Clarke - Rendezvous with Rama
            {"rank": 72, "hardcover_id": 19115},   # Greg Bear - Eon
            {"rank": 73, "hardcover_id": 88382},   # Olaf Stapledon - Odd John
            {"rank": 74, "hardcover_id": 14254},   # Arthur C. Clarke - The Fountains of Paradise
            {"rank": 75, "hardcover_id": 376843},   # Olaf Stapledon - Last and First Men
            {"rank": 76, "hardcover_id": 369986},   # Dan Simmons - The Fall of Hyperion
            {"rank": 77, "hardcover_id": 427798},   # Douglas Adams - The Hitchhiker's Guide to the Galaxy
            {"rank": 78, "hardcover_id": 243782},   # Kate Wilhelm - Where Late the Sweet Birds Sang
            {"rank": 79, "hardcover_id": 350457},   # Arkady Strugatsky - Roadside Picnic
            {"rank": 94, "hardcover_id": 1153086},   # George Turner - The Sea and Summer
            {"rank": 95, "hardcover_id": 429439},   # Sheri S. Tepper - The Gate to Women's Country
            {"rank": 96, "hardcover_id": 1133629},   # H. G. Wells - H.G. Wells Collection, Over 50 Works: The War of the Worlds, The Invisible Man, Time Machine, Island of Dr. Moreau, Little Wars, World Set Free, Tales of Space and Time, When the Sleeper Wakes & MORE!
            {"rank": 97, "hardcover_id": 581235},   # Walter M. Miller, Jr. - A Canticle for Leibowitz
            {"rank": 98, "hardcover_id": 216723},   # Connie Willis - To Say Nothing of the Dog
            {"rank": 99, "hardcover_id": 168465},   # Eric Frank Russell - Wasp
            {"rank": 100, "hardcover_id": 53731},   # Isaac Asimov - The Gods Themselves
            {"rank": 101, "hardcover_id": 2215277},   # James Morrow - This Is the Way the World Ends
            {"rank": 102, "hardcover_id": 1192615},   # H. G. Wells - H.G. Wells Seven Novels, Complete & Unabridged The Time Machine, Island of Dr. Moreau, Invisible Man, First Men In The Moon, Food of the Gods, In the Days of the Comet and War of the Worlds
            {"rank": 103, "hardcover_id": 469098},   # John Crowley - The Deep
            {"rank": 104, "hardcover_id": 938582},   # Connie Willis - Time is the Fire: The Best of Connie Willis
            {"rank": 105, "hardcover_id": 94217},   # Michael  Bishop - No Enemy But Time
            {"rank": 106, "hardcover_id": 332660},   # Alastair Reynolds - Revelation Space
            {"rank": 107, "hardcover_id": 215074},   # Robert A. Heinlein - Double Star
            {"rank": 108, "hardcover_id": 457124},   # Arthur C. Clarke - A Fall of Moondust
            {"rank": 109, "hardcover_id": 166526},   # Philip K. Dick - A Maze of Death
            {"rank": 110, "hardcover_id": 28354},   # Philip K. Dick - The Penultimate Truth
            {"rank": 111, "hardcover_id": 373733},   # Jack Womack - Random Acts of Senseless Violence
            {"rank": 112, "hardcover_id": 1021238},   # Michael Bishop - Transfigurations
            {"rank": 113, "hardcover_id": 384991},   # Douglas Adams - The Restaurant at the End of the Universe
            {"rank": 114, "hardcover_id": 278749},   # Robert A. Heinlein - The Door into Summer
            {"rank": 115, "hardcover_id": 375813},   # Douglas Adams - Life, the Universe and Everything
            {"rank": 116, "hardcover_id": 48953},   # Philip K. Dick - Dr Bloodmoney
            {"rank": 117, "hardcover_id": 784306},   # J. T. Reason - The human contribution
            {"rank": 118, "hardcover_id": 461438},   # Leigh Brackett - The Long Tomorrow
            {"rank": 119, "hardcover_id": 923782},   # Gottfried August Bürger - Leonora. A tale, translated and altered from the German ... by J. T. Stanley ... A new edition. [With a frontispiece and two vignettes engraved after designs by William Blake.] Ger.&Eng
            {"rank": 120, "hardcover_id": 46573},   # Frederik Pohl - Jem
            {"rank": 121, "hardcover_id": 457626},   # Richard Matheson - The Shrinking Man
            {"rank": 122, "hardcover_id": 469084},   # James Blish - A Case of Conscience
            {"rank": 123, "hardcover_id": 154457},   # James Tiptree Jr. - Her Smoke Rose Up Forever
            {"rank": 124, "hardcover_id": 152062},   # Philip K. Dick - A Scanner Darkly
            {"rank": 125, "hardcover_id": 234907},   # John Brunner - Stand on Zanzibar
            {"rank": 126, "hardcover_id": 474576},   # Hal Clement - Mission of Gravity
            {"rank": 127, "hardcover_id": 648866},   # Ursula K. Le Guin - The Word for World is Forest
            {"rank": 128, "hardcover_id": 522659},   # Arkady Strugatsky - Hard to Be a God
            {"rank": 129, "hardcover_id": 85029},   # Robert Silverberg - Downward to the Earth
            {"rank": 130, "hardcover_id": 469190},   # Jack Vance - Night Lamp
            {"rank": 131, "hardcover_id": 547252},   # Lucius Shepard - LIFE DURING WARTIME
            {"rank": 132, "hardcover_id": 547261},   # Walter M. Miller, Jr. - Dark Benediction
            {"rank": 133, "hardcover_id": 9878},   # Ursula K. Le Guin - The Wind's Twelve Quarters
            {"rank": 134, "hardcover_id": 1154397},   # George R.R. Martin - A Game of Thrones: The Story Continues The Complete Box Set of All 7 Books by Martin, George R. R. ( AUTHOR ) Jul-12-2012 Paperback
            {"rank": 135, "hardcover_id": 458254},   # Samuel R. Delany - Nova
            {"rank": 136, "hardcover_id": 428648},   # Walter Tevis - The Man Who Fell to Earth
            {"rank": 137, "hardcover_id": 381999},   # John Wyndham - The Day of the Triffids
            {"rank": 138, "hardcover_id": 427468},   # Vernor Vinge - A Fire Upon the Deep
        ],
    },
]
