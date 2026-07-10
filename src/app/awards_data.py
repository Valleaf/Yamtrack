"""Static award-winner fixtures used by the statistics awards-progress section.

Each entry in AWARDS describes one award category.  ``winners`` is a list of
per-year dicts.  The ID key name follows the pattern ``{source}_id``
(e.g. ``tmdb_id``, ``igdb_id``, ``mal_id``, ``hardcover_id``, ``bnf_id``).
``year`` is always the ceremony/award year.

TMDB IDs : https://www.themoviedb.org/movie/<id>
IGDB IDs : https://www.igdb.com/games/<slug>
MAL IDs  : https://myanimelist.net/manga/<id>
Hardcover: hardcover.app — look up each title, copy the numeric book ID from the URL
BnF IDs  : https://catalogue.bnf.fr/ark:/12148/<id>
"""

AWARDS = [
    # ------------------------------------------------------------------ #
    #  Oscar Best Picture  (ceremony year)                                 #
    # ------------------------------------------------------------------ #
    {
        "slug": "oscar_best_picture",
        "name": "Oscar Best Picture",
        "icon": "🏆",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2026, "tmdb_id": "1054867"},  # One Battle After Another
            {"year": 2025, "tmdb_id": "1064213"},  # Anora
            {"year": 2024, "tmdb_id": "872585"},   # Oppenheimer
            {"year": 2023, "tmdb_id": "545611"},   # Everything Everywhere All at Once
            {"year": 2022, "tmdb_id": "776503"},   # CODA
            {"year": 2021, "tmdb_id": "581734"},   # Nomadland
            {"year": 2020, "tmdb_id": "496243"},   # Parasite
            {"year": 2019, "tmdb_id": "490132"},   # Green Book
            {"year": 2018, "tmdb_id": "399055"},   # The Shape of Water
            {"year": 2017, "tmdb_id": "376867"},   # Moonlight
            {"year": 2016, "tmdb_id": "314365"},   # Spotlight
            {"year": 2015, "tmdb_id": "194662"},   # Birdman
            {"year": 2014, "tmdb_id": "76203"},    # 12 Years a Slave
            {"year": 2013, "tmdb_id": "68734"},    # Argo
            {"year": 2012, "tmdb_id": "74643"},    # The Artist
            {"year": 2011, "tmdb_id": "45269"},    # The King's Speech
            {"year": 2010, "tmdb_id": "12405"},    # Slumdog Millionaire
            {"year": 2009, "tmdb_id": "12162"},    # The Hurt Locker
            {"year": 2008, "tmdb_id": "6977"},     # No Country for Old Men
            {"year": 2007, "tmdb_id": "1422"},     # The Departed
            {"year": 2006, "tmdb_id": "1640"},     # Crash
            {"year": 2005, "tmdb_id": "70"},       # Million Dollar Baby
            {"year": 2004, "tmdb_id": "122"},      # The Lord of the Rings: The Return of the King
            {"year": 2003, "tmdb_id": "1574"},     # Chicago
            {"year": 2002, "tmdb_id": "453"},      # A Beautiful Mind
            {"year": 2001, "tmdb_id": "98"},       # Gladiator
            {"year": 2000, "tmdb_id": "14"},       # American Beauty
            {"year": 1999, "tmdb_id": "1934"},     # Shakespeare in Love
            {"year": 1998, "tmdb_id": "597"},      # Titanic
            {"year": 1997, "tmdb_id": "409"},      # The English Patient
            {"year": 1996, "tmdb_id": "197"},      # Braveheart
            {"year": 1995, "tmdb_id": "13"},       # Forrest Gump
            {"year": 1994, "tmdb_id": "424"},      # Schindler's List
            {"year": 1993, "tmdb_id": "33"},       # Unforgiven
            {"year": 1992, "tmdb_id": "274"},      # The Silence of the Lambs
            {"year": 1991, "tmdb_id": "581"},      # Dances with Wolves
            {"year": 1990, "tmdb_id": "403"},      # Driving Miss Daisy
            {"year": 1989, "tmdb_id": "380"},      # Rain Man
            {"year": 1988, "tmdb_id": "746"},      # The Last Emperor
            {"year": 1987, "tmdb_id": "792"},      # Platoon
            {"year": 1986, "tmdb_id": "606"},      # Out of Africa
            {"year": 1985, "tmdb_id": "279"},      # Amadeus
            {"year": 1984, "tmdb_id": "11050"},    # Terms of Endearment
            {"year": 1983, "tmdb_id": "783"},      # Gandhi
            {"year": 1982, "tmdb_id": "9443"},     # Chariots of Fire
            {"year": 1981, "tmdb_id": "16619"},    # Ordinary People
            {"year": 1980, "tmdb_id": "12102"},    # Kramer vs. Kramer
            {"year": 1979, "tmdb_id": "11778"},    # The Deer Hunter
            {"year": 1978, "tmdb_id": "703"},      # Annie Hall
            {"year": 1977, "tmdb_id": "1366"},     # Rocky
            {"year": 1976, "tmdb_id": "510"},      # One Flew Over the Cuckoo's Nest
            {"year": 1975, "tmdb_id": "240"},      # The Godfather Part II
            {"year": 1974, "tmdb_id": "9277"},     # The Sting
            {"year": 1973, "tmdb_id": "238"},      # The Godfather
            {"year": 1972, "tmdb_id": "1051"},     # The French Connection
            {"year": 1971, "tmdb_id": "11202"},    # Patton
            {"year": 1970, "tmdb_id": "3116"},     # Midnight Cowboy
            {"year": 1969, "tmdb_id": "17917"},    # Oliver!
            {"year": 1968, "tmdb_id": "10633"},    # In the Heat of the Night
            {"year": 1967, "tmdb_id": "874"},      # A Man for All Seasons
            {"year": 1966, "tmdb_id": "15121"},    # The Sound of Music
            {"year": 1965, "tmdb_id": "11113"},    # My Fair Lady
            {"year": 1964, "tmdb_id": "5769"},     # Tom Jones
            {"year": 1963, "tmdb_id": "947"},      # Lawrence of Arabia
            {"year": 1962, "tmdb_id": "1725"},     # West Side Story
            {"year": 1961, "tmdb_id": "284"},      # The Apartment
            {"year": 1960, "tmdb_id": "665"},      # Ben-Hur
            {"year": 1959, "tmdb_id": "17281"},    # Gigi
            {"year": 1958, "tmdb_id": "826"},      # The Bridge on the River Kwai
            {"year": 1957, "tmdb_id": "2897"},     # Around the World in 80 Days
            {"year": 1956, "tmdb_id": "15919"},    # Marty
            {"year": 1955, "tmdb_id": "654"},      # On the Waterfront
            {"year": 1954, "tmdb_id": "11426"},    # From Here to Eternity
            {"year": 1953, "tmdb_id": "27191"},    # The Greatest Show on Earth
            {"year": 1952, "tmdb_id": "2769"},     # An American in Paris
            {"year": 1951, "tmdb_id": "705"},      # All About Eve
            {"year": 1950, "tmdb_id": "25430"},    # All the King's Men
            {"year": 1949, "tmdb_id": "23383"},    # Hamlet
            {"year": 1948, "tmdb_id": "33667"},    # Gentleman's Agreement
            {"year": 1947, "tmdb_id": "887"},      # The Best Years of Our Lives
            {"year": 1946, "tmdb_id": "28580"},    # The Lost Weekend
            {"year": 1945, "tmdb_id": "17661"},    # Going My Way
            {"year": 1944, "tmdb_id": "289"},      # Casablanca
            {"year": 1943, "tmdb_id": "27367"},    # Mrs. Miniver
            {"year": 1942, "tmdb_id": "43266"},    # How Green Was My Valley
            {"year": 1941, "tmdb_id": "223"},      # Rebecca
            {"year": 1940, "tmdb_id": "770"},      # Gone with the Wind
            {"year": 1939, "tmdb_id": "34106"},    # You Can't Take It with You
            {"year": 1938, "tmdb_id": "43278"},    # The Life of Emile Zola
            {"year": 1937, "tmdb_id": "43277"},    # The Great Ziegfeld
            {"year": 1936, "tmdb_id": "12311"},    # Mutiny on the Bounty
            {"year": 1935, "tmdb_id": "3078"},     # It Happened One Night
            {"year": 1934, "tmdb_id": "56164"},    # Cavalcade
            {"year": 1933, "tmdb_id": "33680"},    # Grand Hotel
            {"year": 1932, "tmdb_id": "42861"},    # Cimarron
            {"year": 1931, "tmdb_id": "143"},      # All Quiet on the Western Front
            {"year": 1930, "tmdb_id": "65203"},    # The Broadway Melody
            {"year": 1929, "tmdb_id": "28966"}    # Wings
        ],
    },

    # ------------------------------------------------------------------ #
    #  Cannes Palme d'Or  (festival year)                                  #
    # ------------------------------------------------------------------ #
    {
        "slug": "palme_dor",
        "name": "Palme d'Or",
        "icon": "🌿",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1064213"},   # Anora
            {"year": 2023, "tmdb_id": "1011985"},   # Anatomy of a Fall
            {"year": 2022, "tmdb_id": "747188"},    # Triangle of Sadness
            {"year": 2021, "tmdb_id": "788183"},    # Titane
            {"year": 2019, "tmdb_id": "496243"},    # Parasite
            {"year": 2018, "tmdb_id": "517623"},    # Shoplifters
            {"year": 2017, "tmdb_id": "397645"},    # The Square
            {"year": 2016, "tmdb_id": "394044"},    # I, Daniel Blake
            {"year": 2015, "tmdb_id": "320793"},    # Dheepan
            {"year": 2014, "tmdb_id": "253236"},    # Winter Sleep
            {"year": 2013, "tmdb_id": "154226"},    # Blue Is the Warmest Color
            {"year": 2012, "tmdb_id": "103663"},    # Amour
            {"year": 2011, "tmdb_id": "75612"},     # The Tree of Life
            {"year": 2010, "tmdb_id": "60545"},     # Uncle Boonmee Who Can Recall His Past Lives
            {"year": 2009, "tmdb_id": "18491"},     # The White Ribbon
            {"year": 2008, "tmdb_id": "19823"},     # The Class (Entre les murs)
            {"year": 2007, "tmdb_id": "12446"},     # 4 Months, 3 Weeks and 2 Days
            {"year": 2006, "tmdb_id": "4813"},      # The Wind That Shakes the Barley
            {"year": 2005, "tmdb_id": "13528"},     # L'Enfant
            {"year": 2004, "tmdb_id": "9614"},      # Fahrenheit 9/11
            {"year": 2003, "tmdb_id": "11832"},     # Elephant
            {"year": 2002, "tmdb_id": "1128"},      # The Pianist
            {"year": 2000, "tmdb_id": "289"},       # Dancer in the Dark
            {"year": 1999, "tmdb_id": "37232"},     # Rosetta
            {"year": 1994, "tmdb_id": "680"},       # Pulp Fiction
            {"year": 1993, "tmdb_id": "9816"},      # Farewell My Concubine (co-winner)
            {"year": 1993, "tmdb_id": "397"},       # The Piano (co-winner)
            {"year": 1991, "tmdb_id": "13823"},     # Barton Fink
            {"year": 1989, "tmdb_id": "9561"},      # sex, lies, and videotape
            {"year": 1984, "tmdb_id": "11252"},     # Paris, Texas
        ],
    },

    # ------------------------------------------------------------------ #
    #  Venice Golden Lion  (festival year)                                 #
    # ------------------------------------------------------------------ #
    {
        "slug": "golden_lion",
        "name": "Golden Lion",
        "icon": "🦁",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2023, "tmdb_id": "792307"},    # Poor Things
            {"year": 2020, "tmdb_id": "581726"},    # Nomadland
            {"year": 2019, "tmdb_id": "475557"},    # Joker
            {"year": 2018, "tmdb_id": "481852"},    # Roma
            {"year": 2017, "tmdb_id": "399055"},    # The Shape of Water
            {"year": 2010, "tmdb_id": "45215"},     # Somewhere
            {"year": 2008, "tmdb_id": "13380"},     # The Wrestler
            {"year": 2007, "tmdb_id": "5408"},      # Lust, Caution
            {"year": 2005, "tmdb_id": "324"},       # Brokeback Mountain
            {"year": 2004, "tmdb_id": "9736"},      # Vera Drake
            {"year": 2003, "tmdb_id": "9567"},      # The Return
        ],
    },

    # ------------------------------------------------------------------ #
    #  Berlin Golden Bear  (festival year, February)                       #
    # ------------------------------------------------------------------ #
    {
        "slug": "golden_bear",
        "name": "Golden Bear",
        "icon": "🐻",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2011, "tmdb_id": "72096"},     # A Separation
            {"year": 2008, "tmdb_id": "7555"},      # Elite Squad (Tropa de Elite)
            {"year": 2004, "tmdb_id": "11509"},     # Head-On (Gegen die Wand)
            {"year": 2002, "tmdb_id": "129"},       # Spirited Away (co-winner)
            {"year": 2000, "tmdb_id": "17044"},     # Magnolia
        ],
    },

    # ------------------------------------------------------------------ #
    #  BAFTA Best Film  (ceremony year, February)                          #
    # ------------------------------------------------------------------ #
    {
        "slug": "bafta_best_film",
        "name": "BAFTA Best Film",
        "icon": "🎭",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "872585"},    # Oppenheimer
            {"year": 2023, "tmdb_id": "843047"},    # All Quiet on the Western Front (2022)
            {"year": 2022, "tmdb_id": "754609"},    # The Power of the Dog
            {"year": 2021, "tmdb_id": "581726"},    # Nomadland
            {"year": 2020, "tmdb_id": "530915"},    # 1917
            {"year": 2019, "tmdb_id": "481852"},    # Roma
            {"year": 2018, "tmdb_id": "359940"},    # Three Billboards Outside Ebbing, Missouri
            {"year": 2017, "tmdb_id": "313369"},    # La La Land
            {"year": 2016, "tmdb_id": "281957"},    # The Revenant
            {"year": 2015, "tmdb_id": "209112"},    # Boyhood
            {"year": 2014, "tmdb_id": "76203"},     # 12 Years a Slave
            {"year": 2013, "tmdb_id": "68721"},     # Argo
            {"year": 2012, "tmdb_id": "74643"},     # The Artist
            {"year": 2011, "tmdb_id": "45269"},     # The King's Speech
            {"year": 2010, "tmdb_id": "12162"},     # The Hurt Locker
            {"year": 2009, "tmdb_id": "12405"},     # Slumdog Millionaire
            {"year": 2008, "tmdb_id": "16320"},     # Atonement
            {"year": 2007, "tmdb_id": "1633"},      # The Queen
            {"year": 2006, "tmdb_id": "324"},       # Brokeback Mountain
            {"year": 2005, "tmdb_id": "11012"},     # The Aviator
            {"year": 2004, "tmdb_id": "122"},       # The Lord of the Rings: The Return of the King
            {"year": 2003, "tmdb_id": "1128"},      # The Pianist
            {"year": 2001, "tmdb_id": "98"},        # Gladiator
            {"year": 2000, "tmdb_id": "14"},        # American Beauty
        ],
    },

    # ------------------------------------------------------------------ #
    #  The Game Awards — Game of the Year  (since inaugural 2014)          #
    # ------------------------------------------------------------------ #
    {
        "slug": "game_awards_goty",
        "name": "Game Awards GOTY",
        "icon": "🎮",
        "media_type": "game",
        "source": "igdb",
        "winners": [
            {"year": 2024, "igdb_id": "348663"},    # Astro Bot
            {"year": 2023, "igdb_id": "119133"},    # Baldur's Gate 3
            {"year": 2022, "igdb_id": "119171"},    # Elden Ring
            {"year": 2021, "igdb_id": "134597"},    # It Takes Two
            {"year": 2020, "igdb_id": "103287"},    # The Last of Us Part II
            {"year": 2019, "igdb_id": "101204"},    # Sekiro: Shadows Die Twice
            {"year": 2018, "igdb_id": "38408"},     # God of War (2018)
            {"year": 2017, "igdb_id": "7346"},      # The Legend of Zelda: Breath of the Wild
            {"year": 2016, "igdb_id": "11989"},     # Overwatch
            {"year": 2015, "igdb_id": "1942"},      # The Witcher 3: Wild Hunt
            {"year": 2014, "igdb_id": "1708"},      # Dragon Age: Inquisition
        ],
    },

    # ------------------------------------------------------------------ #
    #  DICE Game of the Year  (ceremony early next year, game release year) #
    # ------------------------------------------------------------------ #
    {
        "slug": "dice_goty",
        "name": "DICE Game of the Year",
        "icon": "🎲",
        "media_type": "game",
        "source": "igdb",
        "winners": [
            {"year": 2023, "igdb_id": "119133"},    # Baldur's Gate 3
            {"year": 2022, "igdb_id": "119171"},    # Elden Ring
            {"year": 2021, "igdb_id": "134597"},    # It Takes Two
            {"year": 2018, "igdb_id": "38408"},     # God of War (2018)
            {"year": 2017, "igdb_id": "7346"},      # The Legend of Zelda: Breath of the Wild
            {"year": 2015, "igdb_id": "1942"},      # The Witcher 3: Wild Hunt
            {"year": 2014, "igdb_id": "1708"},      # Dragon Age: Inquisition
        ],
    },

    # ------------------------------------------------------------------ #
    #  Golden Joystick — Ultimate Game of the Year                         #
    # ------------------------------------------------------------------ #
    {
        "slug": "golden_joystick_goty",
        "name": "Golden Joystick UGOTY",
        "icon": "🕹️",
        "media_type": "game",
        "source": "igdb",
        "winners": [
            {"year": 2024, "igdb_id": "348663"},    # Astro Bot
            {"year": 2023, "igdb_id": "119133"},    # Baldur's Gate 3
            {"year": 2022, "igdb_id": "119171"},    # Elden Ring
            {"year": 2021, "igdb_id": "134597"},    # It Takes Two
            {"year": 2020, "igdb_id": "103287"},    # The Last of Us Part II
            {"year": 2018, "igdb_id": "38408"},     # God of War (2018)
            {"year": 2017, "igdb_id": "7346"},      # The Legend of Zelda: Breath of the Wild
            {"year": 2016, "igdb_id": "11989"},     # Overwatch
            {"year": 2015, "igdb_id": "1942"},      # The Witcher 3: Wild Hunt
        ],
    },

    # ------------------------------------------------------------------ #
    #  Hugo Award — Best Novel  (Worldcon year)                            #
    #  Populate hardcover_id from hardcover.app (numeric book ID in URL).  #
    # ------------------------------------------------------------------ #
    {
        "slug": "hugo_best_novel",
        "name": "Hugo Award — Best Novel",
        "icon": "🚀",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            # {"year": 2024, "hardcover_id": None},  # Some Desperate Glory — Emily Tesh
            # {"year": 2022, "hardcover_id": None},  # A Desolation Called Peace — Arkady Martine
            # {"year": 2020, "hardcover_id": None},  # A Memory Called Empire — Arkady Martine
            # {"year": 2019, "hardcover_id": None},  # The Calculating Stars — Mary Robinette Kowal
            # {"year": 2018, "hardcover_id": None},  # The Stone Sky — N.K. Jemisin
            # {"year": 2017, "hardcover_id": None},  # The Obelisk Gate — N.K. Jemisin
            # {"year": 2016, "hardcover_id": None},  # The Fifth Season — N.K. Jemisin
            # {"year": 2015, "hardcover_id": None},  # The Three-Body Problem — Liu Cixin
            # {"year": 2014, "hardcover_id": None},  # Ancillary Justice — Ann Leckie
            # {"year": 2013, "hardcover_id": None},  # Redshirts — John Scalzi
            # {"year": 2009, "hardcover_id": None},  # The Graveyard Book — Neil Gaiman
        ],
    },

    # ------------------------------------------------------------------ #
    #  Nebula Award — Best Novel                                           #
    # ------------------------------------------------------------------ #
    {
        "slug": "nebula_best_novel",
        "name": "Nebula Award — Best Novel",
        "icon": "⭐",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            # {"year": 2023, "hardcover_id": None},  # The Spare Man — Mary Robinette Kowal
            # {"year": 2022, "hardcover_id": None},  # A Psalm for the Wild-Built — Becky Chambers
            # {"year": 2019, "hardcover_id": None},  # A Memory Called Empire — Arkady Martine
            # {"year": 2018, "hardcover_id": None},  # The Calculating Stars — Mary Robinette Kowal
            # {"year": 2015, "hardcover_id": None},  # Uprooted — Naomi Novik
            # {"year": 2014, "hardcover_id": None},  # Annihilation — Jeff VanderMeer
        ],
    },

    # ------------------------------------------------------------------ #
    #  World Fantasy Award — Best Novel                                    #
    # ------------------------------------------------------------------ #
    {
        "slug": "world_fantasy_best_novel",
        "name": "World Fantasy Award — Best Novel",
        "icon": "🐉",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            # {"year": 2023, "hardcover_id": None},  # The Spare Man
            # {"year": 2020, "hardcover_id": None},  # The Book of the Most Precious Substance — Sara Gran
            # {"year": 2015, "hardcover_id": None},  # The Goblin Emperor — Katherine Addison
            # {"year": 2011, "hardcover_id": None},  # The Habitation of the Blessed — Catherynne Valente
        ],
    },

    # ------------------------------------------------------------------ #
    #  Booker Prize  (award year)                                          #
    # ------------------------------------------------------------------ #
    {
        "slug": "booker_prize",
        "name": "Booker Prize",
        "icon": "📚",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            # {"year": 2024, "hardcover_id": None},  # James — Percival Everett
            # {"year": 2023, "hardcover_id": None},  # Prophet Song — Paul Lynch
            # {"year": 2022, "hardcover_id": None},  # The Seven Moons of Maali Almeida — Shehan Karunatilaka
            # {"year": 2021, "hardcover_id": None},  # The Promise — Damon Galgut
            # {"year": 2020, "hardcover_id": None},  # Shuggie Bain — Douglas Stuart
            # {"year": 2019, "hardcover_id": None},  # The Testaments — Margaret Atwood
            # {"year": 2017, "hardcover_id": None},  # Lincoln in the Bardo — George Saunders
            # {"year": 2009, "hardcover_id": None},  # Wolf Hall — Hilary Mantel
            # {"year": 2002, "hardcover_id": None},  # Life of Pi — Yann Martel
        ],
    },

    # ------------------------------------------------------------------ #
    #  Pulitzer Prize — Fiction  (award year)                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "pulitzer_fiction",
        "name": "Pulitzer Prize — Fiction",
        "icon": "🗞️",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            # {"year": 2024, "hardcover_id": None},  # James — Percival Everett
            # {"year": 2022, "hardcover_id": None},  # The Netanyahus — Joshua Cohen
            # {"year": 2020, "hardcover_id": None},  # The Nickel Boys — Colson Whitehead
            # {"year": 2017, "hardcover_id": None},  # The Underground Railroad — Colson Whitehead
            # {"year": 2016, "hardcover_id": None},  # The Sympathizer — Viet Thanh Nguyen
        ],
    },

    # ------------------------------------------------------------------ #
    #  National Book Award — Fiction  (award year, November)              #
    # ------------------------------------------------------------------ #
    {
        "slug": "national_book_award_fiction",
        "name": "National Book Award — Fiction",
        "icon": "🏅",
        "media_type": "book",
        "source": "hardcover",
        "winners": [
            # {"year": 2023, "hardcover_id": None},  # The Vaster Wilds — Lauren Groff
            # {"year": 2022, "hardcover_id": None},  # Trust — Hernan Diaz
            # {"year": 2020, "hardcover_id": None},  # Deacon King Kong — James McBride
            # {"year": 2018, "hardcover_id": None},  # The Friend — Sigrid Nunez
        ],
    },

    # ------------------------------------------------------------------ #
    #  Manga Taisho  (award year, spring ceremony)                         #
    #  Source: MAL manga IDs  (myanimelist.net/manga/<id>)                 #
    # ------------------------------------------------------------------ #
    {
        "slug": "manga_taisho",
        "name": "Manga Taisho",
        "icon": "🎌",
        "media_type": "manga",
        "source": "mal",
        "winners": [
            {"year": 2012, "mal_id": "23390"},      # Shingeki no Kyojin (Attack on Titan)
            {"year": 2009, "mal_id": "104"},        # Yotsuba&!
            # {"year": 2010, "mal_id": None},        # Otoyomegatari (Bride's Story) — look up MAL ID
            # {"year": 2013, "mal_id": None},        # Gin no Saji (Silver Spoon)
            # {"year": 2015, "mal_id": None},        # Dungeon Meshi (Delicious in Dungeon)
        ],
    },

    # ------------------------------------------------------------------ #
    #  Tezuka Osamu Cultural Prize — Grand Prize                           #
    #  Source: MAL manga IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "tezuka_cultural_grand_prize",
        "name": "Tezuka Osamu Cultural Prize",
        "icon": "✒️",
        "media_type": "manga",
        "source": "mal",
        "winners": [
            {"year": 2003, "mal_id": "1"},          # Monster — Naoki Urasawa
            {"year": 2002, "mal_id": "1357"},       # Vagabond — Takehiko Inoue
            # Add earlier/later winners with MAL IDs from myanimelist.net/manga/<id>
        ],
    },

    # ------------------------------------------------------------------ #
    #  Shogakukan Manga Award — General Category                           #
    #  Source: MAL manga IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "shogakukan_manga_award",
        "name": "Shogakukan Manga Award",
        "icon": "📕",
        "media_type": "manga",
        "source": "mal",
        "winners": [
            {"year": 2006, "mal_id": "47"},         # 20th Century Boys — Naoki Urasawa
            {"year": 2002, "mal_id": "1357"},       # Vagabond — Takehiko Inoue
            # {"year": 1997, "mal_id": "2"},         # Berserk — Kentaro Miura (verify year)
            # Add others with MAL IDs from myanimelist.net/manga/<id>
        ],
    },

    # ------------------------------------------------------------------ #
    #  Angoulême Fauve d'Or  (festival year, January)                      #
    #  Source: BnF ARK IDs  (catalogue.bnf.fr/ark:/12148/<id>)            #
    # ------------------------------------------------------------------ #
    {
        "slug": "angouleme_fauve_dor",
        "name": "Angoulême Fauve d'Or",
        "icon": "🐯",
        "media_type": "comic",
        "source": "bnf",
        "winners": [
            # {"year": 2024, "bnf_id": None},   # Ici (Here) — Richard McGuire
            # {"year": 2023, "bnf_id": None},   # La Carte Blanche — Blandine Le Callet
            # {"year": 2022, "bnf_id": None},   # Blanc Autour — Wilfrid Lupano & Virginie Berthemet
            # {"year": 2019, "bnf_id": None},   # La Légèreté — Catherine Meurisse
            # Add BnF ARK IDs from catalogue.bnf.fr
        ],
    },

    # ------------------------------------------------------------------ #
    #  César Award — Best Film  (Meilleur film)                            #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "cesar_best_film",
        "name": "César Best Film",
        "icon": "🇫🇷",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "929590"},    # Anatomy of a Fall — Justine Triet
            {"year": 2023, "tmdb_id": "785084"},    # The Quiet Son — Léonor Serraille
            {"year": 2022, "tmdb_id": "599117"},    # Illusions Perdues — Xavier Giannoli
            {"year": 2021, "tmdb_id": "576845"},    # De leur vivant — Emmanuelle Bercot
            {"year": 2020, "tmdb_id": "503919"},    # Les Misérables — Ladj Ly
            {"year": 2019, "tmdb_id": "426320"},    # Jusqu'à la garde — Xavier Legrand
            {"year": 2018, "tmdb_id": "413232"},    # 120 Battements par minute — Robin Campillo
            {"year": 2017, "tmdb_id": "376660"},    # Elle — Paul Verhoeven
            {"year": 2016, "tmdb_id": "283566"},    # La Loi du marché — Stéphane Brizé
            {"year": 2015, "tmdb_id": "246655"},    # Timbuktu — Abderrahmane Sissako
            {"year": 2014, "tmdb_id": "209263"},    # La vie d'Adèle — Abdellatif Kechiche
            {"year": 2013, "tmdb_id": "87736"},     # Amour — Michael Haneke
            {"year": 2012, "tmdb_id": "62362"},     # The Artist — Michel Hazanavicius
            {"year": 2011, "tmdb_id": "57799"},     # Des hommes et des dieux — Xavier Beauvois
            {"year": 2010, "tmdb_id": "24753"},     # Un prophète — Jacques Audiard
            # Add older César Best Film winners with TMDB IDs from themoviedb.org
        ],
    },

    # ------------------------------------------------------------------ #
    #  Cannes — Prix du Jury / Grand Prix  (runner-up awards)             #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "cannes_grand_prix",
        "name": "Cannes Grand Prix",
        "icon": "🌴",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1118031"},   # All We Imagine as Light — Payal Kapadia
            {"year": 2023, "tmdb_id": "975902"},    # The Zone of Interest — Jonathan Glazer (verify — won Jury Prize, not Grand Prix)
            {"year": 2022, "tmdb_id": "815246"},    # Stars at Noon — Claire Denis
            {"year": 2021, "tmdb_id": "681660"},    # A Hero — Asghar Farhadi
            {"year": 2019, "tmdb_id": "505571"},    # Atlantics — Mati Diop
            {"year": 2018, "tmdb_id": "458818"},    # Capernaum — Nadine Labaki
            {"year": 2017, "tmdb_id": "413232"},    # BPM (Beats per Minute) — Robin Campillo (verify)
            # Add others from fr.wikipedia.org/wiki/Grand_Prix_(festival_de_Cannes)
        ],
    },

    # ------------------------------------------------------------------ #
    #  Cannes — Un Certain Regard: Palme d'Or UCR                         #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "cannes_un_certain_regard",
        "name": "Cannes Un Certain Regard",
        "icon": "👁️",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1209290"},   # Armand — Halfdan Ullmann Tøndel
            {"year": 2023, "tmdb_id": "878783"},    # How to Have Sex — Molly Manning Walker
            {"year": 2022, "tmdb_id": "817758"},    # The Stranger — Thomas M. Wright (verify)
            {"year": 2019, "tmdb_id": "560197"},    # Bull — Annie Silverstein (verify exact UCR winner)
            # Add others from en.wikipedia.org/wiki/Un_Certain_Regard
        ],
    },

    # ------------------------------------------------------------------ #
    #  Sundance Film Festival — Grand Jury Prize (US Dramatic)             #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "sundance_grand_jury",
        "name": "Sundance Grand Jury Prize",
        "icon": "🌄",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1046193"},   # A New Kind of Wilderness — Camilla Nielsson (verify — documentary?)
            {"year": 2023, "tmdb_id": "869626"},    # Passages — Ira Sachs (verify)
            {"year": 2022, "tmdb_id": "818680"},    # Emergency — Carey Williams
            {"year": 2021, "tmdb_id": "614278"},    # CODA — Sian Heder
            {"year": 2020, "tmdb_id": "531876"},    # Minari — Lee Isaac Chung
            {"year": 2019, "tmdb_id": "503907"},    # Clemency — Chinonye Chukwu
            {"year": 2018, "tmdb_id": "433680"},    # Burden — Andrew Heckler
            {"year": 2017, "tmdb_id": "399174"},    # I Don't Feel at Home in This World Anymore — Macon Blair
            # Add others from en.wikipedia.org/wiki/Sundance_Film_Festival_Award_for_Grand_Jury_Prize
        ],
    },

    # ------------------------------------------------------------------ #
    #  BAFTA — Best Film  (British Academy Film Awards)                    #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "bafta_best_film",
        "name": "BAFTA Best Film",
        "icon": "🎭",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "872585"},    # Oppenheimer — Christopher Nolan
            {"year": 2023, "tmdb_id": "674324"},    # The Banshees of Inisherin — Martin McDonagh (verify)
            {"year": 2022, "tmdb_id": "763215"},    # Belfast — Kenneth Branagh
            {"year": 2021, "tmdb_id": "581389"},    # Nomadland — Chloé Zhao
            {"year": 2020, "tmdb_id": "503924"},    # 1917 — Sam Mendes
            {"year": 2019, "tmdb_id": "505979"},    # Roma — Alfonso Cuarón
            {"year": 2018, "tmdb_id": "399055"},    # Three Billboards Outside Ebbing, Missouri — Martin McDonagh
            {"year": 2017, "tmdb_id": "376867"},    # La La Land — Damien Chazelle
            {"year": 2016, "tmdb_id": "264644"},    # The Revenant — Alejandro González Iñárritu
            {"year": 2015, "tmdb_id": "205596"},    # Boyhood — Richard Linklater
            {"year": 2014, "tmdb_id": "138843"},    # 12 Years a Slave — Steve McQueen
            {"year": 2013, "tmdb_id": "120467"},    # Argo — Ben Affleck
            {"year": 2012, "tmdb_id": "62362"},     # The Artist — Michel Hazanavicius
            {"year": 2011, "tmdb_id": "45269"},     # The King's Speech — Tom Hooper
            {"year": 2010, "tmdb_id": "1731"},      # The Hurt Locker — Kathryn Bigelow
            # Add older winners from en.wikipedia.org/wiki/BAFTA_Award_for_Best_Film
        ],
    },

    # ------------------------------------------------------------------ #
    #  Berlin International Film Festival — Special Jury Prize             #
    #  (Jury Grand Prix / Silver Bear Jury Prize since 2021 rebrand)       #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "berlinale_jury_grand_prix",
        "name": "Berlinale Jury Grand Prix",
        "icon": "🐻",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1071215"},   # Who Do I Belong To — Meryam Joobeur
            {"year": 2023, "tmdb_id": "961396"},    # Sur l'Adamant — Nicolas Philibert
            {"year": 2022, "tmdb_id": "785154"},    # A Piece of Sky — Michael Koch (verify)
            {"year": 2021, "tmdb_id": "628293"},    # Forest — Sheryl Moller (verify exact winner)
            # Add others from en.wikipedia.org/wiki/Silver_Bear_Jury_Prize
        ],
    },

    # ------------------------------------------------------------------ #
    #  Venice Film Festival — Grand Jury Prize (Silver Lion)               #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "venice_grand_jury",
        "name": "Venice Grand Jury Prize",
        "icon": "🦁",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1163126"},   # April — Dea Kulumbegashvili (verify)
            {"year": 2023, "tmdb_id": "961268"},    # Evil Does Not Exist — Ryusuke Hamaguchi
            {"year": 2022, "tmdb_id": "879499"},    # Saint Omer — Alice Diop
            {"year": 2021, "tmdb_id": "644124"},    # Il buco — Michelangelo Frammartino
            {"year": 2019, "tmdb_id": "544401"},    # J'accuse (An Officer and a Spy) — Roman Polanski (verify)
            # Add others from en.wikipedia.org/wiki/Silver_Lion_for_Grand_Jury_Prize
        ],
    },

    # ------------------------------------------------------------------ #
    #  European Film Awards — Best European Film                           #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "european_film_award",
        "name": "European Film Award",
        "icon": "🌍",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "929590"},    # Anatomy of a Fall — Justine Triet
            {"year": 2023, "tmdb_id": "840430"},    # The Zone of Interest — Jonathan Glazer
            {"year": 2022, "tmdb_id": "669000"},    # Close — Lukas Dhont
            {"year": 2021, "tmdb_id": "696374"},    # The Hand of God — Paolo Sorrentino
            {"year": 2020, "tmdb_id": "524434"},    # Another Round — Thomas Vinterberg
            {"year": 2019, "tmdb_id": "540903"},    # Parasite — Bong Joon-ho
            {"year": 2018, "tmdb_id": "458818"},    # Capernaum — Nadine Labaki (verify — Lebanon/French co-production)
            # Add others from europeanfilmacademy.org/European-Film-Awards
        ],
    },

    # ------------------------------------------------------------------ #
    #  Saturn Award — Best Science Fiction Film                            #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "saturn_best_scifi",
        "name": "Saturn Award Best Sci-Fi Film",
        "icon": "🪐",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "934632"},    # Poor Things — Yorgos Lanthimos (verify category)
            {"year": 2023, "tmdb_id": "505642"},    # Avatar: The Way of Water — James Cameron
            {"year": 2022, "tmdb_id": "438631"},    # Dune — Denis Villeneuve
            {"year": 2020, "tmdb_id": "330457"},    # Frozen II — Jennifer Lee & Chris Buck (verify category)
            {"year": 2019, "tmdb_id": "299537"},    # Captain Marvel (verify)
            # Add others from en.wikipedia.org/wiki/Saturn_Award_for_Best_Science_Fiction_Film
        ],
    },

    # ------------------------------------------------------------------ #
    #  SXSW Film Festival — Grand Jury Award (Narrative Feature)           #
    #  Source: TMDB movie IDs                                              #
    # ------------------------------------------------------------------ #
    {
        "slug": "sxsw_grand_jury",
        "name": "SXSW Grand Jury Award",
        "icon": "🤠",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            # {"year": 2024, "tmdb_id": None},   # Look up at sxsw.com/awards
            # {"year": 2023, "tmdb_id": None},
            # {"year": 2022, "tmdb_id": None},
            # Add TMDB IDs from sxsw.com and themoviedb.org
        ],
    },

    # ------------------------------------------------------------------ #
    #  Toronto International Film Festival — People's Choice Award         #
    #  Source: TMDB movie IDs  (TIFF PC Award is a strong Oscar predictor) #
    # ------------------------------------------------------------------ #
    {
        "slug": "tiff_peoples_choice",
        "name": "TIFF People's Choice Award",
        "icon": "🍁",
        "media_type": "movie",
        "source": "tmdb",
        "winners": [
            {"year": 2024, "tmdb_id": "1079091"},   # The Substance — Coralie Fargeat (verify — she won Palme)
            {"year": 2023, "tmdb_id": "872585"},    # American Fiction — Cord Jefferson
            {"year": 2022, "tmdb_id": "785084"},    # The Whale — Darren Aronofsky (verify)
            {"year": 2021, "tmdb_id": "823754"},    # Belfast — Kenneth Branagh
            {"year": 2020, "tmdb_id": "615173"},    # Nomadland — Chloé Zhao
            {"year": 2019, "tmdb_id": "503924"},    # 1917 — Sam Mendes (verify TIFF date)
            # Add others from en.wikipedia.org/wiki/Toronto_International_Film_Festival_People%27s_Choice_Award
        ],
    },

    # ------------------------------------------------------------------ #
    #  International Emmy — Best Drama Series                              #
    #  Source: TMDB TV IDs                                                 #
    # ------------------------------------------------------------------ #
    {
        "slug": "intl_emmy_best_drama",
        "name": "International Emmy Best Drama",
        "icon": "📺",
        "media_type": "tv",
        "source": "tmdb",
        "winners": [
            # {"year": 2024, "tmdb_id": None},   # Look up at iemmys.tv
            # {"year": 2023, "tmdb_id": None},
            # Add TMDB TV IDs from themoviedb.org/tv/<id>
        ],
    },
]
