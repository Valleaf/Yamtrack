#!/usr/bin/env python3
"""
apply_country_worldmap.py
Run from the repo root: python apply_country_worldmap.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
APP = SRC / "app"


def patch(path: Path, old: str, new: str, label: str = "") -> bool:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        print(f"  SKIP {label or path.name} — pattern not found (already patched?)")
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"  OK   {label or path.name}")
    return True


def write(path: Path, content: str, label: str = "") -> None:
    path.write_text(content, encoding="utf-8")
    print(f"  OK   {label or path.name}")


# ─────────────────────────────────────────────────────────────
# 1. Item model — add country field
# ─────────────────────────────────────────────────────────────
print("\n[1] Item model — adding country field")
patch(
    APP / "models.py",
    old='    title = models.TextField()\n    image = models.URLField()',
    new='    title = models.TextField()\n    image = models.URLField()\n    country = models.CharField(max_length=2, blank=True, default="")',
    label="models.py — Item.country field",
)

# ─────────────────────────────────────────────────────────────
# 2. Migration
# ─────────────────────────────────────────────────────────────
print("\n[2] Writing migration 0063_item_country.py")
write(APP / "migrations" / "0063_item_country.py", '''\
from django.db import migrations, models


class Migration(migrations.Migration):
    """Add country field to Item."""

    dependencies = [
        ("app", "0062_add_music_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="country",
            field=models.CharField(blank=True, default="", max_length=2),
        ),
    ]
''')

# ─────────────────────────────────────────────────────────────
# 3. tmdb.py — fix get_country() to return ISO-2 + top-level country key
# ─────────────────────────────────────────────────────────────
print("\n[3] tmdb.py")
tmdb = APP / "providers" / "tmdb.py"

# get_country returns iso_3166_1 instead of name
patch(tmdb,
    old='        return countries[0]["name"]\n    return None',
    new='        return countries[0]["iso_3166_1"]\n    return None',
    label="tmdb.py — get_country() → ISO alpha-2",
)

# movie(): assign country variable before building the dict
patch(tmdb,
    old='        cast = response.get("credits", {}).get("cast", [])\n        filtered_cast = [',
    new='        country = get_country(response["production_countries"])\n        cast = response.get("credits", {}).get("cast", [])\n        filtered_cast = [',
    label="tmdb.py — movie() country variable",
)
# movie(): remove old inline call in details, replace with variable
patch(tmdb,
    old='                "country": get_country(response["production_countries"]),',
    new='                "country": country,',
    label="tmdb.py — movie() details.country uses variable",
)
# movie(): add top-level country key after score_count
patch(tmdb,
    old='            "score_count": response["vote_count"],\n            "details": {\n                "format": "Movie",',
    new='            "score_count": response["vote_count"],\n            "country": country,\n            "details": {\n                "format": "Movie",',
    label="tmdb.py — movie() top-level country",
)

# process_tv(): assign country variable
patch(tmdb,
    old='    num_episodes = response["number_of_episodes"]\n    next_episode = response.get("next_episode_to_air")\n    last_episode = response.get("last_episode_to_air")\n    return {',
    new='    num_episodes = response["number_of_episodes"]\n    next_episode = response.get("next_episode_to_air")\n    last_episode = response.get("last_episode_to_air")\n    country = get_country(response["production_countries"])\n    return {',
    label="tmdb.py — process_tv() country variable",
)
# process_tv(): remove old inline call in details
patch(tmdb,
    old='            "country": get_country(response["production_countries"]),',
    new='            "country": country,',
    label="tmdb.py — process_tv() details.country uses variable",
)
# process_tv(): add top-level country key after score_count
patch(tmdb,
    old='        "score_count": response["vote_count"],\n        "details": {\n            "format": "TV",',
    new='        "score_count": response["vote_count"],\n        "country": country,\n        "details": {\n            "format": "TV",',
    label="tmdb.py — process_tv() top-level country",
)

# enrich_season_with_tv_data(): propagate country from TV show to season
patch(tmdb,
    old='    season_data["genres"] = tv_data["genres"]\n    if season_data["synopsis"] == "No synopsis available.":\n        season_data["synopsis"] = tv_data["synopsis"]\n    return season_data',
    new='    season_data["genres"] = tv_data["genres"]\n    season_data["country"] = tv_data.get("country")\n    if season_data["synopsis"] == "No synopsis available.":\n        season_data["synopsis"] = tv_data["synopsis"]\n    return season_data',
    label="tmdb.py — enrich_season_with_tv_data() propagates country",
)

# ─────────────────────────────────────────────────────────────
# 4. musicbrainz.py — add _get_artist_country() + country in album()
# ─────────────────────────────────────────────────────────────
print("\n[4] musicbrainz.py")
mb = APP / "providers" / "musicbrainz.py"

patch(mb,
    old='def _artist_id(obj: dict) -> str | None:\n    for ac in obj.get("artist-credit", []):\n        if isinstance(ac, dict) and ac.get("artist"):\n            return ac["artist"].get("id")\n    return None',
    new='''\
def _artist_id(obj: dict) -> str | None:
    for ac in obj.get("artist-credit", []):
        if isinstance(ac, dict) and ac.get("artist"):
            return ac["artist"].get("id")
    return None


def _get_artist_country(obj: dict) -> str | None:
    """Extract ISO 3166-1 alpha-2 country code from the first artist credit area.

    Requires the release-group to be fetched with inc containing artists so
    that artist-credit[].artist.area is populated.
    """
    for ac in obj.get("artist-credit", []):
        if not isinstance(ac, dict):
            continue
        artist = ac.get("artist") or {}
        area = artist.get("area") or {}
        codes = area.get("iso-3166-1-codes") or []
        if codes:
            return codes[0]
    return None''',
    label="musicbrainz.py — _get_artist_country()",
)

patch(mb,
    old='    artist_names = _format_artists(data)\n    artist_id = _artist_id(data)\n\n    genres',
    new='    artist_names = _format_artists(data)\n    artist_id = _artist_id(data)\n    country = _get_artist_country(data)\n\n    genres',
    label="musicbrainz.py — album() extract country",
)

patch(mb,
    old='        "score_count": 0,\n        "details": {',
    new='        "score_count": 0,\n        "country": country,\n        "details": {',
    label="musicbrainz.py — album() top-level country",
)

# ─────────────────────────────────────────────────────────────
# 5. igdb.py — country via involved_companies.company.country
# ─────────────────────────────────────────────────────────────
print("\n[5] igdb.py")
igdb = APP / "providers" / "igdb.py"

patch(igdb,
    old='def handle_error(error):\n    """Handle IGDB API errors."""',
    new='''\
# IGDB returns ISO 3166-1 numeric country codes on company objects.
_IGDB_COUNTRY_NUMERIC_TO_ALPHA2: dict[int, str] = {
    36: "AU", 40: "AT", 56: "BE", 76: "BR", 124: "CA", 156: "CN",
    203: "CZ", 208: "DK", 246: "FI", 250: "FR", 276: "DE", 300: "GR",
    344: "HK", 356: "IN", 372: "IE", 376: "IL", 380: "IT", 392: "JP",
    410: "KR", 528: "NL", 554: "NZ", 578: "NO", 616: "PL", 620: "PT",
    643: "RU", 724: "ES", 752: "SE", 756: "CH", 804: "UA", 826: "GB",
    840: "US",
}


def _igdb_country_to_alpha2(numeric) -> str | None:
    """Convert IGDB numeric country code to ISO 3166-1 alpha-2."""
    if numeric is None:
        return None
    return _IGDB_COUNTRY_NUMERIC_TO_ALPHA2.get(int(numeric))


def handle_error(error):
    """Handle IGDB API errors."""''',
    label="igdb.py — country mapping + helper",
)

patch(igdb,
    old='"fields name,cover.image_id,artworks.image_id,"\n            "url,summary,game_type,first_release_date,total_rating,total_rating_count,"\n            "genres.name,themes.name,platforms.name,involved_companies.company.name,"',
    new='"fields name,cover.image_id,artworks.image_id,"\n            "url,summary,game_type,first_release_date,total_rating,total_rating_count,"\n            "genres.name,themes.name,platforms.name,involved_companies.company.name,involved_companies.company.country,"',
    label="igdb.py — add company.country to fields query",
)

patch(igdb,
    old='def get_companies(response):\n    """Return the companies involved in the game."""',
    new='''\
def get_developer_country(response) -> int | None:
    """Return the numeric country code of the first company that has one set."""
    for ic in response.get("involved_companies") or []:
        company = ic.get("company") or {}
        if company.get("country") is not None:
            return company["country"]
    return None


def get_companies(response):
    """Return the companies involved in the game."""''',
    label="igdb.py — get_developer_country()",
)

patch(igdb,
    old='            "score_count": response.get("total_rating_count"),\n            "details": {',
    new='            "score_count": response.get("total_rating_count"),\n            "country": _igdb_country_to_alpha2(get_developer_country(response)),\n            "details": {',
    label="igdb.py — game() top-level country",
)

# ─────────────────────────────────────────────────────────────
# 6. views.py — pass country into Item.update_or_create defaults
# ─────────────────────────────────────────────────────────────
print("\n[6] views.py — Item country on sync")
views = APP / "views.py"

patch(views,
    old='"title": metadata["title"],\n                "image": metadata["image"],\n            },\n        )',
    new='"title": metadata["title"],\n                "image": metadata["image"],\n                "country": metadata.get("country", "") or "",\n            },\n        )',
    label="views.py — sync_metadata defaults include country",
)

# ─────────────────────────────────────────────────────────────
# 7. helpers.py — Item country on initial track
# ─────────────────────────────────────────────────────────────
print("\n[7] helpers.py — Item country on track")
helpers = APP / "helpers.py"

patch(helpers,
    old='"title": metadata["title"],\n                "image": metadata["image"],',
    new='"title": metadata["title"],\n                "image": metadata["image"],\n                "country": metadata.get("country", "") or "",',
    label="helpers.py — get_or_create defaults include country",
)

# ─────────────────────────────────────────────────────────────
# 8. statistics.py — add get_world_map_data()
# ─────────────────────────────────────────────────────────────
print("\n[8] statistics.py — get_world_map_data()")
stats = APP / "statistics.py"
stats_text = stats.read_text(encoding="utf-8")

world_map_fn = '''

# ISO 3166-1 alpha-2 → English country name for map tooltips
_ISO_TO_NAME: dict[str, str] = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan",
    "AG": "Antigua and Barbuda", "AL": "Albania", "AM": "Armenia",
    "AO": "Angola", "AR": "Argentina", "AT": "Austria", "AU": "Australia",
    "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
    "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria",
    "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BN": "Brunei",
    "BO": "Bolivia", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan",
    "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada",
    "CD": "DR Congo", "CF": "Central African Republic", "CG": "Congo",
    "CH": "Switzerland", "CI": "Côte d\'Ivoire", "CL": "Chile",
    "CM": "Cameroon", "CN": "China", "CO": "Colombia", "CR": "Costa Rica",
    "CU": "Cuba", "CV": "Cape Verde", "CY": "Cyprus", "CZ": "Czechia",
    "DE": "Germany", "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica",
    "DO": "Dominican Republic", "DZ": "Algeria", "EC": "Ecuador",
    "EE": "Estonia", "EG": "Egypt", "ER": "Eritrea", "ES": "Spain",
    "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FR": "France",
    "GA": "Gabon", "GB": "United Kingdom", "GD": "Grenada", "GE": "Georgia",
    "GH": "Ghana", "GM": "Gambia", "GN": "Guinea", "GQ": "Equatorial Guinea",
    "GR": "Greece", "GT": "Guatemala", "GW": "Guinea-Bissau", "GY": "Guyana",
    "HN": "Honduras", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary",
    "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India",
    "IQ": "Iraq", "IR": "Iran", "IS": "Iceland", "IT": "Italy",
    "JM": "Jamaica", "JO": "Jordan", "JP": "Japan", "KE": "Kenya",
    "KG": "Kyrgyzstan", "KH": "Cambodia", "KI": "Kiribati", "KM": "Comoros",
    "KN": "Saint Kitts and Nevis", "KP": "North Korea", "KR": "South Korea",
    "KW": "Kuwait", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon",
    "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka",
    "LR": "Liberia", "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg",
    "LV": "Latvia", "LY": "Libya", "MA": "Morocco", "MC": "Monaco",
    "MD": "Moldova", "ME": "Montenegro", "MG": "Madagascar",
    "MH": "Marshall Islands", "MK": "North Macedonia", "ML": "Mali",
    "MM": "Myanmar", "MN": "Mongolia", "MR": "Mauritania", "MT": "Malta",
    "MU": "Mauritius", "MV": "Maldives", "MW": "Malawi", "MX": "Mexico",
    "MY": "Malaysia", "MZ": "Mozambique", "NA": "Namibia", "NE": "Niger",
    "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway",
    "NP": "Nepal", "NR": "Nauru", "NZ": "New Zealand", "OM": "Oman",
    "PA": "Panama", "PE": "Peru", "PG": "Papua New Guinea", "PH": "Philippines",
    "PK": "Pakistan", "PL": "Poland", "PT": "Portugal", "PW": "Palau",
    "PY": "Paraguay", "QA": "Qatar", "RO": "Romania", "RS": "Serbia",
    "RU": "Russia", "RW": "Rwanda", "SA": "Saudi Arabia",
    "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan",
    "SE": "Sweden", "SG": "Singapore", "SI": "Slovenia", "SK": "Slovakia",
    "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal",
    "SO": "Somalia", "SR": "Suriname", "SS": "South Sudan",
    "ST": "São Tomé and Príncipe", "SV": "El Salvador", "SY": "Syria",
    "SZ": "Eswatini", "TD": "Chad", "TG": "Togo", "TH": "Thailand",
    "TJ": "Tajikistan", "TL": "Timor-Leste", "TM": "Turkmenistan",
    "TN": "Tunisia", "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago",
    "TV": "Tuvalu", "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda",
    "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan",
    "VA": "Vatican City", "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela", "VN": "Vietnam", "VU": "Vanuatu", "WS": "Samoa",
    "YE": "Yemen", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe",
}


def get_world_map_data(user_media: dict) -> dict:
    """Aggregate item counts by country and media type for the world map.

    Returns a dict with:
      - "by_type": { media_type: { "XX": count, ... }, ... }
      - "combined": { "XX": count, ... }
      - "country_names": { "XX": "Full Name", ... }
      - "media_types": [list of media types that have country data]
    """
    from app.models import Item  # avoid circular import

    # Collect all item PKs across every media type list
    all_items = []
    for media_list in user_media.values():
        for entry in media_list:
            item = getattr(entry, "item", None)
            if item is not None:
                all_items.append(item)

    # Deduplicate by item pk
    seen = set()
    unique_items = []
    for item in all_items:
        if item.pk not in seen:
            seen.add(item.pk)
            unique_items.append(item)

    by_type: dict[str, dict[str, int]] = {}
    combined: dict[str, int] = {}

    for item in unique_items:
        code = (item.country or "").strip().upper()
        if not code or len(code) != 2:
            continue
        media_type = item.media_type
        by_type.setdefault(media_type, {})
        by_type[media_type][code] = by_type[media_type].get(code, 0) + 1
        combined[code] = combined.get(code, 0) + 1

    # Build country name lookup for codes actually present in the data
    all_codes = set(combined.keys())
    country_names = {code: _ISO_TO_NAME.get(code, code) for code in all_codes}

    # Only list media types that have at least one country
    media_types_with_data = sorted(by_type.keys())

    return {
        "by_type": by_type,
        "combined": combined,
        "country_names": country_names,
        "media_types": media_types_with_data,
    }
'''

if "get_world_map_data" not in stats_text:
    stats_text += world_map_fn
    stats.write_text(stats_text, encoding="utf-8")
    print("  OK   statistics.py — get_world_map_data()")
else:
    print("  SKIP statistics.py — get_world_map_data() already present")

# ─────────────────────────────────────────────────────────────
# 9. views.py — pass world_map_data to statistics template
# ─────────────────────────────────────────────────────────────
print("\n[9] views.py — pass world_map_data to statistics view")

patch(views,
    old='from app.statistics import (',
    new='from app.statistics import (\n    get_world_map_data,',
    label="views.py — import get_world_map_data",
)

# Find the statistics view context dict and append world_map_data
# The context dict ends with something like "return render(request, ...)"
patch(views,
    old='    context = get_stats(user_media)\n    return render(request, "app/statistics.html", context)',
    new='    context = get_stats(user_media)\n    context["world_map"] = get_world_map_data(user_media)\n    return render(request, "app/statistics.html", context)',
    label="views.py — statistics view passes world_map",
)

# ─────────────────────────────────────────────────────────────
# 10. statistics.html — world map section
# ─────────────────────────────────────────────────────────────
print("\n[10] statistics.html — world map section")
tmpl = SRC / "templates" / "app" / "statistics.html"

world_map_html = '''
{% if world_map.combined %}
<div class="mt-4">
  <h4 class="mb-3">{% trans "Media World Map" %}</h4>

  {# Tab buttons #}
  <ul class="nav nav-tabs mb-3" id="worldMapTabs" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="wm-tab-combined" data-bs-toggle="tab"
              data-bs-target="#wm-combined" type="button" role="tab"
              aria-controls="wm-combined" aria-selected="true">
        {% trans "All" %}
      </button>
    </li>
    {% for mt in world_map.media_types %}
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="wm-tab-{{ mt }}" data-bs-toggle="tab"
              data-bs-target="#wm-{{ mt }}" type="button" role="tab"
              aria-controls="wm-{{ mt }}" aria-selected="false">
        {{ mt|title }}
      </button>
    </li>
    {% endfor %}
  </ul>

  {# Tab panes — one canvas per tab #}
  <div class="tab-content" id="worldMapTabsContent">
    <div class="tab-pane fade show active" id="wm-combined" role="tabpanel" aria-labelledby="wm-tab-combined">
      <canvas id="worldmap-combined" style="width:100%;max-height:420px;"></canvas>
    </div>
    {% for mt in world_map.media_types %}
    <div class="tab-pane fade" id="wm-{{ mt }}" role="tabpanel" aria-labelledby="wm-tab-{{ mt }}">
      <canvas id="worldmap-{{ mt }}" style="width:100%;max-height:420px;"></canvas>
    </div>
    {% endfor %}
  </div>
</div>

{# World map data passed to JS #}
<script>
window.WORLD_MAP_DATA = {
  combined: {{ world_map.combined|safe }},
  byType:   {{ world_map.by_type|safe }},
  names:    {{ world_map.country_names|safe }},
  types:    {{ world_map.media_types|safe }},
};
</script>

<script>
(function () {
  'use strict';

  // Only load Chart.js geo if we have data — lazy-load to keep page fast
  const cdn = 'https://cdn.jsdelivr.net/npm/';
  function loadScript(src, cb) {
    const s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    document.head.appendChild(s);
  }

  function buildMap(canvasId, countryData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
      .then(r => r.json())
      .then(worldData => {
        // topojson → feature collection
        const countries = ChartGeo.topojson.feature(worldData, worldData.objects.countries);
        const maxVal = Math.max(...Object.values(countryData), 1);

        const data = countries.features.map(f => {
          // UN numeric → alpha-2 via a small runtime lookup
          // We use the name match from our server-side names dict
          // Chart.js geo identifies countries by their ISO numeric id in topojson
          const id = String(f.id);
          // We pass alpha-2 data; resolve via a tiny inline map
          const alpha2 = NUMERIC_TO_ALPHA2[id];
          const value = alpha2 ? (countryData[alpha2] || 0) : 0;
          return { feature: f, value };
        });

        new Chart(canvas, {
          type: 'choropleth',
          data: {
            labels: countries.features.map(f => {
              const alpha2 = NUMERIC_TO_ALPHA2[String(f.id)];
              return alpha2
                ? (window.WORLD_MAP_DATA.names[alpha2] || alpha2)
                : (f.properties.name || f.id);
            }),
            datasets: [{
              label: 'Items',
              data,
              backgroundColor(ctx) {
                if (!ctx.raw) return 'rgba(0,0,0,0)';
                const v = ctx.raw.value || 0;
                if (v === 0) return 'rgba(200,200,200,0.4)';
                const t = v / maxVal;
                // Blue gradient: light → deep
                const r = Math.round(220 - t * 180);
                const g = Math.round(220 - t * 130);
                const b = Math.round(255 - t * 60);
                return `rgba(${r},${g},${b},0.85)`;
              },
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label(ctx) {
                    const v = ctx.raw ? ctx.raw.value : 0;
                    return v ? `${v} item${v !== 1 ? 's' : ''}` : 'No items';
                  },
                },
              },
            },
            scales: {
              projection: { axis: 'x', projection: 'naturalEarth1' },
              color: { display: false },
            },
          },
        });
      });
  }

  // Compact UN numeric → ISO alpha-2 for countries that appear in topojson
  const NUMERIC_TO_ALPHA2 = {
    "4":"AF","8":"AL","12":"DZ","24":"AO","32":"AR","36":"AU","40":"AT","50":"BD",
    "56":"BE","68":"BO","76":"BR","100":"BG","104":"MM","116":"KH","120":"CM",
    "124":"CA","140":"CF","144":"LK","152":"CL","156":"CN","170":"CO","180":"CD",
    "188":"CR","191":"HR","192":"CU","196":"CY","203":"CZ","208":"DK","214":"DO",
    "218":"EC","818":"EG","222":"SV","233":"EE","231":"ET","246":"FI","250":"FR",
    "266":"GA","276":"DE","288":"GH","300":"GR","320":"GT","324":"GN","332":"HT",
    "340":"HN","348":"HU","356":"IN","360":"ID","364":"IR","368":"IQ","372":"IE",
    "376":"IL","380":"IT","388":"JM","392":"JP","400":"JO","398":"KZ","404":"KE",
    "408":"KP","410":"KR","414":"KW","418":"LA","422":"LB","430":"LR","434":"LY",
    "440":"LT","442":"LU","450":"MG","454":"MW","458":"MY","484":"MX","504":"MA",
    "508":"MZ","516":"NA","524":"NP","528":"NL","540":"NC","554":"NZ","558":"NI",
    "562":"NE","566":"NG","578":"NO","586":"PK","591":"PA","598":"PG","600":"PY",
    "604":"PE","608":"PH","616":"PL","620":"PT","630":"PR","642":"RO","643":"RU",
    "646":"RW","682":"SA","686":"SN","694":"SL","706":"SO","710":"ZA","724":"ES",
    "729":"SD","752":"SE","756":"CH","760":"SY","764":"TH","792":"TR","800":"UG",
    "804":"UA","784":"AE","826":"GB","840":"US","858":"UY","860":"UZ","862":"VE",
    "704":"VN","887":"YE","894":"ZM","716":"ZW","051":"AM","031":"AZ","112":"BY",
    "070":"BA","076":"BR","100":"BG","795":"TM","762":"TJ","496":"MN","498":"MD",
    "703":"SK","705":"SI","688":"RS","807":"MK","008":"AL","070":"BA"
  };

  function initMaps() {
    const D = window.WORLD_MAP_DATA;

    // Build combined map
    buildMap('worldmap-combined', D.combined);

    // Build per-type maps (lazy: only when tab is first shown)
    D.types.forEach(mt => {
      const tabEl = document.getElementById('wm-tab-' + mt);
      if (!tabEl) return;
      let built = false;
      tabEl.addEventListener('shown.bs.tab', () => {
        if (!built) {
          buildMap('worldmap-' + mt, D.byType[mt] || {});
          built = true;
        }
      });
    });
  }

  // Load Chart.js → chartjs-chart-geo → then init
  loadScript(cdn + 'chart.js@4/dist/chart.umd.min.js', () => {
    loadScript(cdn + 'chartjs-chart-geo@4/build/index.umd.min.js', initMaps);
  });
})();
</script>
{% endif %}
'''

tmpl_text = tmpl.read_text(encoding="utf-8")
if "world_map" not in tmpl_text:
    # Append before the last {% endblock %}
    last_endblock = tmpl_text.rfind("{% endblock %}")
    if last_endblock != -1:
        tmpl_text = tmpl_text[:last_endblock] + world_map_html + "\n{% endblock %}"
        tmpl.write_text(tmpl_text, encoding="utf-8")
        print("  OK   statistics.html — world map section added")
    else:
        # Just append
        tmpl.write_text(tmpl_text + world_map_html, encoding="utf-8")
        print("  OK   statistics.html — world map section appended")
else:
    print("  SKIP statistics.html — world map already present")

print("\n✅  Done. Next steps:")
print("   python src/manage.py migrate")
print("   python src/manage.py runserver")
print()
print("   Existing items won't have country populated yet.")
print("   They'll get it the next time their metadata is synced,")
print("   or you can run the optional backfill:")
print("   python src/manage.py shell -c \"")
print("   from app.models import Item; from app.providers.services import get_media_metadata")
print("   for item in Item.objects.filter(country='').exclude(source='manual'):") 
print("       try:")
print("           m = get_media_metadata(item.media_type, item.media_id, item.source)")
print("           item.country = m.get('country','') or ''")
print("           item.save(update_fields=['country'])")
print("       except Exception as e: print(item, e)\"")
